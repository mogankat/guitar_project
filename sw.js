const CACHE_NAME = 'guitar-fretboard-v5';
const SAMPLE_CACHE = 'guitar-samples-v2';   // recordings: kept across app updates
const ASSETS = [
  '/',
  '/index.html',
  '/theory.html',
  '/sampler.js',
  '/manifest.json',
  '/icons/icon-192.svg'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME && k !== SAMPLE_CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const req = e.request;

  // Network-first for page navigations so app updates land without a manual
  // cache bump; fall back to the cached shell when offline.
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then(r => r || caches.match('/index.html')))
    );
    return;
  }

  // Instrument recording bundles: cache-first, saved the first time each is fetched,
  // so a sound works offline once it has been used.
  const url = new URL(req.url);
  if (url.origin === location.origin && /\/samples\/[\w-]+\.js$/.test(url.pathname)) {
    e.respondWith(
      caches.open(SAMPLE_CACHE).then(cache =>
        cache.match(req).then(hit => hit || fetch(req).then(res => {
          if (res.ok) cache.put(req, res.clone());
          return res;
        })))
    );
    return;
  }

  // The sample player: network-first so updates land, cache when offline.
  if (url.origin === location.origin && /\/sampler\.js$/.test(url.pathname)) {
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(req, copy));
        return res;
      }).catch(() => caches.match(req))
    );
    return;
  }

  // Cache-first for static assets (icons, manifest, etc.).
  e.respondWith(
    caches.match(req).then(r => r || fetch(req))
  );
});
