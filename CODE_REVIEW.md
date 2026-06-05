# Guitar Fretboard — Code Review

Reviewed: index.html (active PWA, 1,556 lines), www/index.html (duplicate), streamlit_app.py (931 lines, older version), sw.js, manifest.json, package.json, requirements.txt, and the committed android/ wrapper.

Findings are grouped and numbered so you can pick which to apply. Severity reflects impact, not effort.

---

## A. Repository hygiene — highest impact

**A1. No `.gitignore`; build artifacts and dependencies are committed. (High)**
2,102 of the 2,177 tracked files are `node_modules/` (27 MB), `android/app/build/` (19 MB), and `.venv/`. The working tree is ~400 MB. These are all regenerable and should never be in version control. They bloat clones, pollute diffs, and create merge noise.

*Fix:* Add a `.gitignore` covering `node_modules/`, `.venv/`, `android/app/build/`, `android/.gradle/`, `android/build/`, `__pycache__/`, etc., then `git rm -r --cached` the offending paths in one cleanup commit. (This rewrites what's tracked going forward but leaves your local files intact.)

**A2. `package.json` metadata is wrong/empty. (Low)**
`"main": "sw.js"` is meaningless for this project (there's no npm entry point), `description` is empty, `author`/`keywords` are blank, and the only script is the default failing `test`. Minor, but it's the project's front door.

*Fix:* Set a real description, drop or correct `main`, and add useful scripts (e.g. a `cap sync` / build helper). Optionally add `"private": true`.

---

## B. Source duplication

**B1. `index.html` and `www/index.html` are byte-identical, hand-maintained copies. (High)**
Both are 1,556 lines and currently identical. Capacitor serves from `www/` (per `capacitor.config.json` `webDir: "www"`), while GitHub Pages serves the root `index.html`. Keeping two copies in sync by hand guarantees eventual drift — and the working tree already shows both files modified together, which is the maintenance tax in action.

*Fix:* Keep a single source of truth and generate the other. Options, simplest first: (a) a one-line `copy` npm script (`cp index.html www/index.html && cp manifest.json sw.js www/`) run before `cap sync`; (b) point Capacitor's `webDir` at the root; (c) a small build step. Manifest, sw.js and icons should flow the same way so `www/` is never edited directly.

---

## C. Dead / unused code

**C1. `streamlit_app.py` is a superseded parallel implementation. (Medium)**
The git history shows the project moved from a Streamlit Python app to the current vanilla-JS PWA (the JS version added bass mode, Web Audio, CAGED, tab writer, looper — none of which the Python file tracks). It's now a 931-line second codebase that isn't deployed and will rot. Keeping it is fine *if* it's intentionally a separate desktop entry point, but right now nothing references it and it duplicates the music-theory data tables already in the JS.

*Fix:* Decide its fate. If it's abandoned, delete it (and `requirements.txt`); if it's a kept alternative, add a short note to the README explaining when to use which, so it's clearly intentional rather than stale.

**C2. `requirements.txt` lists unused dependencies. (Low)**
It declares `numpy` and `sounddevice`, but `streamlit_app.py` imports only `streamlit` — neither is used anywhere. Anyone installing requirements pulls in a native-audio library for nothing.

*Fix:* Reduce to `streamlit>=1.27.0` (or delete the file with C1).

**C3. Dead DOM and no-op function in index.html. (Low)**
`<div id="info-display">` is permanently `display:none` (line 48/128) — the info text is now drawn inside the SVG instead — yet `updateInfoDisplay()` (line 1389) is still called at the end of every `renderFretboard()` and does nothing. Harmless but confusing.

*Fix:* Remove the `#info-display` element, the unused CSS rule, and the `updateInfoDisplay()` function and its call.

**C4. Fret-marker list contains positions that can never render. (Low)**
Line 481: `for (const f of [3, 5, 7, 9, 15, 17, 19, 21])` but `N_FRETS = 15`, so frets are only 0–14 and the guard `if (f < N_FRETS)` silently drops 15, 17, 19, 21. The 15-fret board also omits the single-dot at 12's neighbors. Not a bug, just misleading cruft.

*Fix:* Trim the array to `[3, 5, 7, 9]` (the markers actually visible at 15 frets), or raise `N_FRETS` if you want the higher positions.

---

## D. PWA / service worker

**D1. Service worker is cache-first with no update path and an incomplete asset list. (Medium)**
`sw.js` caches only `/`, `/index.html`, `/manifest.json` — it omits `icons/icon-192.svg` (referenced by the manifest), so the icon isn't available offline. More importantly the `fetch` handler is pure cache-first (`caches.match(...).then(r => r || fetch(...))`): once `index.html` is cached, users keep getting the old app until the `CACHE_NAME` is manually bumped (which is exactly why the git log has a "bump cache version to invalidate stale assets" commit — a recurring manual workaround).

*Fix:* Add the icon to `ASSETS`, and switch the HTML navigation request to network-first (or stale-while-revalidate) so updates land without a manual cache bump, while static assets stay cache-first.

**D2. `www/` PWA assets may be stale relative to root. (Low, follows from B1)**
`www/sw.js`, `www/manifest.json`, `www/icons/` are separate copies. Same drift risk as B1; fold them into the single-source build step.

---

## E. JavaScript inefficiencies & smells (index.html)

**E1. Full SVG rebuild + per-element listener rebinding on every render. (Medium)**
`renderFretboard()` regenerates the entire SVG as a string, sets `innerHTML`, then `querySelectorAll('.note-dot')` and `.strum-box'` and attaches a fresh `pointerdown` listener to every element — on every settings change *and* every resize tick. In "All Notes" view that's ~90 note dots re-created and re-bound each time. It works, but it's more GC churn and DOM work than needed.

*Fix:* Use event delegation — one `pointerdown` listener on `#fretboard-container` that reads `event.target.dataset` (`freq`/`s`/`f` for dots, `notes` for strum boxes). Attach it once in `init()`; the per-render loops and rebinding disappear. This is the single biggest code-quality win in the JS.

**E2. Redundant membership test in `getNoteCircles()`. (Low)**
Line 587: `if (ni in degs || degs[ni] !== undefined)` — the two conditions are equivalent for this object, so the `||` is dead. (`in` also matches inherited keys in general, so `degs[ni] !== undefined` is the safer single check.)

*Fix:* Reduce to `if (degs[ni] !== undefined)`.

**E3. 22 inline `on*` HTML attribute handlers calling global functions. (Low)**
Markup is peppered with `onclick=`, `onchange=`, `oninput=`, `onkeydown=` that call globals (`onSettingChange()`, `playProgression()`, etc.). It works in a single file, but it couples markup to a global namespace, blocks a future Content-Security-Policy (inline handlers require `unsafe-inline`), and scatters wiring across the document.

*Fix:* Move handler wiring into `init()` with `addEventListener` (you already do this for the menu, chips, and resize — the rest is inconsistent). Lower priority than the others; mainly a consistency/CSP concern.

**E4. Karplus-Strong synthesis allocates a 2.5 s buffer per note on the main thread. (Low)**
`playNote()` builds a `Float32Array` of `sampleRate * 2.5` samples (~110k floats at 44.1 kHz) and runs two full passes over it for *every* note, synchronously. Fine for taps; during fast strums/arpeggios or looped licks it can cause audible jank on weaker mobile devices.

*Fix:* If you notice stutter, cache/reuse buffers per (string,fret) or shorten the tail; not worth changing pre-emptively if playback feels fine on target devices.

**E5. Minor redundancy in `parseChord()`. (Low)**
It computes `norm = qual.toLowerCase().replace(/\s+/g,'')` and then looks up `PROG_CHORD_IVALS[qual] || [qual.toLowerCase()] || [norm]`; the middle term is subsumed by `norm` whenever there's no whitespace. Cosmetic.

*Fix:* Collapse to a single normalized lookup.

---

## Suggested order of operations

1. **A1 + A2** — add `.gitignore`, untrack `node_modules`/`build`/`.venv`, fix `package.json`. (Biggest cleanup, zero runtime risk.)
2. **B1 + D2** — single source of truth for `index.html` and PWA assets via a copy/build step.
3. **C1–C4** — remove dead code (decide on Streamlit first).
4. **D1** — service worker update strategy + icon caching.
5. **E1** — event delegation; then **E2, E5** quick cleanups; **E3/E4** optional.

None of A–D change runtime behavior of the live app. E1–E2 should be verified by loading the page and confirming note taps, strum boxes, CAGED, triads, metronome, progression, tab writer, and looper still work.
