"""Guitar Fretboard Visualizer — Streamlit version.

Local run:  streamlit run streamlit_app.py
Streamlit Cloud: set Main file path to streamlit_app.py
"""
import streamlit as st


NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

GUITAR_STRING_NOTES = ['E', 'B', 'G', 'D', 'A', 'E']
GUITAR_STRING_FREQS = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]  
BASS_STRING_NOTES   = ['G', 'D', 'A', 'E']
BASS_STRING_FREQS   = [98.00, 73.42, 55.00, 41.20]                      

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

FRET_W  = 75
STRING_H = 50
ML      = 50
MT      = 50
N_FRETS = 15
SVG_W   = ML + (N_FRETS - 1) * FRET_W + 70   

def fx(fret):   return ML + fret * FRET_W
def sy(string): return MT + string * STRING_H



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
        'instrument':  'guitar',   
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
            if min_f < N_FRETS and min_f > last_max:
                result.append((base, voicing))
                last_max = max_f
    return result


def svg_circle(x, y, color, text, freq=None, string=None, fret=None):
    if freq is not None:
        if string is not None and fret is not None:
            oc = f' onclick="playNote({freq:.4f},{string},{fret})" style="cursor:pointer"'
        else:
            oc = f' onclick="playNote({freq:.4f})" style="cursor:pointer"'
    else:
        oc = ''
    return (
        f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" stroke="{color}"{oc}/>'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" font-family="Arial" '
        f'font-size="10" font-weight="bold" fill="white" pointer-events="none">{text}</text>'
    )

def svg_rect(x1, y1, x2, y2, color, stroke_w=2, onclick_notes=None):
    if onclick_notes is not None:
        extra = (f' fill="transparent" onclick="playStrum({onclick_notes},30)" '
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
                parts.append(svg_circle(fx(fret), sy(string), color, display, freq, string, fret))
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
                parts.append(svg_circle(fx(fret), sy(string), '#555555', NOTES[NOTES.index(note_at(string, fret))], freq, string, fret))
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

def get_strum_notes():
    """[[freq, string_idx, fret], ...] low-string first, for the current display."""
    s = st.session_state
    n = get_n_strings()
    sfreqs = get_string_freqs()

    if s.view == 'all':
        
        return [[round(sfreqs[si], 4), si, 0] for si in range(n - 1, -1, -1)]

    if s.view == 'root':
        root_ni = NOTES.index(s.root)
        notes = []
        for string in range(n - 1, -1, -1):
            for fret in range(N_FRETS):
                if NOTES.index(note_at(string, fret)) == root_ni:
                    notes.append([round(sfreqs[string] * (2 ** (fret / 12)), 4), string, fret])
                    break
        return notes

    
    if s.hide_notes and s.triad_grps:
        by_string = {}
        for _, voicing in get_active_voicings():
            for p in voicing:
                si, fr = p['string'], p['fret']
                if si not in by_string or fr < by_string[si]:
                    by_string[si] = fr
        return [[round(sfreqs[si] * (2 ** (fr / 12)), 4), si, fr]
                for si, fr in sorted(by_string.items(), reverse=True)]

    
    root_idx = NOTES.index(s.root)
    if s.view == 'scale':
        active_ni = {(root_idx + i) % 12 for i in SCALE_INTERVALS[s.scale]}
    else:
        active_ni = {(root_idx + i) % 12 for i in CHORD_INTERVALS[s.chord]}

    notes = []
    for string in range(n - 1, -1, -1):   
        for fret in range(N_FRETS):
            if NOTES.index(note_at(string, fret)) in active_ni:
                notes.append([round(sfreqs[string] * (2 ** (fret / 12)), 4), string, fret])
                break
    return notes

def render_triad_boxes():
    sfreqs = get_string_freqs()
    parts = []
    for group, voicing in get_active_voicings():
        xs = [p['x'] for p in voicing]
        ys = [p['y'] for p in voicing]
        
        vnotes = [[round(sfreqs[p['string']] * (2 ** (p['fret'] / 12)), 4), p['string'], p['fret']]
                  for p in sorted(voicing, key=lambda x: -x['string'])]
        parts.append(svg_rect(min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                              GROUP_COLORS[group], 3, vnotes))
    return parts

def render_triads_only():
    s = st.session_state
    sfreqs = get_string_freqs()
    parts = []
    for group, voicing in get_active_voicings():
        xs = [p['x'] for p in voicing]
        ys = [p['y'] for p in voicing]
        vnotes = [[round(sfreqs[p['string']] * (2 ** (p['fret'] / 12)), 4), p['string'], p['fret']]
                  for p in sorted(voicing, key=lambda x: -x['string'])]
        
        parts.append(svg_rect(min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                              GROUP_COLORS[group], 3, vnotes))
        for p in voicing:
            color   = INTERVAL_COLORS.get(p['label'], '#e74c3c')
            display = note_at(p['string'], p['fret']) if s.label_mode == 'note' else p['label']
            freq = sfreqs[p['string']] * (2 ** (p['fret'] / 12))
            parts.append(svg_circle(p['x'], p['y'], color, display, freq, p['string'], p['fret']))
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
        if base_fret >= N_FRETS:
            continue

        circle_parts = []
        frets_drawn, strs_drawn = [], []
        for si, offset in enumerate(shape['pattern']):
            if offset == -1:
                continue
            exp_fret = base_fret + offset
            if exp_fret >= N_FRETS:
                continue
            open_sn = NOTES.index(GUITAR_STRING_NOTES[si])
            best_fret, best_label, best_dist = None, None, 999
            for interval, label in chord_degs.items():
                target   = (root_idx + interval) % 12
                base_pos = (target - open_sn) % 12
                for oct in range(-1, 3):
                    f = base_pos + oct * 12
                    if 0 <= f < N_FRETS:
                        d = abs(f - exp_fret)
                        if d < best_dist:
                            best_dist, best_fret, best_label = d, f, label
            if best_fret is None or best_dist > 3:
                continue
            ni      = NOTES.index(note_at(si, best_fret))
            color   = INTERVAL_COLORS.get(best_label, '#888888')
            display = NOTES[ni] if s.label_mode == 'note' else best_label
            freq = GUITAR_STRING_FREQS[si] * (2 ** (best_fret / 12))
            circle_parts.append(svg_circle(fx(best_fret), sy(si), color, display, freq, si, best_fret))
            frets_drawn.append(best_fret)
            strs_drawn.append(si)

        if frets_drawn:
            xs  = [fx(f) for f in frets_drawn]
            ys  = [sy(si) for si in strs_drawn]
            bc  = BOX_COLORS[shape_name]
            
            pairs = sorted(zip(strs_drawn, frets_drawn), key=lambda x: -x[0])
            shape_notes = [[round(GUITAR_STRING_FREQS[si] * (2 ** (fr / 12)), 4), si, fr]
                           for si, fr in pairs]
            
            parts.append(svg_rect(min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                                  bc, 2, shape_notes))
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
    cy_mid = sy(0) + (cur_ns - 1) * STRING_H // 2   

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
        if fret < N_FRETS:
            p.append(f'<circle cx="{fx(fret)}" cy="{cy_mid}" r="5" fill="{mc}"/>')
    if 12 < N_FRETS:
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
function playNote(freq,si,fr){
  if(_lickRec&&si!=null&&fr!=null)
    _lickNotes.push({f:freq,t:Date.now()-_lickT0,s:si,fr:fr});
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
function playStrum(notes,delay){
  notes.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],n[2]);},i*delay);});
}

var _lickRec=false,_lickT0=0,_lickNotes=[],_savedLicks={};

function _loadLicks(){
  try{_savedLicks=JSON.parse(localStorage.getItem('guitar_licks')||'{}');}
  catch(e){_savedLicks={};}
  _renderLickList();
}
function _storeLicks(){localStorage.setItem('guitar_licks',JSON.stringify(_savedLicks));}

function toggleRecording(){
  var btn=document.getElementById('rec-btn');
  var sa=document.getElementById('save-area');
  if(_lickRec){
    _lickRec=false;
    btn.innerHTML='&#9210; Record';
    btn.style.background=_btnBg;btn.style.color=_btnFg;
    if(_lickNotes.length>0) sa.style.display='flex';
  }else{
    _lickRec=true;_lickT0=Date.now();_lickNotes=[];
    btn.innerHTML='&#9209; Stop';
    btn.style.background='#cc0000';btn.style.color='white';
    sa.style.display='none';
  }
}
function saveLick(){
  var name=document.getElementById('lick-name').value.trim();
  if(!name){alert('Enter a name for the lick');return;}
  _savedLicks[name]={ns:_nStrings,notes:_lickNotes.slice()};
  _storeLicks();_renderLickList();
  document.getElementById('lick-name').value='';
  document.getElementById('save-area').style.display='none';
}
function deleteLick(name){
  delete _savedLicks[name];_storeLicks();_renderLickList();
}
function playLick(name){
  var lick=_savedLicks[name];
  if(!lick)return;
  var notes=lick.notes||lick;
  if(!notes.length)return;
  notes.forEach(function(n){
    var freq=n.f!=null?n.f:n.freq;
    setTimeout(function(){playNote(freq,n.s,n.fr);},n.t);
  });
}

function _genTab(lick){
  var notes=lick.notes||lick;
  if(!notes||!notes.length)return null;
  var valid=notes.filter(function(n){return n.s!=null&&n.fr!=null;});
  if(!valid.length)return null;

  var ns=lick.ns||(valid.some(function(n){return n.s>3;})?6:4);
  var labels=ns===4?['G','D','A','E']:['e','B','G','D','A','E'];

  valid.sort(function(a,b){return a.t-b.t;});
  var cols=[];
  valid.forEach(function(n){
    var last=cols.length?cols[cols.length-1]:null;
    if(last&&n.t-last[last.length-1].t<100)last.push(n);
    else cols.push([n]);
  });

  var rows=labels.map(function(){return '';});
  cols.forEach(function(col){
    var byStr={};
    col.forEach(function(n){byStr[n.s]=n.fr;});
    var maxW=1;
    for(var i=0;i<ns;i++)
      if(byStr[i]!=null)maxW=Math.max(maxW,String(byStr[i]).length);
    for(var i=0;i<ns;i++){
      if(byStr[i]!=null){
        var s=String(byStr[i]);
        rows[i]+='-'+s+new Array(maxW-s.length+1).join('-');
      }else{
        rows[i]+=new Array(maxW+2).join('-');
      }
    }
  });

  return labels.map(function(l,i){return l+'|'+rows[i]+'-|';}).join('\\n');
}

function _renderLickList(){
  var el=document.getElementById('lick-list');if(!el)return;
  var names=Object.keys(_savedLicks);
  if(!names.length){
    el.innerHTML='<span style="color:#888;font-size:12px;font-style:italic">No licks saved yet \u2014 record one above</span>';
    return;
  }
  el.innerHTML=names.map(function(n){
    var esc=n.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
    var tab=_genTab(_savedLicks[n]);
    var tabHtml=tab
      ?'<pre style="margin:3px 0 0;font-size:11px;line-height:1.35;color:'+_lblFg+';font-family:monospace">'+tab+'</pre>'
      :'';
    return '<div style="margin:6px 0 8px">'+
      '<div style="display:flex;align-items:center;gap:5px">'+
      '<button onclick="playLick(&quot;'+esc+'&quot;)" style="padding:3px 12px;font-size:12px;cursor:pointer;border:1px solid #888;border-radius:3px;background:'+_btnBg+';color:'+_btnFg+'">&#9654; '+n+'</button>'+
      '<button onclick="deleteLick(&quot;'+esc+'&quot;)" title="Delete" style="padding:3px 8px;font-size:12px;cursor:pointer;border:1px solid #888;border-radius:3px;background:'+_btnBg+';color:#e05050;">&#10005;</button>'+
      '</div>'+tabHtml+'</div>';
  }).join('');
}
var _metro={running:false,bpm:120,beats:4,tick:0,timeout:null};
function _metroTick(){
  if(!_metro.running)return;
  var ctx=_getCtx();
  var isAccent=_metro.tick%_metro.beats===0;
  _metro.tick++;
  var osc=ctx.createOscillator();var gain=ctx.createGain();
  osc.type='triangle';osc.frequency.value=isAccent?1000:750;
  osc.connect(gain);gain.connect(ctx.destination);
  gain.gain.setValueAtTime(isAccent?0.4:0.25,ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.06);
  osc.start(ctx.currentTime);osc.stop(ctx.currentTime+0.08);
  _metro.timeout=setTimeout(_metroTick,60000/_metro.bpm);
}
function toggleMetronome(){
  var btn=document.getElementById('metro-btn');
  if(_metro.running){
    _metro.running=false;clearTimeout(_metro.timeout);
    btn.style.background=_btnBg;btn.style.color=_btnFg;
  }else{
    _metro.running=true;_metro.tick=0;
    _metro.bpm=parseInt(document.getElementById('metro-bpm').value)||120;
    _metro.beats=parseInt(document.getElementById('metro-top').value)||4;
    _metroTick();
    btn.style.background='#0066cc';btn.style.color='white';
  }
}
function _metroUpdate(){
  if(_metro.running){
    _metro.bpm=parseInt(document.getElementById('metro-bpm').value)||120;
    _metro.beats=parseInt(document.getElementById('metro-top').value)||4;
  }
}

var _NOTES_JS=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];

var _CHORD_IVALS={

  '':[0,4,7],'major':[0,4,7],'maj':[0,4,7],'m':[0,3,7],

  'minor':[0,3,7],'min':[0,3,7],

  '5':[0,7],

  '7':[0,4,7,10],'dominant7':[0,4,7,10],'dom7':[0,4,7,10],
  'maj7':[0,4,7,11],'major7':[0,4,7,11],
  'm7':[0,3,7,10],'minor7':[0,3,7,10],'min7':[0,3,7,10],
  'minormajor7':[0,3,7,11],'mm7':[0,3,7,11],

  'sus2':[0,2,7],'suspended2':[0,2,7],
  'sus4':[0,5,7],'suspended4':[0,5,7],

  'aug':[0,4,8],'augmented':[0,4,8],'+':[0,4,8],
  'dim':[0,3,6],'diminished':[0,3,6],'o':[0,3,6],
  'dim7':[0,3,6,9],'diminished7':[0,3,6,9],'o7':[0,3,6,9],
  'halfdim':[0,3,6,10],'halfdiminished':[0,3,6,10],'m7b5':[0,3,6,10],

  'add9':[0,4,7,2],'addnine':[0,4,7,2],
  'add2':[0,2,4,7],
  '9':[0,4,7,10,2],'dominant9':[0,4,7,10,2],
  'm9':[0,3,7,10,2],'minor9':[0,3,7,10,2],
  'maj9':[0,4,7,11,2],'major9':[0,4,7,11,2],
  '11':[0,4,7,10,2,5],'13':[0,4,7,10,2,5,9]
};

function _parseChord(sym){
  sym=sym.trim();if(!sym)return null;
  var minFret=0;
  var fp=sym.match(/@(\\d+)/);
  if(fp){minFret=parseInt(fp[1]);sym=sym.replace(/@\\d+/,'').trim();}
  var m=sym.match(/^([A-G][b#]?)\\s*(.*)/);if(!m)return null;
  var rn=m[1],qual=m[2].trim();
  var fm={'Cb':'B','Db':'C#','Eb':'D#','Fb':'E','Gb':'F#','Ab':'G#','Bb':'A#'};
  if(fm[rn])rn=fm[rn];
  var ri=_NOTES_JS.indexOf(rn);if(ri===-1)return null;
  var norm=qual.toLowerCase().replace(/\\s+/g,'');
  var iv=_CHORD_IVALS[qual]||_CHORD_IVALS[qual.toLowerCase()]||_CHORD_IVALS[norm]||[0,4,7];
  return {root:ri,ivals:iv,minFret:minFret};
}
function _chordToNotes(chord){
  var minFret=chord.minFret||0;
  var ns={};chord.ivals.forEach(function(i){ns[(chord.root+i)%12]=true;});
  var notes=[];
  for(var si=_nStrings-1;si>=0;si--){
    var on=_NOTES_JS.indexOf(_STRING_NOTES[si]);
    for(var fr=minFret;fr<_N_FRETS;fr++){
      if(ns[(on+fr)%12]){
        notes.push([Math.round(_STRING_FREQS[si]*Math.pow(2,fr/12)*10000)/10000,si,fr]);
        break;
      }
    }
  }
  return notes;
}
var _progRunning=false,_progTimeout=null;
function playProgression(){
  var input=document.getElementById('chord-prog').value.trim();
  var syms=input.indexOf(',')>=0
    ? input.split(/,/).map(function(s){return s.trim();}).filter(Boolean)
    : input.split(/\\s+/).filter(Boolean);
  if(!syms.length)return;
  var btn=document.getElementById('prog-btn');
  if(_progRunning){
    _progRunning=false;clearTimeout(_progTimeout);
    btn.textContent='▶ Play';btn.style.background=_btnBg;btn.style.color=_btnFg;
    return;
  }
  _progRunning=true;
  btn.textContent='⏹ Stop';btn.style.background='#cc0000';btn.style.color='white';
  var bpm=parseInt(document.getElementById('metro-bpm').value)||120;
  var bpc=parseInt(document.getElementById('prog-beats').value)||4;
  var mspc=Math.round(60000/bpm*bpc);
  var idx=0;
  (function next(){
    if(!_progRunning)return;
    var c=_parseChord(syms[idx]);
    if(c)playStrum(_chordToNotes(c),30);
    idx++;
    if(idx>=syms.length) idx=0;
    _progTimeout=setTimeout(next,mspc);
  })();
}
window.addEventListener('load',_loadLicks);
</script>"""

def build_fretboard_html():
    s = st.session_state
    dark   = s.dark
    bg     = '#1e1e1e' if dark else 'white'
    btn_bg = '#444444' if dark else '#eeeeee'
    btn_fg = '#ffffff' if dark else '#222222'
    inp_bg = '#2d2d2d' if dark else '#ffffff'
    inp_fg = '#ffffff' if dark else '#222222'
    lbl_fg = '#cccccc' if dark else '#333333'
    bdr_col = '#555'   if dark else '#ccc'

    svg_h = get_svg_h()
    rbs = (f'padding:5px 12px;font-size:12px;cursor:pointer;background:{btn_bg};color:{btn_fg};'
           f'border:1px solid #888;border-radius:4px')
    sbs = (f'padding:4px 10px;font-size:12px;cursor:pointer;background:{btn_bg};color:{btn_fg};'
           f'border:1px solid #888;border-radius:3px')
    nis = (f'padding:2px 4px;font-size:11px;border:1px solid #888;border-radius:3px;'
           f'background:{inp_bg};color:{inp_fg};')
    ins = (f'padding:4px 6px;font-size:12px;border:1px solid #888;border-radius:3px;'
           f'background:{inp_bg};color:{inp_fg};width:100%;box-sizing:border-box')

    sn_js = '[' + ','.join(f'"{n}"' for n in get_string_notes()) + ']'
    sf_js = '[' + ','.join(f'{f:.4f}' for f in get_string_freqs()) + ']'

    lick_panel = (
        f'<script>var _btnBg="{btn_bg}",_btnFg="{btn_fg}",_lblFg="{lbl_fg}",'
        f'_nStrings={get_n_strings()},_N_FRETS={N_FRETS},_STRING_NOTES={sn_js},_STRING_FREQS={sf_js};</script>'
        f'<div id="right-panel" style="width:200px;border-left:1px solid {bdr_col};'
        f'padding:10px 12px;font-family:Arial;color:{lbl_fg};'
        f'height:100%;box-sizing:border-box;display:flex;flex-direction:column">'
        
        f'<div style="font-size:12px;font-weight:bold;margin-bottom:5px">Chord Progression</div>'
        f'<input id="chord-prog" placeholder="Am F C G  or  A minor, F major, C@5" style="{ins}"'
        f' onkeydown="if(event.key===\'Enter\')playProgression()">'
        f'<div style="display:flex;align-items:center;gap:5px;margin-top:6px;flex-wrap:wrap">'
        f'<button id="prog-btn" onclick="playProgression()" style="{sbs}">&#9654; Play</button>'
        f'<span style="font-size:11px">Beats/chord</span>'
        f'<input id="prog-beats" type="number" value="4" min="1" max="32"'
        f' style="{nis}width:34px">'
        f'</div>'
        
        f'<hr style="border:none;border-top:1px solid {bdr_col};margin:10px 0 8px">'
        
        f'<div style="display:flex;gap:6px;margin-bottom:6px">'
        f'<button id="rec-btn" onclick="toggleRecording()" style="{rbs}">&#9210; Record</button>'
        f'<button id="metro-btn" onclick="toggleMetronome()" style="{rbs}">&#9833; Metro</button>'
        f'</div>'
        
        f'<div style="display:flex;align-items:center;gap:4px;margin-bottom:8px;font-size:11px">'
        f'<span>BPM</span>'
        f'<input id="metro-bpm" type="number" value="120" min="40" max="240"'
        f' oninput="_metroUpdate()" style="{nis}width:44px">'
        f'<span style="margin-left:4px">Time</span>'
        f'<input id="metro-top" type="number" value="4" min="1" max="12"'
        f' oninput="_metroUpdate()" style="{nis}width:28px">'
        f'<span>/</span>'
        f'<input id="metro-bot" type="number" value="4" min="1" max="32"'
        f' style="{nis}width:28px">'
        f'</div>'
        
        f'<div id="save-area" style="display:none;flex-direction:column;gap:5px;margin-bottom:8px">'
        f'<input id="lick-name" placeholder="Name this lick..." style="{ins}"'
        f' onkeydown="if(event.key===\'Enter\')saveLick()"/>'
        f'<button onclick="saveLick()" style="{sbs}">Save</button>'
        f'</div>'
        
        f'<div id="lick-list" style="flex-grow:1;overflow-y:auto;min-height:0"></div>'
        f'</div>'
    )

    return (
        f'<!DOCTYPE html><html><head>'
        f'<style>body{{margin:0;background:{bg};overflow-x:auto;overflow-y:hidden}}'
        f'table{{border-collapse:collapse}}td{{padding:0;vertical-align:top}}</style>'
        f'</head><body>'
        f'<table style="height:{svg_h}px"><tr style="height:{svg_h}px">'
        f'<td>{build_svg()}</td>'
        f'<td style="width:200px">{lick_panel}</td>'
        f'</tr></table>'
        f'{_KS_JS}</body></html>'
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

    st.components.v1.html(build_fretboard_html(), height=get_svg_h() + 20, scrolling=False)

    st.divider()

    
    util_cols = st.columns([1, 4, 4, 4])
    util_cols[0].markdown("**Display**")
    lbl_text = "Show Intervals" if s.label_mode == 'note' else "Show Note Names"
    if util_cols[1].button(lbl_text, key="lbl", use_container_width=True):
        s.label_mode = 'interval' if s.label_mode == 'note' else 'note'
        st.rerun()

    dark_text = "Light Mode" if s.dark else "Dark Mode"
    if util_cols[2].button(dark_text, key="btn_dark", use_container_width=True):
        s.dark = not s.dark
        st.rerun()

    if util_cols[3].button("Clear", key="clear", use_container_width=True):
        s.caged      = set()
        s.triad_grps = set()
        s.hide_notes = False
        s.view       = 'all'
        st.rerun()

    
    inst_cols = st.columns([1, 6, 6])
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

    
    mode_cols = st.columns([1] + [12/len(MODE_SCALES)] * len(MODE_SCALES))
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

    
    scale_cols = st.columns([1] + [12/len(NAMED_SCALES)] * len(NAMED_SCALES))
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

    
    chord_list = list(CHORD_INTERVALS.keys())
    chord_cols = st.columns([1] + [12/len(chord_list)] * len(chord_list))
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

    
    if not _is_bass():
        all_shapes  = set(CAGED_SHAPES.keys())
        shape_names = list(CAGED_SHAPES.keys()) + ['All']
        caged_cols  = st.columns([1] + [12/len(shape_names)] * len(shape_names))
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

    
    
    if _is_bass():
        group_labels = {0: 'G-D-A', 1: 'D-A-E'}
    else:
        group_labels = {0: 'e-B-G', 1: 'B-G-D', 2: 'G-D-A', 3: 'D-A-E'}
    n_triad_btns = 1 + len(group_labels)  
    triad_cols = st.columns([1] + [12/n_triad_btns] * n_triad_btns)
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


main()
