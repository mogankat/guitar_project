"""Guitar Fretboard Visualizer — Streamlit version.

Local run:  streamlit run streamlit_app.py
Streamlit Cloud: set Main file path to streamlit_app.py
"""
import streamlit as st


NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Per-instrument string layout (high → low, matching display order)
GUITAR_STRING_NOTES = ['E', 'B', 'G', 'D', 'A', 'E']
GUITAR_STRING_FREQS = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]  # Hz
BASS_STRING_NOTES   = ['G', 'D', 'A', 'E']
BASS_STRING_FREQS   = [98.00, 73.42, 55.00, 41.20]                      # Hz

MODE_SCALES  = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
NAMED_SCALES = ['Nat Minor', 'Harm Minor', 'Mel Minor', 'Maj Pent', 'Min Pent', 'Maj Blues', 'Min Blues']

SCALE_INTERVALS = {
    'Ionian':     [0, 2, 4, 5, 7, 9, 11],
    'Dorian':     [0, 2, 3, 5, 7, 9, 10],
    'Phrygian':   [0, 1, 3, 5, 7, 8, 10],
    'Lydian':     [0, 2, 4, 6, 7, 9, 11],
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'Aeolian':    [0, 2, 3, 5, 7, 8, 10],
    'Locrian':    [0, 1, 3, 5, 6, 8, 10],
    'Nat Minor':  [0, 2, 3, 5, 7, 8, 10],
    'Harm Minor': [0, 2, 3, 5, 7, 8, 11],
    'Mel Minor':  [0, 2, 3, 5, 7, 9, 11],
    'Maj Pent':   [0, 2, 4, 7, 9],
    'Min Pent':   [0, 3, 5, 7, 10],
    'Maj Blues':  [0, 2, 3, 4, 7, 9],
    'Min Blues':  [0, 3, 5, 6, 7, 10],
}
CHORD_INTERVALS = {
    'Major': [0, 4, 7],
    'Minor': [0, 3, 7],
    'Sus4':  [0, 5, 7],
    'Sus2':  [0, 2, 7],
    'Aug':   [0, 4, 8],
    'Dim':   [0, 3, 6],
    'Add9':  [0, 4, 7, 2],
    '7':     [0, 4, 7, 10],
}
SCALE_DEGREES = {
    'Ionian':     {0:'1', 2:'2', 4:'3', 5:'4', 7:'5', 9:'6', 11:'7'},
    'Dorian':     {0:'1', 2:'2', 3:'b3', 5:'4', 7:'5', 9:'6', 10:'b7'},
    'Phrygian':   {0:'1', 1:'b2', 3:'b3', 5:'4', 7:'5', 8:'b6', 10:'b7'},
    'Lydian':     {0:'1', 2:'2', 4:'3', 6:'#4', 7:'5', 9:'6', 11:'7'},
    'Mixolydian': {0:'1', 2:'2', 4:'3', 5:'4', 7:'5', 9:'6', 10:'b7'},
    'Aeolian':    {0:'1', 2:'2', 3:'b3', 5:'4', 7:'5', 8:'b6', 10:'b7'},
    'Locrian':    {0:'1', 1:'b2', 3:'b3', 5:'4', 6:'b5', 8:'b6', 10:'b7'},
    'Nat Minor':  {0:'1', 2:'2', 3:'b3', 5:'4', 7:'5', 8:'b6', 10:'b7'},
    'Harm Minor': {0:'1', 2:'2', 3:'b3', 5:'4', 7:'5', 8:'b6', 11:'7'},
    'Mel Minor':  {0:'1', 2:'2', 3:'b3', 5:'4', 7:'5', 9:'6', 11:'7'},
    'Maj Pent':   {0:'1', 2:'2', 4:'3', 7:'5', 9:'6'},
    'Min Pent':   {0:'1', 3:'b3', 5:'4', 7:'5', 10:'b7'},
    'Maj Blues':  {0:'1', 2:'2', 3:'b3', 4:'3', 7:'5', 9:'6'},
    'Min Blues':  {0:'1', 3:'b3', 5:'4', 6:'b5', 7:'5', 10:'b7'},
}
CHORD_DEGREES = {
    'Major': {0:'R', 4:'3', 7:'5'},
    'Minor': {0:'R', 3:'b3', 7:'5'},
    'Sus4':  {0:'R', 5:'4', 7:'5'},
    'Sus2':  {0:'R', 2:'2', 7:'5'},
    'Aug':   {0:'R', 4:'3', 8:'#5'},
    'Dim':   {0:'R', 3:'b3', 6:'b5'},
    'Add9':  {0:'R', 4:'3', 7:'5', 2:'9'},
    '7':     {0:'R', 4:'3', 7:'5', 10:'b7'},
}

INTERVAL_COLORS = {
    'R': '#27ae60', '1': '#27ae60',
    '3': '#2980b9', 'b3': '#e74c3c',
    '5': '#2980b9', 'b5': '#e74c3c', '#5': '#e74c3c',
    '9': '#e74c3c', 'b7': '#e74c3c', '7': '#e74c3c',
    '4': '#e74c3c', '2': '#e74c3c', 'b2': '#e74c3c',
    '#4': '#e74c3c', '6': '#e74c3c', 'b6': '#e74c3c',
}
GROUP_COLORS = {0: '#ff6600', 1: '#9900cc', 2: '#0066ff', 3: '#009900'}
BOX_COLORS   = {'C': '#ff6600', 'A': '#9900cc', 'G': '#0066ff', 'E': '#009900', 'D': '#cc0000'}

CAGED_SHAPES = {
    'C': {'pattern': [0, 1, 0, 2, 3, -1], 'root_string': 4, 'root_fret_in_pattern': 3},
    'A': {'pattern': [0, 2, 2, 2, 0, -1], 'root_string': 4, 'root_fret_in_pattern': 0},
    'G': {'pattern': [3, 3, 0, 0, 2,  3], 'root_string': 5, 'root_fret_in_pattern': 3},
    'E': {'pattern': [0, 0, 1, 2, 2,  0], 'root_string': 5, 'root_fret_in_pattern': 0},
    'D': {'pattern': [2, 3, 2, 0, -1,-1], 'root_string': 3, 'root_fret_in_pattern': 0},
}

FRET_W  = 50
STRING_H = 50
ML      = 50
MT      = 50
N_FRETS = 23
SVG_W   = ML + (N_FRETS - 1) * FRET_W + 70   # width never changes

def fx(fret):   return ML + fret * FRET_W
def sy(string): return MT + string * STRING_H

# ── Instrument helpers (read session state, safe to call during rendering) ──

def _is_bass():
    return st.session_state.get('instrument', 'guitar') == 'bass'

def get_string_notes():
    return BASS_STRING_NOTES if _is_bass() else GUITAR_STRING_NOTES

def get_string_freqs():
    return BASS_STRING_FREQS if _is_bass() else GUITAR_STRING_FREQS

def get_n_strings():
    return len(BASS_STRING_NOTES) if _is_bass() else len(GUITAR_STRING_NOTES)

def get_svg_h():
    return MT + (get_n_strings() - 1) * STRING_H + 60


def init_state():
    defaults = {
        'root':        'C',
        'scale':       'Ionian',
        'chord':       'Major',
        'view':        'all',
        'caged':       set(),
        'triad_grps':  set(),
        'hide_notes':  False,
        'label_mode':  'note',
        'dark':        False,
        'instrument':  'guitar',   # 'guitar' or 'bass'
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def note_at(string, fret):
    return NOTES[(NOTES.index(get_string_notes()[string]) + fret) % 12]

def triad_from_context():
    """Return (interval→label dict, required label set) for current scale/chord."""
    s = st.session_state
    if s.view == 'chord':
        degs = CHORD_DEGREES[s.chord]
        return degs, set(degs.values())

    scale    = s.scale
    intervals = SCALE_INTERVALS[scale]
    degs     = SCALE_DEGREES[scale]

    third_int = next((i for i in intervals if degs[i] == '3'), None) or \
                next((i for i in intervals if degs[i] == 'b3'), None)
    fifth_int  = next((i for i in intervals if degs[i] == '5'), None) or \
                next((i for i in intervals if degs[i] in ('#5', 'b5')), None)

    third_lbl = degs[third_int] if third_int is not None else '3'
    fifth_lbl = degs[fifth_int]  if fifth_int is not None else '5'
    if third_int is None: third_int = 4
    if fifth_int is None: fifth_int = 7

    triad_degs = {0: 'R', third_int: third_lbl, fifth_int: fifth_lbl}
    return triad_degs, {'R', third_lbl, fifth_lbl}

def find_triad_voicings(positions, required_labels):
    """Non-overlapping triad voicings per string group, capped before fret 12."""
    n = get_n_strings()
    by_string = {i: [] for i in range(n)}
    for p in positions:
        by_string[p['string']].append(p)

    result = []
    for base in range(n - 2):
        s0, s1, s2 = by_string[base], by_string[base+1], by_string[base+2]
        candidates = []
        for p0 in s0:
            for p1 in s1:
                for p2 in s2:
                    labels = {p0['label'], p1['label'], p2['label']}
                    frets  = [p0['fret'], p1['fret'], p2['fret']]
                    if labels == required_labels and max(frets) - min(frets) <= 4:
                        candidates.append((min(frets), max(frets), [p0, p1, p2]))
        candidates.sort()
        last_max = -1
        for min_f, max_f, voicing in candidates:
            if min_f < 12 and min_f > last_max:
                result.append((base, voicing))
                last_max = max_f
    return result


def svg_circle(x, y, color, text, freq=None):
    if freq is not None:
        oc = f' onclick="playNote({freq:.4f})" style="cursor:pointer"'
    else:
        oc = ''
    return (
        f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" stroke="{color}"{oc}/>'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" font-family="Arial" '
        f'font-size="10" font-weight="bold" fill="white" pointer-events="none">{text}</text>'
    )

def svg_rect(x1, y1, x2, y2, color, stroke_w=2, onclick_freqs=None):
    if onclick_freqs is not None:
        extra = (f' fill="transparent" onclick="playStrum({onclick_freqs},30)" '
                 f'style="cursor:pointer"')
    else:
        extra = ' fill="none"'
    return (
        f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" '
        f'stroke="{color}" stroke-width="{stroke_w}"{extra}/>'
    )


def render_note_circles(degrees_dict):
    s = st.session_state
    root_idx = NOTES.index(s.root)
    parts = []
    for string in range(get_n_strings()):
        for fret in range(N_FRETS):
            ni = NOTES.index(note_at(string, fret))
            if ni in degrees_dict:
                label   = degrees_dict[ni]
                color   = INTERVAL_COLORS.get(label, '#e74c3c')
                display = NOTES[ni] if s.label_mode == 'note' else label
                freq = get_string_freqs()[string] * (2 ** (fret / 12))
                parts.append(svg_circle(fx(fret), sy(string), color, display, freq))
    return parts

def render_base():
    s = st.session_state
    root_idx = NOTES.index(s.root)

    if s.view == 'all':
        sfreqs = get_string_freqs()
        parts = []
        for string in range(get_n_strings()):
            for fret in range(N_FRETS):
                freq = sfreqs[string] * (2 ** (fret / 12))
                parts.append(svg_circle(fx(fret), sy(string), '#555555', NOTES[NOTES.index(note_at(string, fret))], freq))
        return parts

    if s.view == 'root':
        return render_note_circles({root_idx: 'R'})

    if s.view == 'scale':
        degs = {(root_idx + i) % 12: SCALE_DEGREES[s.scale][i]
                for i in SCALE_INTERVALS[s.scale]}
    else:
        degs = {(root_idx + i) % 12: CHORD_DEGREES[s.chord][i]
                for i in CHORD_INTERVALS[s.chord]}
    return render_note_circles(degs)

def get_active_voicings():
    s = st.session_state
    if s.view in ('all', 'root'):
        return []
    root_idx = NOTES.index(s.root)
    triad_degs, required = triad_from_context()
    d = {(root_idx + i) % 12: triad_degs[i] for i in triad_degs}

    all_pos = [
        {'string': st_idx, 'fret': fr,
         'x': fx(fr), 'y': sy(st_idx),
         'label': d[NOTES.index(note_at(st_idx, fr))]}
        for st_idx in range(get_n_strings())
        for fr in range(N_FRETS)
        if NOTES.index(note_at(st_idx, fr)) in d
    ]
    return [(g, v) for g, v in find_triad_voicings(all_pos, required)
            if g in s.triad_grps]

def get_strum_freqs():
    """One frequency per string, low-string first (strum order), for the current display."""
    s = st.session_state
    n = get_n_strings()
    sfreqs = get_string_freqs()

    if s.view == 'all':
        return [round(f, 4) for f in reversed(sfreqs)]  # open strings, low first

    if s.view == 'root':
        root_ni = NOTES.index(s.root)
        freqs = []
        for string in range(n - 1, -1, -1):
            for fret in range(N_FRETS):
                if NOTES.index(note_at(string, fret)) == root_ni:
                    freqs.append(round(sfreqs[string] * (2 ** (fret / 12)), 4))
                    break
        return freqs

    # When triads-only mode: use the active voicing positions
    if s.hide_notes and s.triad_grps:
        by_string = {}
        for _, voicing in get_active_voicings():
            for p in voicing:
                si, fr = p['string'], p['fret']
                if si not in by_string or fr < by_string[si]:
                    by_string[si] = fr
        return [round(sfreqs[si] * (2 ** (fr / 12)), 4)
                for si, fr in sorted(by_string.items(), reverse=True)]

    # Chord / scale view: pick lowest highlighted fret on each string
    root_idx = NOTES.index(s.root)
    if s.view == 'scale':
        active_ni = {(root_idx + i) % 12 for i in SCALE_INTERVALS[s.scale]}
    else:
        active_ni = {(root_idx + i) % 12 for i in CHORD_INTERVALS[s.chord]}

    freqs = []
    for string in range(n - 1, -1, -1):   # low string first
        for fret in range(N_FRETS):
            if NOTES.index(note_at(string, fret)) in active_ni:
                freqs.append(round(sfreqs[string] * (2 ** (fret / 12)), 4))
                break
    return freqs

def render_triad_boxes():
    sfreqs = get_string_freqs()
    parts = []
    for group, voicing in get_active_voicings():
        xs = [p['x'] for p in voicing]
        ys = [p['y'] for p in voicing]
        # low string (highest index) first → strum order
        vfreqs = [round(sfreqs[p['string']] * (2 ** (p['fret'] / 12)), 4)
                  for p in sorted(voicing, key=lambda x: -x['string'])]
        parts.append(svg_rect(min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                              GROUP_COLORS[group], 3, vfreqs))
    return parts

def render_triads_only():
    s = st.session_state
    sfreqs = get_string_freqs()
    parts = []
    for group, voicing in get_active_voicings():
        xs = [p['x'] for p in voicing]
        ys = [p['y'] for p in voicing]
        # low string (highest index) first → strum order
        vfreqs = [round(sfreqs[p['string']] * (2 ** (p['fret'] / 12)), 4)
                  for p in sorted(voicing, key=lambda x: -x['string'])]
        # rect drawn FIRST so circles render on top and remain individually clickable
        parts.append(svg_rect(min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                              GROUP_COLORS[group], 3, vfreqs))
        for p in voicing:
            color   = INTERVAL_COLORS.get(p['label'], '#e74c3c')
            display = note_at(p['string'], p['fret']) if s.label_mode == 'note' else p['label']
            freq = sfreqs[p['string']] * (2 ** (p['fret'] / 12))
            parts.append(svg_circle(p['x'], p['y'], color, display, freq))
    return parts

def render_caged():
    if _is_bass():
        return []
    s = st.session_state
    root_idx  = NOTES.index(s.root)
    chord_degs = CHORD_DEGREES[s.chord]
    parts = []

    for shape_name, shape in CAGED_SHAPES.items():
        if shape_name not in s.caged:
            continue
        open_ni   = NOTES.index(GUITAR_STRING_NOTES[shape['root_string']])
        base_fret = (root_idx - open_ni) % 12 - shape['root_fret_in_pattern']
        if base_fret < 0:
            base_fret += 12
        if base_fret > 22:
            continue

        circle_parts = []
        frets_drawn, strs_drawn = [], []
        for si, offset in enumerate(shape['pattern']):
            if offset == -1:
                continue
            exp_fret = base_fret + offset
            if exp_fret > 22:
                continue
            open_sn = NOTES.index(GUITAR_STRING_NOTES[si])
            best_fret, best_label, best_dist = None, None, 999
            for interval, label in chord_degs.items():
                target   = (root_idx + interval) % 12
                base_pos = (target - open_sn) % 12
                for oct in range(-1, 3):
                    f = base_pos + oct * 12
                    if 0 <= f <= 22:
                        d = abs(f - exp_fret)
                        if d < best_dist:
                            best_dist, best_fret, best_label = d, f, label
            if best_fret is None or best_dist > 3:
                continue
            ni      = NOTES.index(note_at(si, best_fret))
            color   = INTERVAL_COLORS.get(best_label, '#888888')
            display = NOTES[ni] if s.label_mode == 'note' else best_label
            freq = GUITAR_STRING_FREQS[si] * (2 ** (best_fret / 12))
            circle_parts.append(svg_circle(fx(best_fret), sy(si), color, display, freq))
            frets_drawn.append(best_fret)
            strs_drawn.append(si)

        if frets_drawn:
            xs  = [fx(f) for f in frets_drawn]
            ys  = [sy(si) for si in strs_drawn]
            bc  = BOX_COLORS[shape_name]
            # low string (highest index) first → strum order
            pairs = sorted(zip(strs_drawn, frets_drawn), key=lambda x: -x[0])
            shape_freqs = [round(GUITAR_STRING_FREQS[si] * (2 ** (fr / 12)), 4)
                           for si, fr in pairs]
            # rect drawn FIRST so circles render on top and remain individually clickable
            parts.append(svg_rect(min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                                  bc, 2, shape_freqs))
            parts.extend(circle_parts)
            parts.append(
                f'<text x="{min(xs)-14}" y="{min(ys)-16}" font-family="Arial" '
                f'font-size="9" font-weight="bold" fill="{bc}">{shape_name}</text>'
            )
    return parts


def build_svg():
    s = st.session_state
    dark = s.dark
    bg   = '#1e1e1e' if dark else 'white'
    sc   = '#daa520' if dark else '#8B4513'
    fc   = '#ffffff' if dark else '#444444'
    mc   = '#ffffff' if dark else '#444444'
    tc   = '#ffffff' if dark else '#444444'

    cur_ns = get_n_strings()
    cur_sn = get_string_notes()
    svg_h  = get_svg_h()
    cy_mid = sy(0) + (cur_ns - 1) * STRING_H // 2   # vertical center of fretboard

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{svg_h}" '
         f'style="background:{bg};display:block">']

    for i in range(cur_ns):
        y = sy(i)
        p.append(f'<line x1="{fx(0)}" y1="{y}" x2="{fx(N_FRETS-1)}" y2="{y}" '
                 f'stroke="{sc}" stroke-width="2"/>')

    for i in range(N_FRETS):
        x = fx(i)
        w = 3 if i == 0 else 1
        p.append(f'<line x1="{x}" y1="{sy(0)}" x2="{x}" y2="{sy(cur_ns-1)}" '
                 f'stroke="{fc}" stroke-width="{w}"/>')

    for fret in [3, 5, 7, 9, 15, 17, 19, 21]:
        p.append(f'<circle cx="{fx(fret)}" cy="{cy_mid}" r="5" fill="{mc}"/>')
    p.append(f'<circle cx="{fx(12)}" cy="{cy_mid - 10}" r="5" fill="{mc}"/>')
    p.append(f'<circle cx="{fx(12)}" cy="{cy_mid + 10}" r="5" fill="{mc}"/>')

    for i, note in enumerate(cur_sn):
        p.append(f'<text x="25" y="{sy(i)+5}" text-anchor="middle" '
                 f'font-family="Arial" font-size="12" fill="{tc}">{note}</text>')

    yn = sy(cur_ns - 1) + 25
    for i in range(N_FRETS):
        p.append(f'<text x="{fx(i)}" y="{yn}" text-anchor="middle" '
                 f'font-family="Arial" font-size="10" fill="{tc}">{i}</text>')

    has_triads = bool(s.triad_grps)
    if s.caged:
        p.extend(render_caged())
    elif s.hide_notes and has_triads:
        p.extend(render_triads_only())
    else:
        p.extend(render_base())
        if has_triads:
            p.extend(render_triad_boxes())

    p.append('</svg>')
    return '\n'.join(p)


_KS_JS = """<script>
var _ksCtx=null;
function _getCtx(){
  if(!_ksCtx||_ksCtx.state==='closed')
    _ksCtx=new(window.AudioContext||window.webkitAudioContext)();
  if(_ksCtx.state==='suspended')_ksCtx.resume();
  return _ksCtx;
}
function playNote(freq){
  var ctx=_getCtx(),sr=ctx.sampleRate;
  var N=Math.max(2,Math.round(sr/freq));
  var ns=Math.round(sr*2.5);
  var buf=new Float32Array(N);
  for(var i=0;i<N;i++)buf[i]=Math.random()*2-1;
  var ab=ctx.createBuffer(1,ns,sr);
  var d=ab.getChannelData(0);
  var decay=freq<300?0.998:0.996;
  for(var i=0;i<ns;i++){
    var j=i%N;
    d[i]=buf[j];
    buf[j]=decay*0.5*(buf[j]+buf[(i+1)%N]);
  }
  for(var i=0;i<ns;i++)d[i]=Math.tanh(d[i]*1.5)*0.65;
  var src=ctx.createBufferSource();
  src.buffer=ab;src.connect(ctx.destination);src.start();
}
function playStrum(freqs,delay){
  freqs.forEach(function(f,i){setTimeout(function(){playNote(f);},i*delay);});
}
</script>"""

def build_fretboard_html():
    s = st.session_state
    dark = s.dark
    bg     = '#1e1e1e' if dark else 'white'
    btn_bg = '#444444' if dark else '#eeeeee'
    btn_fg = '#ffffff' if dark else '#222222'

    freqs = get_strum_freqs()
    btn_style = (f'padding:5px 16px;font-size:13px;cursor:pointer;'
                 f'background:{btn_bg};color:{btn_fg};'
                 f'border:1px solid #888;border-radius:4px;margin-right:8px')
    buttons = (
        f'<div style="padding:6px 0 2px {ML}px">'
        f'<button onclick="playStrum({freqs},30)" style="{btn_style}">&#9834; Strum</button>'
        f'<button onclick="playStrum({freqs},0)"  style="{btn_style}">&#9835; Chord</button>'
        f'</div>'
    )
    return (
        f'<!DOCTYPE html><html><head>'
        f'<style>body{{margin:0;background:{bg};overflow-x:auto;overflow-y:hidden}}</style>'
        f'</head><body>{build_svg()}{buttons}{_KS_JS}</body></html>'
    )


def btn(label, key, active=False, use_width=True):
    """Shortcut: returns True if clicked; type=primary when active."""
    t = "primary" if active else "secondary"
    return st.button(label, key=key, type=t, use_container_width=use_width)

def main():
    st.set_page_config(page_title="Guitar Fretboard", layout="wide")
    init_state()
    s = st.session_state

    st.title("Guitar Fretboard Visualizer")

    st.components.v1.html(build_fretboard_html(), height=get_svg_h() + 60, scrolling=False)

    st.divider()

    # ── Instrument ────────────────────────────────────────────────────────────
    inst_cols = st.columns([1, 1, 1])
    inst_cols[0].markdown("**Instrument**")
    if inst_cols[1].button("Guitar", key="inst_guitar",
                           type="primary" if not _is_bass() else "secondary",
                           use_container_width=True):
        if _is_bass():
            s.instrument = 'guitar'
            s.triad_grps = set()
            st.rerun()
    if inst_cols[2].button("Bass", key="inst_bass",
                           type="primary" if _is_bass() else "secondary",
                           use_container_width=True):
        if not _is_bass():
            s.instrument = 'bass'
            s.caged      = set()
            s.triad_grps = set()
            st.rerun()

    # ── Root ──────────────────────────────────────────────────────────────────
    root_cols = st.columns([1] + [1] * 12)
    root_cols[0].markdown("**Root**")
    for i, note in enumerate(NOTES):
        active_root = note == s.root and s.view in ('root', 'scale', 'chord')
        if root_cols[i + 1].button(note, key=f"r_{note}",
                                   type="primary" if active_root else "secondary",
                                   use_container_width=True):
            if s.view == 'all':
                s.root = note
                s.view = 'root'
            elif s.view == 'root' and s.root == note:
                s.view = 'all'
            else:
                s.root = note
            st.rerun()

    # ── Modes ─────────────────────────────────────────────────────────────────
    mode_cols = st.columns([1] + [1] * len(MODE_SCALES))
    mode_cols[0].markdown("**Modes**")
    for i, scale in enumerate(MODE_SCALES):
        active = s.view == 'scale' and s.scale == scale
        if mode_cols[i + 1].button(scale, key=f"m_{scale}",
                                   type="primary" if active else "secondary",
                                   use_container_width=True):
            if active:
                s.view = 'all'
                s.triad_grps = set()
                s.caged = set()
            else:
                s.scale = scale
                s.view  = 'scale'
                s.caged = set()
            st.rerun()

    # ── Scales ────────────────────────────────────────────────────────────────
    scale_cols = st.columns([1] + [1] * len(NAMED_SCALES))
    scale_cols[0].markdown("**Scales**")
    for i, scale in enumerate(NAMED_SCALES):
        active = s.view == 'scale' and s.scale == scale
        if scale_cols[i + 1].button(scale, key=f"s_{scale}",
                                    type="primary" if active else "secondary",
                                    use_container_width=True):
            if active:
                s.view = 'all'
                s.triad_grps = set()
                s.caged = set()
            else:
                s.scale = scale
                s.view  = 'scale'
                s.caged = set()
            st.rerun()

    # ── Chords ────────────────────────────────────────────────────────────────
    chord_list = list(CHORD_INTERVALS.keys())
    chord_cols = st.columns([1] + [1] * len(chord_list))
    chord_cols[0].markdown("**Chords**")
    for i, chord in enumerate(chord_list):
        active = s.view == 'chord' and s.chord == chord
        if chord_cols[i + 1].button(chord, key=f"c_{chord}",
                                    type="primary" if active else "secondary",
                                    use_container_width=True):
            if active:
                s.view = 'all'
                s.triad_grps = set()
            else:
                s.chord = chord
                s.view  = 'chord'
            st.rerun()

    # ── CAGED (guitar only) ───────────────────────────────────────────────────
    if not _is_bass():
        all_shapes  = set(CAGED_SHAPES.keys())
        shape_names = list(CAGED_SHAPES.keys()) + ['All']
        caged_cols  = st.columns([1] + [1] * len(shape_names))
        caged_cols[0].markdown("**CAGED**")
        for i, shape in enumerate(shape_names):
            label  = "All Shapes" if shape == 'All' else f"{shape} Shape"
            active = (s.caged == all_shapes) if shape == 'All' else (shape in s.caged)
            if caged_cols[i + 1].button(label, key=f"cg_{shape}",
                                        type="primary" if active else "secondary",
                                        use_container_width=True):
                if shape == 'All':
                    s.caged = set() if s.caged == all_shapes else set(all_shapes)
                else:
                    s.caged = (s.caged - {shape}) if shape in s.caged else (s.caged | {shape})
                st.rerun()

    # ── Triads ────────────────────────────────────────────────────────────────
    # Bass: ordered low→high (D-A-E first); guitar: high→low (e-B-G first)
    if _is_bass():
        group_labels = {0: 'G-D-A', 1: 'D-A-E'}
    else:
        group_labels = {0: 'e-B-G', 1: 'B-G-D', 2: 'G-D-A', 3: 'D-A-E'}
    triad_cols = st.columns([1, 1.2] + [1] * len(group_labels))
    triad_cols[0].markdown("**Triads**")
    hide_label = "Show Notes" if s.hide_notes else "Hide Notes"
    if triad_cols[1].button(hide_label, key="btn_hide_notes", use_container_width=True):
        s.hide_notes = not s.hide_notes
        st.rerun()

    for col_i, (gid, glabel) in enumerate(group_labels.items(), start=2):
        active = gid in s.triad_grps
        if triad_cols[col_i].button(glabel, key=f"tg_{gid}",
                                    type="primary" if active else "secondary",
                                    use_container_width=True):
            if gid in s.triad_grps:
                s.triad_grps = s.triad_grps - {gid}
                if not s.triad_grps:
                    s.hide_notes = False
            else:
                s.triad_grps = s.triad_grps | {gid}
            st.rerun()


    st.divider()
    util_cols = st.columns(4)
    lbl_text = "Show Intervals" if s.label_mode == 'note' else "Show Note Names"
    if util_cols[0].button(lbl_text, key="lbl", use_container_width=True):
        s.label_mode = 'interval' if s.label_mode == 'note' else 'note'
        st.rerun()

    dark_text = "Light Mode" if s.dark else "Dark Mode"
    if util_cols[1].button(dark_text, key="btn_dark", use_container_width=True):
        s.dark = not s.dark
        st.rerun()

    if util_cols[2].button("Clear", key="clear", use_container_width=True):
        s.caged      = set()
        s.triad_grps = set()
        s.hide_notes = False
        s.view       = 'all'
        st.rerun()

main()
