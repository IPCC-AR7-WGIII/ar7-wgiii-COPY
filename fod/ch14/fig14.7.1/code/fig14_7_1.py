#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# fig14_7_1.py — standalone export script for Fig14_7_1_maturity_matrix
# Extracted from ch14_schematics.ipynb (notebook retired as build system).
# AR7 restyle 2026-07-31: styled via _stylerun/ar7_style.py (IPCC palette,
# Arial/Arial Narrow, 180x100 mm canvas, 300 dpi export, WCAG/greyscale checks).
# Run from the "10_Figures" folder:  python "_stylerun/fig14_7_1.py"
# Reads maturity_evidence.csv (relative path); writes
# Fig14_7_1_maturity_matrix.png/.pdf beside the CSV at the folder
# root, with _greyscale.png in _qa/greyscale (central layout); or
# into figure/ with no greyscale dump (GitHub package layout).
import matplotlib
matplotlib.use("Agg")

import csv
import os
import sys
import textwrap

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
import matplotlib.text as mtext

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ar7_style as ar7

# Layout-aware paths (R9). HERE is this file's folder, ROOT its parent, so one
# file serves both places it is run from:
#   central working folder -- CSVs read from and renders written to ROOT, with
#     greyscale QA dumps in ROOT/_qa/greyscale;
#   GitHub figure package (ROOT/CITATION.cff present) -- data read from
#     ROOT/data, renders written to ROOT/figure, no greyscale dump.
# Paths are normalised in ar7.layout() so 'code/../data' stays inside the
# Windows 260-character limit on long checkout locations.
DATA_DIR, OUT_DIR, GREY_DIR = ar7.layout(__file__)
os.makedirs(OUT_DIR, exist_ok=True)

ar7.apply_style()

# ---------------------------------------------------------------- content ---
# Content is FROZEN: maturity classes and citations come verbatim from
# maturity_evidence.csv. Only labelling changed for AR7 style: acronyms are
# spelled out at first occurrence (IoT -> internet of things, AI -> artificial
# intelligence). IEA and PJM in citations stay as-is: they are the publishing
# organisations' standard citation names, not expandable acronyms in-figure.
CATEGORIES = [
    ('Sensing and data acquisition', 'Sensing and\ndata acquisition',
     '(internet of things,\nsensor networks)'),
    ('Analytics and optimisation', 'Analytics and\noptimisation',
     '(artificial intelligence,\nmachine learning)'),
    ('Simulation and planning', 'Simulation and\nplanning',
     '(digital twins)'),
    ('Coordination and control', 'Coordination and\ncontrol',
     '(platforms,\ncommunication networks)'),
]
MODES = ['Sector coupling', 'Flexibility provision', 'Real-time balancing',
         'Forecasting and planning']
MODE_LABELS = ['Sector\ncoupling', 'Flexibility\nprovision',
               'Real-time\nbalancing', 'Forecasting and\nanticipatory planning']
# S9: the mode names are the field's own terms and stay fixed (style note
# 17); these glosses give the plain-words reading D4 asks for, in the same
# manner the row categories already use.
MODE_GLOSS = ['linking electricity with\nheat, transport and industry',
              'shifting demand and\nsupply in time',
              'matching supply and\ndemand second by second',
              'predicting output and\ndemand ahead of time']

# Maturity ramp on the IPCC palette: dark_blue -> ipcc_blue -> warm_yellow.
# Not a red-green pairing; three distinct lightnesses so the ramp survives
# greyscale; a per-class marker (filled / half / open circle) gives a second,
# non-colour channel. Text colour flips to white on the dark fill for WCAG AA.
CLASS_ORDER = ['deployed at scale', 'demonstrated in pilots',
               'research and prototype']
# Fills lightened on 2026-09-29 for the FOD review, which asked for a lighter
# blue on "demonstrated in pilots" to improve the contrast of the text on it.
# Black-on-fill contrast rises from 6.37 to 9.51 for pilots and from 10.93 to
# 14.52 for research. Both are tints of the same palette hues, so the ordinal
# ramp is unchanged in order and direction: greyscale L 42 / 171 / 211, gaps
# 129 and 40, both clear of the 30 floor. Lightening research is only possible
# because the header band moved to white; against the old grey(0.15) headers it
# would have been 6 levels away.
CLASS_STYLE = {
    'deployed at scale':      {'fill': ar7.PALETTE['dark_blue'],
                               'text': '#ffffff', 'marker': 'full',
                               'label': 'Deployed at scale'},
    'demonstrated in pilots': {'fill': ar7.tint(ar7.PALETTE['ipcc_blue'], 0.30),
                               'text': ar7.BLACK, 'marker': 'half',
                               'label': 'Demonstrated in pilots'},
    'research and prototype': {'fill': ar7.tint(ar7.PALETTE['warm_yellow'], 0.45),
                               'text': ar7.BLACK, 'marker': 'open',
                               'label': 'Research and prototype'},
}

HEADLINE = ('Digitalisation technologies for integration span the full maturity\n'
            'range, from deployed at scale to research and prototype')

GREY_EDGE = ar7.grey(0.40)      # cell borders
GREY_HEAD = '#ffffff'           # header band, white (FOD review feedback,
                                # 2026-09-29). It was grey(0.15), L 217, which
                                # capped how light the class fills could go
                                # before headers and data cells became
                                # indistinguishable in greyscale. White frees
                                # the light end of the ramp, and it also
                                # removes the old clash with ar7.NO_DATA, which
                                # is grey(0.15) and keeps its no-data meaning.
GREY_SUBTLE = ar7.grey(0.70)    # secondary text (example sublabels)

# ------------------------------------------------------------- geometry (mm) —
# The axes are mapped 1 data unit = 1 mm on a 180x100 mm canvas, so every
# coordinate below is a physical measurement on the printed page.
CANVAS = (180, 100)
X0 = 2.0                 # left margin
HEADER_COL_W = 36.0      # column pitch of the category header column
COL_W = 35.0             # column pitch of the four data columns
GAP = 0.8                # white gap between cells
MARKER_CLEAR = 4.4       # cell text starts right of this, clear
                         # of the class marker
ROW_PITCH = 14.8
HEADER_ROW_TOP = 85.0
HEADER_ROW_H = 13.0
DATA_TOP = 71.2          # top of the first data row
CELL_H = ROW_PITCH - GAP
BOX = 'round,pad=0,rounding_size=1.2'
LEGEND_XS = (6.0, 54.0, 110.0)
LEGEND_Y0 = 4.6          # legend swatch bottom; swatch 6 x 4 mm

SIZE_HEADER = ar7.SIZE_AXIS_LABEL      # 8 pt bold — row/column headers
SIZE_CELL = ar7.SIZE_TICK              # 7 pt — class labels. Kept in Arial
                                       # Narrow: regular Arial overflowed the
                                       # cells and fouled the markers.
SIZE_CITE = ar7.SIZE_TICK              # 7 pt — in-cell citations. Raised from
                                       # the 6 pt floor for the FOD review, and
                                       # kept in Arial Narrow: these are the
                                       # densest strings on the canvas.
SIZE_EXAMPLE = 7                       # example sublabels (annotation font)


def read_cells(csv_path=None):
    # Resolved through DATA_DIR so the same file reads the CSV at
    # the folder root centrally and from data/ inside a package.
    csv_path = csv_path or os.path.join(DATA_DIR, 'maturity_evidence.csv')
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    cells = {}
    for r in rows:
        key = (r['category'].strip(), r['mode'].strip())
        klass = r['maturity_class'].strip().lower()
        if klass not in CLASS_STYLE:
            raise ValueError(f'unknown maturity_class {klass!r} for {key}')
        cells[key] = (klass, r.get('short_citation', '').strip())
    return cells


# ------------------------------------------------------------ build figure ---
AUDIT = []      # text audit: WCAG + containment entries
PAIRS = []      # (upper_artist, lower_artist, desc) vertical-gap checks
CLEARS = []     # (artist, min_x_mm, desc) marker-clearance checks

fig = plt.figure(figsize=ar7.fig_mm(*CANVAS))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, CANVAS[0])
ax.set_ylim(0, CANVAS[1])
ax.set_axis_off()


def add_text(x, y, s, *, desc, bg, bounds=None, **kw):
    t = ax.text(x, y, s, **kw)
    AUDIT.append({'desc': desc, 'artist': t, 'bg': bg, 'bounds': bounds})
    return t


def draw_marker(x, y, klass, colour):
    kind = CLASS_STYLE[klass]['marker']
    kw = dict(marker='o', linestyle='none', markersize=6.0,
              markeredgewidth=0.7, markeredgecolor=colour,
              clip_on=False, zorder=3)
    if kind == 'full':
        ln = Line2D([x], [y], markerfacecolor=colour, **kw)
    elif kind == 'half':
        ln = Line2D([x], [y], fillstyle='left', markerfacecolor=colour,
                    markerfacecoloralt='none', **kw)
    else:
        ln = Line2D([x], [y], markerfacecolor='none', **kw)
    ax.add_line(ln)


# Headline (required wording, bold 14 pt, above the figure)
add_text(X0, 99.3, HEADLINE, desc='headline',
         bg='#ffffff', bounds=(X0, 178.0, 86.0, 100.0),
         ha='left', va='top', linespacing=1.12, **ar7.headline_kwargs())

# Column headers
ax.add_patch(FancyBboxPatch((X0, HEADER_ROW_TOP - HEADER_ROW_H),
                            HEADER_COL_W - GAP, HEADER_ROW_H, boxstyle=BOX,
                            facecolor=GREY_HEAD, edgecolor=GREY_EDGE,
                            linewidth=0.6))
for j, label in enumerate(MODE_LABELS):
    x = X0 + HEADER_COL_W + j * COL_W
    ax.add_patch(FancyBboxPatch((x, HEADER_ROW_TOP - HEADER_ROW_H),
                                COL_W - GAP, HEADER_ROW_H, boxstyle=BOX,
                                facecolor=GREY_HEAD, edgecolor=GREY_EDGE,
                                linewidth=0.6))
    add_text(x + (COL_W - GAP) / 2, HEADER_ROW_TOP - 3.2, label,
             desc=f'mode header {j}', bg=GREY_HEAD,
             bounds=(x, x + COL_W - GAP,
                     HEADER_ROW_TOP - HEADER_ROW_H, HEADER_ROW_TOP),
             ha='center', va='center', family='Arial',
             fontsize=SIZE_HEADER, fontweight='bold', color=ar7.BLACK)
    add_text(x + (COL_W - GAP) / 2, HEADER_ROW_TOP - 9.4, MODE_GLOSS[j],
             desc=f'mode gloss {j}', bg=GREY_HEAD,
             bounds=(x, x + COL_W - GAP,
                     HEADER_ROW_TOP - HEADER_ROW_H, HEADER_ROW_TOP),
             ha='center', va='center', family='Arial',
             fontsize=SIZE_CELL, color=GREY_SUBTLE)

# Data rows
cells = read_cells()
for i, (cat_key, cat_label, examples) in enumerate(CATEGORIES):
    top = DATA_TOP - i * ROW_PITCH
    bot = top - CELL_H
    ax.add_patch(FancyBboxPatch((X0, bot), HEADER_COL_W - GAP, CELL_H,
                                boxstyle=BOX, facecolor=GREY_HEAD,
                                edgecolor=GREY_EDGE, linewidth=0.6))
    cxh = X0 + (HEADER_COL_W - GAP) / 2
    name_t = add_text(cxh, top - 4.4, cat_label, desc=f'category {i} name',
                      bg=GREY_HEAD, bounds=(X0, X0 + HEADER_COL_W - GAP, bot, top),
                      ha='center', va='center', family='Arial',
                      fontsize=SIZE_HEADER, fontweight='bold', color=ar7.BLACK)
    ex_t = add_text(cxh, bot + 3.6, examples, desc=f'category {i} examples',
                    bg=GREY_HEAD, bounds=(X0, X0 + HEADER_COL_W - GAP, bot, top),
                    ha='center', va='center', fontsize=SIZE_EXAMPLE,
                    color=GREY_SUBTLE, **ar7.ANNOTATION_FONT)
    PAIRS.append((name_t, ex_t, f'category {i} name/examples'))

    for j, mode in enumerate(MODES):
        left = X0 + HEADER_COL_W + j * COL_W
        cw = COL_W - GAP
        cx = left + cw / 2
        entry = cells.get((cat_key, mode))
        if entry:
            klass, cite = entry
            st = CLASS_STYLE[klass]
            ax.add_patch(FancyBboxPatch((left, bot), cw, CELL_H, boxstyle=BOX,
                                        facecolor=st['fill'],
                                        edgecolor=GREY_EDGE, linewidth=0.6))
            draw_marker(left + 2.7, top - 2.9, klass, st['text'])
            # Centred in the space right of the marker, not in the whole
            # cell: regular Arial is wider than Arial Narrow and would
            # otherwise foul the marker at left + MARKER_CLEAR.
            lab_cx = (left + MARKER_CLEAR + left + cw) / 2
            lab_t = add_text(lab_cx, top - 2.9, st['label'],
                             desc=f'class label ({i},{j})', bg=st['fill'],
                             bounds=(left, left + cw, bot, top),
                             ha='center', va='center', family='Arial',
                             fontsize=SIZE_CELL, color=st['text'])
            CLEARS.append((lab_t, left + MARKER_CLEAR,
                           f'class label ({i},{j})'))
            if cite:
                # 27 characters, not 33: regular Arial is wider than Arial
                # Narrow. 33 put the longest line outside the cell and 30
                # left the densest cell with no visible side margin.
                lines = textwrap.wrap(
                    f'({cite})'.replace('et al.', 'et al.'), 27)
                n = len(lines)
                cite_t = add_text(cx, bot + 1.3 + n * 1.27, '\n'.join(lines),
                                  desc=f'citation ({i},{j})', bg=st['fill'],
                                  bounds=(left, left + cw, bot, top),
                                  ha='center', va='center',
                                  family='Arial', fontsize=SIZE_CITE,
                                  color=st['text'])
                PAIRS.append((lab_t, cite_t, f'cell ({i},{j}) label/citation'))
        else:
            # A genuinely empty (category, mode) cell renders as NO_DATA (15%
            # black) and must carry a documented sentinel row in
            # maturity_evidence.csv. As of 2026-07-31 all 16 cells have
            # evidence rows, so this branch is unreachable.
            ax.add_patch(FancyBboxPatch((left, bot), cw, CELL_H, boxstyle=BOX,
                                        facecolor=ar7.NO_DATA,
                                        edgecolor=GREY_EDGE, linewidth=0.6))
            add_text(cx, (top + bot) / 2, 'not assessed',
                     desc=f'not assessed ({i},{j})', bg=ar7.NO_DATA,
                     bounds=(left, left + cw, bot, top),
                     ha='center', va='center', family='Arial',
                     fontsize=SIZE_CELL, style='italic', color=GREY_SUBTLE)


# ---------------------------------------------------------------- checks ----
MM = 25.4


def _ext_mm(artist, renderer):
    e = artist.get_window_extent(renderer=renderer)
    d = fig.dpi
    return (e.x0 / d * MM, e.x1 / d * MM, e.y0 / d * MM, e.y1 / d * MM)


def _pil_L(hex_colour):
    r, g, b = (int(hex_colour.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return round(0.299 * r + 0.587 * g + 0.114 * b)


def run_checks():
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    fails = []

    # 1) fonts: every rendered text resolves to an Arial-family file
    families = set()
    texts = [t for t in fig.findobj(mtext.Text) if t.get_text().strip()]
    for t in texts:
        fname = os.path.basename(
            font_manager.findfont(t.get_fontproperties()))
        families.add(fname)
        if not fname.upper().startswith('ARIAL'):
            fails.append(f'FONT: {t.get_text()[:30]!r} -> {fname}')
    print(f'fonts: {len(texts)} texts -> {sorted(families)}')

    # 2) minimum size
    smallest = min(t.get_fontsize() for t in texts)
    print(f'min text size: {smallest} pt (floor {ar7.SIZE_MIN})')
    if smallest < ar7.SIZE_MIN:
        fails.append(f'SIZE: {smallest} pt < {ar7.SIZE_MIN}')

    # 3) WCAG AA for every audited text against its actual background
    combos = {}
    for a in AUDIT:
        t = a['artist']
        bold = str(t.get_fontweight()) in ('bold', '700')
        ok, ratio, thr = ar7.wcag_passes(t.get_color(), a['bg'],
                                         t.get_fontsize(), bold)
        key = (str(t.get_color()), a['bg'], thr)
        combos[key] = min(combos.get(key, 99.0), ratio)
        if not ok:
            fails.append(f"WCAG: {a['desc']} {ratio:.2f} < {thr}")
    for (fg, bg, thr), ratio in sorted(combos.items()):
        print(f'wcag: {fg} on {bg}: {ratio:.2f} (needs {thr})')

    # 4) containment and collision
    for a in AUDIT:
        if a['bounds']:
            x0, x1, y0, y1 = a['bounds']
            ex0, ex1, ey0, ey1 = _ext_mm(a['artist'], ren)
            if (ex0 < x0 - 0.4 or ex1 > x1 + 0.4
                    or ey0 < y0 - 0.4 or ey1 > y1 + 0.4):
                fails.append(f"BOUNDS: {a['desc']} "
                             f'[{ex0:.1f},{ex1:.1f},{ey0:.1f},{ey1:.1f}] '
                             f'outside [{x0},{x1},{y0},{y1}]')
    for upper, lower, desc in PAIRS:
        gap = _ext_mm(upper, ren)[2] - _ext_mm(lower, ren)[3]
        if gap < 0.3:
            fails.append(f'OVERLAP: {desc} gap {gap:.2f} mm')
    for t, min_x, desc in CLEARS:
        if _ext_mm(t, ren)[0] < min_x:
            fails.append(f'MARKER CLEARANCE: {desc}')

    # 5) greyscale separation of the three class fills (PIL L formula)
    Ls = {k: _pil_L(CLASS_STYLE[k]['fill']) for k in CLASS_ORDER}
    print('greyscale L:', ', '.join(f'{k} {v}' for k, v in Ls.items()))
    vals = [Ls[k] for k in CLASS_ORDER]
    gaps = [abs(a - b) for a, b in zip(vals, vals[1:])]
    if min(gaps) < 30:
        fails.append(f'GREYSCALE: class L gaps {gaps} (< 30)')

    for f_ in fails:
        print('FAIL', f_)
    return not fails


ok = run_checks()
if not ok:
    sys.exit(1)

ar7.export(fig, os.path.join(OUT_DIR, 'Fig14_7_1_maturity_matrix'))
if GREY_DIR:
    os.makedirs(GREY_DIR, exist_ok=True)
    print('greyscale dump:',
          ar7.greyscale_dump(fig, os.path.join(GREY_DIR, 'Fig14_7_1_maturity_matrix')))
print(f'exported Fig14_7_1_maturity_matrix.png/.pdf '
      f'({CANVAS[0]}x{CANVAS[1]} mm, 300 dpi)')
