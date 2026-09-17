# Instrument samples

The recordings in this folder come from
[tonejs-instruments](https://github.com/nbrosowsky/tonejs-instruments)
by Nicholaus P. Brosowsky, licensed under
[Creative Commons Attribution 3.0 (CC BY 3.0)](https://creativecommons.org/licenses/by/3.0/).

| Folder | Instrument | Original source (per tonejs-instruments) |
|---|---|---|
| `guitar-acoustic/` | Steel-string acoustic guitar | University of Iowa Electronic Music Studios — http://theremin.music.uiowa.edu/ |
| `guitar-electric/` | Electric guitar | Karoryfer Samples — https://www.karoryfer.com/karoryfer-samples |
| `guitar-nylon/` | Nylon-string classical guitar | Freesound, pack 11573 "classicalguitar-multisampled" by quartertone — https://freesound.org |
| `bass-electric/` | Electric bass | Karoryfer Samples — https://www.karoryfer.com/karoryfer-samples |

Changes made for this app: MP3 files only; leading silence trimmed; each note
cut to at most 4.3–6 seconds with a short fade-out; re-encoded as mono 96 kbps.
`manifest.json` lists the notes in each folder and a loudness-matching gain.
`<folder>.js` bundles the same MP3s (base64) so the app can load them even when opened from disk; rebuild with `python3 tools/build_sample_bundles.py`.
