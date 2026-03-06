import tkinter as tk
import threading

try:
    import numpy as np
    import sounddevice as sd
    _AUDIO_OK = True
except ImportError:
    _AUDIO_OK = False


class GuitarFretboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guitar Fretboard")
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.string_notes = ['E', 'B', 'G', 'D', 'A', 'E']
        self.selected_root = 'C'
        self.note_buttons = {}
        self.scale_buttons = {}
        self.chord_buttons = {}
        self.caged_buttons = {}
        self.active_triad_groups = {0, 1, 2, 3}
        self.triad_group_buttons = {}

        self.mode_scales = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
        self.named_scales = ['Nat Minor', 'Harm Minor', 'Mel Minor', 'Maj Pent', 'Min Pent', 'Maj Blues', 'Min Blues']

        self.scale_intervals = {
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
        self.chord_intervals = {
            'Major': [0, 4, 7],
            'Minor': [0, 3, 7],
            'Sus4':  [0, 5, 7],
            'Sus2':  [0, 2, 7],
            'Aug':   [0, 4, 8],
            'Dim':   [0, 3, 6],
            'Add9':  [0, 4, 7, 2],
            '7':     [0, 4, 7, 10],
        }
        self.scale_degrees = {
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
        self.chord_degrees = {
            'Major': {0:'R', 4:'3', 7:'5'},
            'Minor': {0:'R', 3:'b3', 7:'5'},
            'Sus4':  {0:'R', 5:'4', 7:'5'},
            'Sus2':  {0:'R', 2:'2', 7:'5'},
            'Aug':   {0:'R', 4:'3', 8:'#5'},
            'Dim':   {0:'R', 3:'b3', 6:'b5'},
            'Add9':  {0:'R', 4:'3', 7:'5', 2:'9'},
            '7':     {0:'R', 4:'3', 7:'5', 10:'b7'},
        }
        self.interval_colors = {
            'R': 'green', '1': 'green',
            '3': 'blue',  'b3': 'red',
            '5': 'blue',  'b5': 'red',  '#5': 'red',
            '9': 'red',   'b7': 'red',  '7': 'red',
            '4': 'red',   '2': 'red',   'b2': 'red',
            '#4': 'red',  '6': 'red',   'b6': 'red',
        }
        self.label_mode = 'note'
        self.current_scale = 'Ionian'
        self.last_render_fn = None
        self.caged_shapes = {
            'C': {'pattern': [0, 1, 0, 2, 3, -1], 'root_string': 4, 'root_fret_in_pattern': 3},
            'A': {'pattern': [0, 2, 2, 2, 0, -1], 'root_string': 4, 'root_fret_in_pattern': 0},
            'G': {'pattern': [3, 3, 0, 0, 2,  3], 'root_string': 5, 'root_fret_in_pattern': 3},
            'E': {'pattern': [0, 0, 1, 2, 2,  0], 'root_string': 5, 'root_fret_in_pattern': 0},
            'D': {'pattern': [2, 3, 2, 0, -1,-1], 'root_string': 3, 'root_fret_in_pattern': 0},
        }
        self.dark_mode = False
        self.colors = {
            'bg': 'white', 'string': 'brown',
            'fret': 'black', 'marker': 'black', 'text': 'black',
        }
        self.open_string_freqs = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
        self._play_lock = threading.Lock()

        self.canvas = tk.Canvas(root, width=1200, height=400, bg='white')
        self.canvas.pack()
        self.highlights = []
        self.draw_fretboard()
        self.create_ui()
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.show_scale('Ionian')


    def draw_fretboard(self):
        for i in range(6):
            y = 50 + i * 50
            self.canvas.create_line(50, y, 1150, y, width=2, fill=self.colors['string'])
        for i in range(23):
            x = 50 + i * 50
            self.canvas.create_line(x, 50, x, 300, width=2 if i == 0 else 1, fill=self.colors['fret'])
        for fret in [3, 5, 7, 9, 15, 17, 19, 21]:
            x = 50 + fret * 50
            self.canvas.create_oval(x-5, 170, x+5, 180, fill=self.colors['marker'])
        x = 50 + 12 * 50
        self.canvas.create_oval(x-5, 165, x+5, 175, fill=self.colors['marker'])
        self.canvas.create_oval(x-5, 185, x+5, 195, fill=self.colors['marker'])
        for i, note in enumerate(self.string_notes):
            self.canvas.create_text(25, 50 + i*50, text=note, font=('Arial', 12), fill=self.colors['text'])
        for i in range(23):
            x = 50 + i * 50
            self.canvas.create_text(x, 320, text=str(i), font=('Arial', 10), fill=self.colors['text'])


    def create_ui(self):
        note_frame = tk.Frame(self.root)
        note_frame.pack(pady=6)
        tk.Label(note_frame, text="Root:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 6))
        for note in self.notes:
            btn = tk.Button(note_frame, text=note, width=3,
                            command=lambda n=note: self.select_root(n))
            btn.pack(side=tk.LEFT, padx=2)
            self.note_buttons[note] = btn
        self._default_btn_bg = self.note_buttons['C'].cget('bg')
        self.select_root('C')

        modes_frame = tk.Frame(self.root)
        modes_frame.pack(pady=4)
        tk.Label(modes_frame, text="Modes:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 6))
        for scale in self.mode_scales:
            btn = tk.Button(modes_frame, text=scale,
                            command=lambda s=scale: self.show_scale(s))
            btn.pack(side=tk.LEFT, padx=2)
            self.scale_buttons[scale] = btn

        scales_frame = tk.Frame(self.root)
        scales_frame.pack(pady=4)
        tk.Label(scales_frame, text="Scales:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 6))
        for scale in self.named_scales:
            btn = tk.Button(scales_frame, text=scale,
                            command=lambda s=scale: self.show_scale(s))
            btn.pack(side=tk.LEFT, padx=2)
            self.scale_buttons[scale] = btn

        chord_frame = tk.Frame(self.root)
        chord_frame.pack(pady=4)
        tk.Label(chord_frame, text="Chords:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 6))
        for chord in self.chord_intervals:
            btn = tk.Button(chord_frame, text=chord,
                            command=lambda c=chord: self.show_chord(c))
            btn.pack(side=tk.LEFT, padx=2)
            self.chord_buttons[chord] = btn

        caged_frame = tk.Frame(self.root)
        caged_frame.pack(pady=4)
        tk.Label(caged_frame, text="CAGED:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 6))
        for shape in self.caged_shapes:
            btn = tk.Button(caged_frame, text=f"{shape} Shape",
                            command=lambda s=shape: self.show_caged(s))
            btn.pack(side=tk.LEFT, padx=2)
            self.caged_buttons[shape] = btn
        btn = tk.Button(caged_frame, text="All Shapes",
                        command=lambda: self.show_caged('All'))
        btn.pack(side=tk.LEFT, padx=2)
        self.caged_buttons['All'] = btn

        triad_frame = tk.Frame(self.root)
        triad_frame.pack(pady=4)
        tk.Label(triad_frame, text="Triads:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 6))
        self.triad_btn = tk.Button(triad_frame, text="Show Triads", command=self.toggle_triads)
        self.triad_btn.pack(side=tk.LEFT, padx=2)
        tk.Label(triad_frame, text="  Groups:", fg='gray').pack(side=tk.LEFT, padx=(6, 2))
        for group_id, label in [(0, 'e-B-G'), (1, 'B-G-D'), (2, 'G-D-A'), (3, 'D-A-E')]:
            btn = tk.Button(triad_frame, text=label,
                            command=lambda g=group_id: self.toggle_triad_group(g))
            btn.pack(side=tk.LEFT, padx=2)
            self.triad_group_buttons[group_id] = btn
        self._update_triad_group_buttons()

        other_frame = tk.Frame(self.root)
        other_frame.pack(pady=4)
        self.label_btn = tk.Button(other_frame,
                                   text='Show Intervals' if self.label_mode == 'note' else 'Show Note Names',
                                   command=self.toggle_label_mode)
        self.label_btn.pack(side=tk.LEFT, padx=2)
        tk.Button(other_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode).pack(side=tk.LEFT, padx=2)
        tk.Button(other_frame, text="Clear", command=self.clear_highlights).pack(side=tk.LEFT, padx=2)

    def select_root(self, note):
        self.selected_root = note
        for n, btn in self.note_buttons.items():
            if n == note:
                btn.config(bg='#2ecc71', fg='black', font=('Arial', 10, 'bold'))
            else:
                btn.config(bg=self._default_btn_bg, fg='black', font=('Arial', 10))
        if self.last_render_fn:
            self.last_render_fn()

    _group_colors = {0: '#ff6600', 1: '#9900cc', 2: '#0066ff', 3: '#009900'}

    def _update_triad_group_buttons(self):
        for group_id, btn in self.triad_group_buttons.items():
            if group_id in self.active_triad_groups:
                btn.config(bg=self._group_colors[group_id], fg='black', font=('Arial', 9, 'bold'))
            else:
                btn.config(bg=self._default_btn_bg, fg='black', font=('Arial', 9))

    def _set_section_btn(self, btn_dict, active_key):
        for btn in self.scale_buttons.values():
            btn.config(bg=self._default_btn_bg, fg='black', font=('Arial', 10))
        for btn in self.chord_buttons.values():
            btn.config(bg=self._default_btn_bg, fg='black', font=('Arial', 10))
        for btn in self.caged_buttons.values():
            btn.config(bg=self._default_btn_bg, fg='black', font=('Arial', 10))
        if active_key in btn_dict:
            btn_dict[active_key].config(bg='#2ecc71', fg='black', font=('Arial', 10, 'bold'))

    def toggle_triad_group(self, group):
        if group in self.active_triad_groups:
            self.active_triad_groups.discard(group)
        else:
            self.active_triad_groups.add(group)
        self._update_triad_group_buttons()
        if self.last_render_fn == self.show_triads:
            self.show_triads()


    def get_note_at(self, string, fret):
        idx = (self.notes.index(self.string_notes[string]) + fret) % 12
        return self.notes[idx]

    def highlight_with_labels(self, degrees_dict):
        for string in range(6):
            for fret in range(23):
                note = self.get_note_at(string, fret)
                note_idx = self.notes.index(note)
                if note_idx in degrees_dict:
                    label = degrees_dict[note_idx]
                    color = self.interval_colors.get(label, 'red')
                    display = note if self.label_mode == 'note' else label
                    x = 50 + fret * 50
                    y = 50 + string * 50
                    item1 = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=color, outline=color)
                    text_color = 'white' if color in ['green', 'blue', 'red', 'purple'] else 'black'
                    item2 = self.canvas.create_text(x, y, text=display, font=('Arial', 10, 'bold'), fill=text_color)
                    self.highlights.extend([item1, item2])

    def clear_highlights(self):
        for item in self.highlights:
            self.canvas.delete(item)
        self.highlights = []
        if hasattr(self, 'triad_btn'):
            self.triad_btn.config(text="Show Triads")

    def toggle_label_mode(self):
        self.label_mode = 'note' if self.label_mode == 'interval' else 'interval'
        self.label_btn.config(text='Show Intervals' if self.label_mode == 'note' else 'Show Note Names')
        if self.last_render_fn:
            self.last_render_fn()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.colors = {
            'bg': '#1e1e1e', 'string': '#daa520', 'fret': '#ffffff',
            'marker': '#ffffff', 'text': '#ffffff',
        } if self.dark_mode else {
            'bg': 'white', 'string': 'brown',
            'fret': 'black', 'marker': 'black', 'text': 'black',
        }
        self.canvas.config(bg=self.colors['bg'])
        self.canvas.delete('all')
        self.draw_fretboard()
        if self.last_render_fn:
            self.last_render_fn()


    def show_scale(self, scale):
        self.clear_highlights()
        self.current_scale = scale
        self._set_section_btn(self.scale_buttons, scale)
        self.last_render_fn = lambda s=scale: self.show_scale(s)
        root_idx = self.notes.index(self.selected_root)
        degrees_dict = {
            (root_idx + i) % 12: self.scale_degrees[scale][i]
            for i in self.scale_intervals[scale]
        }
        self.highlight_with_labels(degrees_dict)

    def show_chord(self, chord_type):
        self.clear_highlights()
        self._set_section_btn(self.chord_buttons, chord_type)
        self.last_render_fn = lambda c=chord_type: self.show_chord(c)
        root_idx = self.notes.index(self.selected_root)
        degrees_dict = {
            (root_idx + i) % 12: self.chord_degrees[chord_type][i]
            for i in self.chord_intervals[chord_type]
        }
        self.highlight_with_labels(degrees_dict)

    def show_caged(self, selected='All'):
        self.clear_highlights()
        self._set_section_btn(self.caged_buttons, selected)
        self.last_render_fn = lambda s=selected: self.show_caged(s)
        shapes_to_show = list(self.caged_shapes.keys()) if selected == 'All' else [selected]
        root_idx = self.notes.index(self.selected_root)
        chord_degs = {0: 'R', 4: '3', 7: '5'}
        box_colors = {'C': '#ff6600', 'A': '#9900cc', 'G': '#0066ff', 'E': '#009900', 'D': '#cc0000'}

        for shape_name in shapes_to_show:
            shape = self.caged_shapes[shape_name]
            open_note_idx = self.notes.index(self.string_notes[shape['root_string']])
            base_fret = (root_idx - open_note_idx) % 12 - shape['root_fret_in_pattern']
            if base_fret < 0:
                base_fret += 12

            if base_fret <= 22:
                frets_drawn, strings_drawn = [], []
                for string_idx, fret_offset in enumerate(shape['pattern']):
                    if fret_offset == -1:
                        continue
                    actual_fret = base_fret + fret_offset
                    if actual_fret > 22:
                        continue
                    note_idx = self.notes.index(self.get_note_at(string_idx, actual_fret))
                    label = chord_degs.get((note_idx - root_idx) % 12, '?')
                    color = self.interval_colors.get(label, 'gray')
                    display = self.notes[note_idx] if self.label_mode == 'note' else label
                    x = 50 + actual_fret * 50
                    y = 50 + string_idx * 50
                    item1 = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=color, outline=color)
                    text_color = 'white' if color in ['green', 'blue', 'red', 'purple'] else 'black'
                    item2 = self.canvas.create_text(x, y, text=display, font=('Arial', 10, 'bold'), fill=text_color)
                    self.highlights.extend([item1, item2])
                    frets_drawn.append(actual_fret)
                    strings_drawn.append(string_idx)

                if frets_drawn:
                    xs = [50 + f * 50 for f in frets_drawn]
                    ys = [50 + s * 50 for s in strings_drawn]
                    box_color = box_colors[shape_name]
                    box = self.canvas.create_rectangle(
                        min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                        outline=box_color, width=2, fill=''
                    )
                    lbl = self.canvas.create_text(
                        min(xs)-14, min(ys)-26, text=shape_name,
                        font=('Arial', 9, 'bold'), fill=box_color, anchor='w'
                    )
                    self.highlights.extend([box, lbl])

    def toggle_triads(self):
        if self.last_render_fn == self.show_triads:
            self.clear_highlights()
            self.last_render_fn = None
        else:
            self.show_triads()

    def _triad_from_scale(self):
        """Return (triad_degrees_dict_by_interval, required_labels) for the tonic triad of the current scale."""
        scale = self.current_scale
        intervals = self.scale_intervals[scale]
        degs = self.scale_degrees[scale]

        # Natural 3rd beats flat 3rd; natural 5th beats altered 5ths
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

    def show_triads(self):
        self.clear_highlights()
        self.last_render_fn = self.show_triads
        self.triad_btn.config(text="Hide Triads")
        root_idx = self.notes.index(self.selected_root)

        triad_degs, required_labels = self._triad_from_scale()
        degrees_dict = {(root_idx + i) % 12: triad_degs[i] for i in triad_degs}

        all_positions = [
            {'x': 50 + fret*50, 'y': 50 + string*50,
             'string': string, 'fret': fret,
             'label': degrees_dict[self.notes.index(self.get_note_at(string, fret))],
             'note_idx': self.notes.index(self.get_note_at(string, fret))}
            for string in range(6) for fret in range(23)
            if self.notes.index(self.get_note_at(string, fret)) in degrees_dict
        ]

        for group, voicing in self.find_triad_voicings(all_positions, required_labels):
            if group not in self.active_triad_groups:
                continue
            box_color = self._group_colors[group]
            for pos in voicing:
                label = pos['label']
                color = self.interval_colors.get(label, 'red')
                x, y = pos['x'], pos['y']
                item1 = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=color, outline=color)
                text_color = 'white' if color in ['green', 'blue', 'red', 'purple'] else 'black'
                display = self.get_note_at(pos['string'], pos['fret']) if self.label_mode == 'note' else label
                item2 = self.canvas.create_text(x, y, text=display, font=('Arial', 10, 'bold'), fill=text_color)
                self.highlights.extend([item1, item2])
            xs = [p['x'] for p in voicing]
            ys = [p['y'] for p in voicing]
            box = self.canvas.create_rectangle(
                min(xs)-15, min(ys)-15, max(xs)+15, max(ys)+15,
                outline=box_color, width=2, fill=''
            )
            self.highlights.append(box)

    def find_triad_voicings(self, positions, required_labels=None):
        """One non-overlapping triad voicing per fret region per string group."""
        if required_labels is None:
            required_labels = {'R', '3', '5'}
        by_string = {s: [] for s in range(6)}
        for pos in positions:
            by_string[pos['string']].append(pos)

        result = []
        for base in range(4):
            s0, s1, s2 = by_string[base], by_string[base+1], by_string[base+2]
            candidates = []
            for p0 in s0:
                for p1 in s1:
                    for p2 in s2:
                        labels = {p0['label'], p1['label'], p2['label']}
                        frets = [p0['fret'], p1['fret'], p2['fret']]
                        if labels == required_labels and max(frets) - min(frets) <= 4:
                            candidates.append((min(frets), [p0, p1, p2]))
            candidates.sort()
            last_min = -5
            for min_fret, voicing in candidates:
                if min_fret >= last_min + 4:
                    result.append((base, voicing))
                    last_min = min_fret

        return result



    def on_canvas_click(self, event):
        """Play the note at the nearest fret/string intersection."""
        if not _AUDIO_OK:
            return
        fret = round((event.x - 50) / 50)
        string = round((event.y - 50) / 50)
        fret = max(0, min(22, fret))
        string = max(0, min(5, string))
        if abs(event.x - (50 + fret * 50)) > 18 or abs(event.y - (50 + string * 50)) > 18:
            return
        freq = self.open_string_freqs[string] * (2 ** (fret / 12))
        threading.Thread(target=self._play_note, args=(freq,), daemon=True).start()

    def _play_note(self, frequency, sample_rate=44100, duration=2.5):
        """Karplus-Strong plucked string synthesis."""
        N = int(sample_rate / frequency)
        if N < 2:
            return
        n_samples = int(sample_rate * duration)

        buf = np.random.uniform(-1.0, 1.0, N).astype(np.float32)

        decay = 0.998 if frequency < 300 else 0.996

        out = np.zeros(n_samples, dtype=np.float32)
        for i in range(n_samples):
            j = i % N
            out[i] = buf[j]
            buf[j] = decay * 0.5 * (buf[j] + buf[(i + 1) % N])

        out = np.tanh(out * 1.5).astype(np.float32) * 0.65

        try:
            with self._play_lock:
                sd.stop()
                sd.play(out, sample_rate)
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = GuitarFretboardApp(root)
    root.mainloop()
