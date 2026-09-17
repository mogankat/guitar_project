// ════════════════════════════════════════════════════════════════
// Sampled instruments — real guitar/bass recordings, shared by the
// fretboard (index.html) and the cheat sheet (theory.html).
//
// Recordings live in samples/<set>/ as MP3s named by pitch (A2.mp3,
// Cs3.mp3 = C#3 …). tools/build_sample_bundles.py packs each set into
// samples/<set>.js, which is what gets loaded: a <script> works even when the
// page is opened straight from disk (file://), where fetch() is blocked. A note is played from
// the nearest recording, re-pitched with playbackRate. A set is only
// downloaded when it is first chosen; until it is ready (or if it can't be
// loaded, e.g. offline before first use) play() returns false and the page
// falls back to its synthesized string.
//
// Samples: tonejs-instruments by Nicholaus Brosowsky (CC BY 3.0) — see
// samples/CREDITS.md.
// ════════════════════════════════════════════════════════════════
(function () {
  const BASE = 'samples/';
  const SETS = { acoustic: 'guitar-acoustic', electric: 'guitar-electric', nylon: 'guitar-nylon', bass: 'bass-electric' };
  const NAMES = { acoustic: 'Acoustic', electric: 'Electric', nylon: 'Nylon', bass: 'Bass' };
  const PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
  const MAX_RING = 4;                  // seconds a note may ring before fading
  const sets = {};                     // tone -> { status, promise, zones: [{ midi, buf }], gain }
  const listeners = [];
  const waiting = {};                  // set folder -> { res, rej } while its bundle loads
  let decoder = null;

  function nameToMidi(n) {             // "Cs4" / "Db4" / "C#4" -> MIDI number
    const m = /^([A-G])(s|#|b)?(-?\d)$/.exec(n);
    if (!m) return null;
    return (+m[3] + 1) * 12 + PC[m[1]] + (m[2] === 'b' ? -1 : m[2] ? 1 : 0);
  }
  // Bundles call this when they run.
  function register(dir, data) {
    const w = waiting[dir];
    if (w) { delete waiting[dir]; w.res(data); }
  }
  function loadBundle(dir) {
    return new Promise((res, rej) => {
      waiting[dir] = { res, rej };
      const sc = document.createElement('script');
      sc.src = BASE + dir + '.js';
      sc.async = true;
      const fail = () => { if (waiting[dir]) { delete waiting[dir]; rej(new Error('could not load ' + dir)); } };
      sc.onerror = fail;
      sc.onload = () => setTimeout(fail, 0);         // loaded but never registered
      document.head.appendChild(sc);
    });
  }
  function b64ToArrayBuffer(b64) {
    const bin = atob(b64), n = bin.length, u = new Uint8Array(n);
    for (let i = 0; i < n; i++) u[i] = bin.charCodeAt(i);
    return u.buffer;
  }
  function decode(ab) {
    // A private offline context decodes, so loading never needs a user gesture;
    // decoded buffers play in any AudioContext.
    if (!decoder) {
      const OAC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      decoder = new OAC(2, 1, 44100);
    }
    return new Promise((res, rej) => {
      const p = decoder.decodeAudioData(ab, res, rej);
      if (p && p.then) p.then(res, rej);
    });
  }
  // Where the note actually starts: decoders can add a few ms of padding, which
  // would make fast runs and strums drag.
  function onset(buf) {
    const d = buf.getChannelData(0), n = Math.min(d.length, Math.round(buf.sampleRate * 0.3));
    let peak = 0;
    for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(d[i]));
    const th = peak * 0.05;
    for (let i = 0; i < n; i++) if (Math.abs(d[i]) > th) return Math.max(0, i / buf.sampleRate - 0.002);
    return 0;
  }
  function emit(tone) { listeners.forEach(fn => { try { fn(tone, status(tone)); } catch (e) {} }); }

  // Start loading a sound (safe to call repeatedly). Resolves true when ready.
  function load(tone) {
    const dir = SETS[tone];
    if (!dir) return Promise.resolve(false);
    if (sets[tone]) return sets[tone].promise;
    const s = sets[tone] = { status: 'loading', zones: [], gain: 1 };
    emit(tone);
    s.promise = loadBundle(dir).then(data => {
      const names = Object.keys((data && data.notes) || {});
      if (!names.length) throw new Error('no samples for ' + dir);
      s.gain = data.gain || 1;
      return Promise.all(names.map(n =>
        decode(b64ToArrayBuffer(data.notes[n]))
          .then(buf => ({ midi: nameToMidi(n), buf, offset: onset(buf) }))
          .catch(() => null)));                        // one bad file shouldn't sink the set
    }).then(zones => {
      s.zones = zones.filter(z => z && z.midi != null).sort((a, b) => a.midi - b.midi);
      if (!s.zones.length) throw new Error('no playable samples');
      s.status = 'ready';
      emit(tone);
      return true;
    }).catch(() => {
      s.status = 'failed';
      emit(tone);
      return false;
    });
    return s.promise;
  }
  function status(tone) { return sets[tone] ? sets[tone].status : (SETS[tone] ? 'idle' : 'none'); }
  function ready(tone) { return status(tone) === 'ready'; }

  // Output for the recordings: just a safety limiter so big chords don't clip
  // (no tone shaping — the recordings already sound like the instrument).
  function bus(ctx) {
    if (ctx._sampleBus) return ctx._sampleBus;
    const inp = ctx.createGain(); inp.gain.value = 0.9;
    const lim = ctx.createDynamicsCompressor();
    lim.threshold.value = -3; lim.knee.value = 3; lim.ratio.value = 20;
    lim.attack.value = 0.002; lim.release.value = 0.15;
    inp.connect(lim); lim.connect(ctx.destination);
    return (ctx._sampleBus = inp);
  }

  // Play `freq` (Hz) on `tone` at audio time `when`.
  // Returns false if the sound isn't loaded (caller falls back to synthesis).
  // opts: { dur } seconds to hold before a short release (default: let it ring).
  function play(ctx, tone, freq, when, vel, opts) {
    const s = sets[tone];
    if (!s || s.status !== 'ready') { if (!s) load(tone); return false; }
    const midi = 69 + 12 * Math.log2(freq / 440);
    let z = s.zones[0];
    for (const c of s.zones) if (Math.abs(c.midi - midi) < Math.abs(z.midi - midi)) z = c;
    const rate = Math.pow(2, (midi - z.midi) / 12);
    const t0 = Math.max(when == null ? ctx.currentTime : when, ctx.currentTime);
    const src = ctx.createBufferSource();
    src.buffer = z.buf;
    src.playbackRate.value = rate;
    const g = ctx.createGain();
    const level = Math.max(0.0001, (vel == null ? 1 : vel) * s.gain);
    const natural = (z.buf.duration - z.offset) / rate;
    const hold = Math.min(opts && opts.dur ? opts.dur : MAX_RING, natural);
    g.gain.setValueAtTime(level, t0);
    g.gain.setValueAtTime(level, t0 + hold);
    g.gain.exponentialRampToValueAtTime(0.0005, t0 + hold + 0.35);
    src.connect(g); g.connect(bus(ctx));
    src.start(t0, z.offset);
    src.stop(t0 + Math.min(hold + 0.4, natural + 0.05));
    return true;
  }

  function onChange(fn) { listeners.push(fn); }

  window.GuitarSamples = { load, ready, status, play, onChange, register, SETS, NAMES };
})();
