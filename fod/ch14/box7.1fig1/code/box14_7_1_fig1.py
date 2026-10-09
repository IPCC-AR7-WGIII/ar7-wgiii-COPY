#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# box14_7_1_fig1.py — standalone export script for FigBox14_1_integration_architecture
# Extracted from ch14_schematics.ipynb (notebook retired as build system).
# AR7 restyle 2026-07-31 (Block 5): styled via _stylerun/ar7_style.py — IPCC
# palette (blues + mustard family, no red-green pairing), Arial/Arial Narrow
# type scale, 180x100 mm canvas, 300 dpi export, WCAG / greyscale / layout
# self-checks with export gated on all passing.
#
# Layout and content are FROZEN from the notebook original. The arrangement is
# mapped 1:1 from the old data coordinates (x 0-16, y 0.25-11.15) onto mm:
#   x_mm = 11.25 * u          y_mm = 13 + 7.25 * (u - 0.55)
# Micro-nudges (<= 0.9 mm, commented at the constants) keep the AR7 type sizes
# clear of neighbouring elements; no box, row, column, link or wording was
# moved or reordered. Style-mandated text changes only:
#   - the mandated unifying headline (14 pt bold) replaces the old in-image
#     "Box 14.7.1 Figure 1: ..." title line (the figure number lives in the
#     manuscript caption, as settled in Block 2);
#   - acronyms spelled out at first occurrence: IoT -> internet of things,
#     AI -> artificial intelligence, AFOLU -> agriculture, forestry and other
#     land use, VRE -> variable renewable energy. The remaining all-caps
#     rendered tokens are panel titles (words, not acronyms) and section tags.
# Run from the "10_Figures" folder:
#   python "_stylerun/box14_7_1_fig1.py"
# No data inputs; writes FigBox14_1_integration_architecture.png/.pdf at the folder root with
# FigBox14_1_integration_architecture_greyscale.png in _qa/greyscale
# (central layout), or into figure/ with no greyscale dump
# (GitHub package layout).
import matplotlib
matplotlib.use("Agg")

import os
import sys
import textwrap

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
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

MM = 25.4
CANVAS = (180, 100)

# ---------------------------------------------------------------- content ---
# FROZEN wording; the Block-5 acronym expansions are the only text changes.
HEADLINE = ('Four technology categories act through four integration modes\n'
            'across sectors, systems and markets')

TECHNOLOGIES = [                     # (category, example technologies)
    ('Sensing and data acquisition', 'internet of things, sensor networks'),
    ('Analytics and optimisation', 'artificial intelligence, machine learning'),
    ('Simulation and planning', 'digital twins'),
    ('Coordination and control', 'platforms, communication networks'),
]
MODES = ['Sector coupling', 'Flexibility provision', 'Real-time balancing',
         'Forecasting and\nanticipatory planning']
SECTORS = ['Energy', 'Transport', 'Buildings', 'Industry',
           'Agriculture, forestry\nand other land use']    # was 'AFOLU'
SYSTEMS = ['Food', 'Water', 'Urban', 'Materials',
           'Flexibility markets\nand platforms']
OUTCOMES = [
    ('System flexibility and variable\nrenewable energy integration',  # 'VRE'
     '(14.7.4)'),
    ('Costs and\npotentials', '(14.8)'),
    ('Systemic risks and\ndistributional implications', '(14.7.5)'),
]

# ---------------------------------------------------------------- palette ---


def tint(hex_colour, white_share=0.85):
    """Blend a hex colour towards white (white_share = share of white)."""
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda v: round(v + (255 - v) * white_share)
    return '#{:02x}{:02x}{:02x}'.format(mix(r), mix(g), mix(b))


# AR7 remap, blues + mustard family only (no red-green anywhere). Fills are
# light tints; identity is carried by the full-hue edges PLUS panel position
# and the bold 10 pt panel titles, so colour is never the only channel. The
# two adjacent same-shape pairs get a large PIL-L edge gap: technologies
# dark_blue 42 vs modes warm_mustard 130 (gap 88); sectors ipcc_blue 134 vs
# systems warm_yellow 175 (gap 41). Modes vs sectors (130 vs 134) are
# non-adjacent, differently sized panels under different titles.
C_TECH = ar7.PALETTE['dark_blue']       # technologies (14.7.1)
C_MODE = ar7.PALETTE['warm_mustard']    # integration modes (14.7.2)
C_SECTOR = ar7.PALETTE['ipcc_blue']     # applications: sectors (14.7.3)
C_SYSTEM = ar7.PALETTE['warm_yellow']   # applications: systems and markets
F_TECH, F_MODE = tint(C_TECH), tint(C_MODE)
F_SECTOR, F_SYSTEM = tint(C_SECTOR), tint(C_SYSTEM)

GREY_TXT = ar7.grey(0.70)     # secondary text (tags, examples, annotations)
GREY_LINE = ar7.grey(0.40)    # collector lines and container edge (old #999999)
GREY_EDGE = ar7.grey(0.60)    # outcomes-strip edge (old #666666)
GREY_ARROW = ar7.grey(0.75)   # trunk arrows (old #444444)
WHITE = '#ffffff'             # zone fills: the old <15%-black washes are not
                              # legal greys (floor grey(0.15)), and grey(0.15)
                              # would sit darker than the box tints (figure-
                              # ground inversion), so zones are white + edged.

# ------------------------------------------------------------- type sizes ---
S_BODY = 7        # box labels, single-line (Arial; category names bold)
S_BODY2 = 7       # two-line box labels. Raised from 6.5 for the FOD review.
S_EX = 7          # example sublines, grey. Raised from 6.5 for the FOD
                  # review; kept in Arial Narrow because regular Arial
                  # overflowed the technology boxes at this size.
S_TAG = 7         # section tags, Arial, grey
S_SUB = 8         # column subheads, Arial bold

# ------------------------------------------------------------ geometry (mm) —


def X(u):
    return 11.25 * u                    # 16 notebook units -> 180 mm


def Y(u):
    return 13.0 + 7.25 * (u - 0.55)     # strip bottom -> 13 mm caption floor


ROWS = [8.6, 7.15, 5.7, 4.25]                     # shared tech/mode rows
COL_MID_Y = Y((ROWS[0] + ROWS[-1]) / 2)
# TECH_H raised from 1.05 u (7.6 mm) on 2026-09-29 so the example
# sublines fit in regular Arial over two lines, and held to 9.0 so the
# four boxes keep a visible 1.5 mm gap against the 10.5 mm row pitch.
# In Arial Narrow the sublines
# fitted on one line; regular Arial needs up to 43.1 mm, wider than the
# 38.2 mm box, and widening the box would push into the modes column.
TECH_X, TECH_W, TECH_H = X(2.2), 11.25 * 3.4, 9.0
MODE_X, MODE_W, MODE_H = X(7.0), 11.25 * 3.0, 7.25 * 0.9
APP_L, APP_R, APP_B, APP_T = X(9.75), X(15.35), Y(3.7), Y(9.7)
SEC_X, SYS_X = X(11.0), X(13.9)
APP_W, APP_H = 11.25 * 2.2, 7.25 * 0.8
APP_ROWS = [Y(8.7 - i * 1.05) for i in range(5)]
COLL = [X(4.3), X(5.1), X(8.85)]                  # collector-line x positions
STRIP = (X(1.0), Y(0.55), 11.25 * 14.35, 7.25 * 2.0)
DOWN_X, DOWN_Y0, DOWN_Y1 = X(7.85), Y(3.45), Y(2.63)
OUT_X = [X(3.39), X(8.18), X(12.96)]
OUT_TEXT_Y = Y(1.45)

# Micro-nudged anchors (old-mapped values in comments): the AR7 sizes need
# slightly taller stacks than the notebook's 12-15 pt design did.
TITLE_Y = 83.2       # panel-title baseline; old 10.15u -> 82.6 (+0.6 mm)
TAG_Y = 79.75        # section tags, va bottom; old 9.78u -> 79.9 (-0.15 mm)
SUB_Y = 77.16        # column subheads; old 9.32u -> 76.6 (+0.6 mm)
OUT_TAG_Y = 14.8     # outcome tags; old 0.92u -> 15.7 (-0.9 mm)
NAME_DU, EX_DU = 0.359, -0.234  # in-box offsets, reset for the taller
                                # technology boxes and two-line sublines
HEADLINE_XY = (2.0, 99.2)      # fig-level, va top (fig14_7_2 convention)

fig = plt.figure(figsize=ar7.fig_mm(*CANVAS))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, CANVAS[0])
ax.set_ylim(0, CANVAS[1])
ax.axis('off')

AUDIT = []     # WCAG + containment audit: {'desc', 'artist', 'bg'}
PAIRS = []     # (upper, lower, desc): vertical gap >= 0.3 mm; 'mm' = fixed edge
BOXES = []     # (rect(x0,y0,w,h), [texts], desc): in-box fit, pad >= 0.3 mm
DRAWN = []     # every line/patch drawn: line-width floor check


def add_text(x, y, s, *, desc, bg, **kw):
    t = ax.text(x, y, s, **kw)
    AUDIT.append({'desc': desc, 'artist': t, 'bg': bg})
    return t


def rbox(x0, y0, w, h, face, edge, lw, rs, z):
    p = FancyBboxPatch((x0, y0), w, h,
                       boxstyle=f'round,pad=0,rounding_size={rs}',
                       facecolor=face, edgecolor=edge, linewidth=lw, zorder=z)
    ax.add_patch(p)
    DRAWN.append(p)
    return p


def line(x0, x1, y0, y1):
    (ln,) = ax.plot([x0, x1], [y0, y1], color=GREY_LINE, lw=0.6,
                    solid_capstyle='butt', zorder=1)
    DRAWN.append(ln)


def arrow(p0, p1):
    a = FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=8,
                        lw=1.3, color=GREY_ARROW, shrinkA=0, shrinkB=0,
                        zorder=3)
    ax.add_patch(a)
    DRAWN.append(a)


# Headline (required wording, bold 14 pt; replaces the old in-image title)
head_t = fig.text(HEADLINE_XY[0] / CANVAS[0], HEADLINE_XY[1] / CANVAS[1],
                  HEADLINE, ha='left', va='top', linespacing=1.12,
                  **ar7.headline_kwargs())
AUDIT.append({'desc': 'headline', 'artist': head_t, 'bg': WHITE})

# --- Technologies (14.7.1) ---
title_tech = add_text(TECH_X, TITLE_Y, 'TECHNOLOGIES',
                      desc='panel title: technologies', bg=WHITE,
                      ha='center', va='bottom', **ar7.subhead_kwargs())
tag_tech = add_text(TECH_X, TAG_Y, '(14.7.1)', desc='tag: technologies',
                    bg=WHITE, ha='center', va='bottom',
                    family='Arial', fontsize=S_TAG, color=GREY_TXT)
for u, (name, examples) in zip(ROWS, TECHNOLOGIES):
    y = Y(u)
    rbox(TECH_X - TECH_W / 2, y - TECH_H / 2, TECH_W, TECH_H,
         F_TECH, C_TECH, 0.9, 1.0, 2)
    nm = add_text(TECH_X, Y(u + NAME_DU), name, desc=f'tech name: {name}',
                  bg=F_TECH, ha='center', va='center', family='Arial',
                  fontsize=S_BODY, fontweight='bold', color=ar7.BLACK,
                  zorder=4)
    exm = add_text(TECH_X, Y(u + EX_DU),
                   '\n'.join(textwrap.wrap(f'({examples})', 26)),
                   desc=f'tech examples: {name}', bg=F_TECH,
                   ha='center', va='center', family='Arial',
                   fontsize=S_EX, color=GREY_TXT, zorder=4, linespacing=1.0)
    BOXES.append(((TECH_X - TECH_W / 2, y - TECH_H / 2, TECH_W, TECH_H),
                  [nm, exm], f'tech box: {name}'))
    PAIRS.append((nm, exm, f'tech name vs examples: {name}'))

# --- Integration modes (14.7.2) ---
title_mode = add_text(MODE_X, TITLE_Y, 'INTEGRATION MODES',
                      desc='panel title: modes', bg=WHITE,
                      ha='center', va='bottom', **ar7.subhead_kwargs())
tag_mode = add_text(MODE_X, TAG_Y, '(14.7.2)', desc='tag: modes', bg=WHITE,
                    ha='center', va='bottom', family='Arial',
                    fontsize=S_TAG, color=GREY_TXT)
for u, mode in zip(ROWS, MODES):
    y = Y(u)
    rbox(MODE_X - MODE_W / 2, y - MODE_H / 2, MODE_W, MODE_H,
         F_MODE, C_MODE, 0.9, 1.0, 2)
    t = add_text(MODE_X, y, mode, desc=f'mode: {mode.splitlines()[0]}',
                 bg=F_MODE, ha='center', va='center', family='Arial',
                 fontsize=S_BODY, color=ar7.BLACK, linespacing=1.1, zorder=4)
    BOXES.append(((MODE_X - MODE_W / 2, y - MODE_H / 2, MODE_W, MODE_H),
                  [t], f'mode box: {mode.splitlines()[0]}'))

# --- Applications (14.7.3): container with sectors, systems and markets ---
rbox(APP_L, APP_B, APP_R - APP_L, APP_T - APP_B, WHITE, GREY_LINE,
     0.65, 1.5, 1)
APP_MID = (APP_L + APP_R) / 2
title_app = add_text(APP_MID, TITLE_Y, 'APPLICATIONS',
                     desc='panel title: applications', bg=WHITE,
                     ha='center', va='bottom', **ar7.subhead_kwargs())
tag_app = add_text(APP_MID, TAG_Y, '(14.7.3)', desc='tag: applications',
                   bg=WHITE, ha='center', va='bottom',
                   family='Arial', fontsize=S_TAG, color=GREY_TXT)
sub_sec = add_text(SEC_X, SUB_Y, 'Sectors', desc='subhead: sectors', bg=WHITE,
                   ha='center', va='center', family='Arial', fontsize=S_SUB,
                   fontweight='bold', color=ar7.BLACK, zorder=4)
sub_sys = add_text(SYS_X, SUB_Y, 'Systems and markets',
                   desc='subhead: systems and markets', bg=WHITE,
                   ha='center', va='center', family='Arial', fontsize=S_SUB,
                   fontweight='bold', color=ar7.BLACK, zorder=4)
for cx, entries, face, edge, kind in (
        (SEC_X, SECTORS, F_SECTOR, C_SECTOR, 'sector'),
        (SYS_X, SYSTEMS, F_SYSTEM, C_SYSTEM, 'system')):
    for y, label in zip(APP_ROWS, entries):
        rbox(cx - APP_W / 2, y - APP_H / 2, APP_W, APP_H,
             face, edge, 0.9, 1.0, 2)
        t = add_text(cx, y, label, desc=f'{kind}: {label.splitlines()[0]}',
                     bg=face, ha='center', va='center', family='Arial',
                     fontsize=S_BODY2 if '\n' in label else S_BODY,
                     color=ar7.BLACK, linespacing=1.0, zorder=4)
        BOXES.append(((cx - APP_W / 2, y - APP_H / 2, APP_W, APP_H),
                      [t], f'{kind} box: {label.splitlines()[0]}'))

# --- Category-level links: bus design (frozen) — collector verticals with a
# stub per box and one trunk arrow per junction, so links read many-to-many.
y_top, y_bot = Y(ROWS[0]), Y(ROWS[-1])
line(COLL[0], COLL[0], y_bot, y_top)
line(COLL[1], COLL[1], y_bot, y_top)
line(COLL[2], COLL[2], y_bot, y_top)
for u in ROWS:
    line(TECH_X + TECH_W / 2, COLL[0], Y(u), Y(u))    # out of technologies
    line(COLL[1], MODE_X - MODE_W / 2, Y(u), Y(u))    # into modes
    line(MODE_X + MODE_W / 2, COLL[2], Y(u), Y(u))    # out of modes
arrow((COLL[0], COL_MID_Y), (COLL[1], COL_MID_Y))
arrow((COLL[2], COL_MID_Y), (APP_L, COL_MID_Y))

# Annotations, 7.5 pt in the recorded annotation font (Arial Italic)
ann_enable = add_text((COLL[0] + COLL[1]) / 2, COL_MID_Y + 2.03, 'enable',
                      desc='annotation: enable', bg=WHITE,
                      ha='center', va='bottom', color=GREY_TXT,
                      linespacing=1.1, zorder=4, **ar7.annotation_kwargs())
ann_operate = add_text((COLL[2] + APP_L) / 2, COL_MID_Y + 2.03,
                       'operate\nacross', desc='annotation: operate across',
                       bg=WHITE, ha='center', va='bottom', color=GREY_TXT,
                       linespacing=1.1, zorder=4, **ar7.annotation_kwargs())
ANNOT_BANDS = [(ann_enable, (COLL[0], COLL[1]), 'enable'),
               (ann_operate, (COLL[2], APP_L), 'operate across')]

# --- Integration outcomes and trade-offs strip ---
arrow((DOWN_X, DOWN_Y0), (DOWN_X, DOWN_Y1))
rbox(*STRIP, WHITE, GREY_EDGE, 0.9, 1.5, 1)
strip_title = add_text(X(8.1), Y(2.2), 'INTEGRATION OUTCOMES AND TRADE-OFFS',
                       desc='panel title: outcomes', bg=WHITE,
                       ha='center', va='center', zorder=4,
                       **ar7.subhead_kwargs())
out_pairs = []
for cx, (outcome, tag) in zip(OUT_X, OUTCOMES):
    ot = add_text(cx, OUT_TEXT_Y, outcome,
                  desc=f'outcome: {outcome.splitlines()[0]}', bg=WHITE,
                  ha='center', va='center', family='Arial', fontsize=S_BODY,
                  color=ar7.BLACK, linespacing=1.1, zorder=4)
    tg = add_text(cx, OUT_TAG_Y, tag, desc=f'outcome tag: {tag}', bg=WHITE,
                  ha='center', va='center', family='Arial',
                  fontsize=S_TAG, color=GREY_TXT, zorder=4)
    out_pairs.append((ot, tg))
    PAIRS += [(strip_title, ot, f'strip title vs outcome: {tag}'),
              (ot, tg, f'outcome text vs tag: {tag}'),
              (tg, ('mm', STRIP[1]), f'outcome tag vs strip bottom: {tag}')]

# Remaining vertical-stack pairs (top of canvas downwards)
for t, name in ((title_tech, 'technologies'), (title_mode, 'modes'),
                (title_app, 'applications')):
    PAIRS.append((head_t, t, f'headline vs title: {name}'))
PAIRS += [(title_tech, tag_tech, 'title vs tag: technologies'),
          (title_mode, tag_mode, 'title vs tag: modes'),
          (title_app, tag_app, 'title vs tag: applications'),
          (tag_app, ('mm', APP_T), 'applications tag vs container top'),
          (('mm', APP_T), sub_sec, 'container top vs subhead: sectors'),
          (('mm', APP_T), sub_sys, 'container top vs subhead: systems'),
          (sub_sec, ('mm', APP_ROWS[0] + APP_H / 2),
           'subhead vs first box: sectors'),
          (sub_sys, ('mm', APP_ROWS[0] + APP_H / 2),
           'subhead vs first box: systems'),
          (('mm', STRIP[1] + STRIP[3]), strip_title,
           'strip top vs strip title'),
          (('mm', DOWN_Y1), strip_title, 'down-arrow tip vs strip title'),
          (ann_enable, ('mm', COL_MID_Y + 0.5), 'enable vs trunk arrow'),
          (ann_operate, ('mm', COL_MID_Y + 0.5),
           'operate across vs trunk arrow')]

# ---------------------------------------------------------------- checks ----


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

    def edge_mm(item, which):
        if isinstance(item, tuple) and item[0] == 'mm':
            return item[1]
        x0, x1, y0, y1 = _ext_mm(item, ren)
        return y0 if which == 'bottom' else y1

    # 1) fonts: every rendered text resolves to an Arial-family file
    families = set()
    texts = [t for t in fig.findobj(mtext.Text) if t.get_text().strip()]
    for t in texts:
        fname = os.path.basename(font_manager.findfont(t.get_fontproperties()))
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

    # 4) canvas containment for every audited text
    for a in AUDIT:
        x0, x1, y0, y1 = _ext_mm(a['artist'], ren)
        if (x0 < -0.2 or x1 > CANVAS[0] + 0.2
                or y0 < -0.2 or y1 > CANVAS[1] + 0.2):
            fails.append(f"CANVAS: {a['desc']} "
                         f'[{x0:.1f},{x1:.1f},{y0:.1f},{y1:.1f}] off-canvas')

    # 5) in-box fit: every box label inside its patch with >= 0.3 mm padding
    worst_pad = 99.0
    for (bx, by, bw, bh), arts, desc in BOXES:
        for t in arts:
            x0, x1, y0, y1 = _ext_mm(t, ren)
            pad = min(x0 - bx, bx + bw - x1, y0 - by, by + bh - y1)
            worst_pad = min(worst_pad, pad)
            if pad < 0.3:
                fails.append(f'IN-BOX: {desc} pad {pad:.2f} mm')
    print(f'in-box padding, worst: {worst_pad:.2f} mm (floor 0.3)')

    # 6) vertical gaps down the stacks
    for upper, lower, desc in PAIRS:
        gap = edge_mm(upper, 'bottom') - edge_mm(lower, 'top')
        print(f'gap: {desc}: {gap:.2f} mm')
        if gap < 0.3:
            fails.append(f'OVERLAP: {desc} gap {gap:.2f} mm')

    # 7) annotations sit clear of the collector verticals / container edge
    for t, (bl, br), desc in ANNOT_BANDS:
        x0, x1, _, _ = _ext_mm(t, ren)
        clear = min(x0 - bl, br - x1)
        print(f'annotation clearance: {desc}: {clear:.2f} mm')
        if clear < 0.3:
            fails.append(f'ANNOT: {desc} clearance {clear:.2f} mm')

    # 8) line-width floors on everything drawn (all lines here are grey or
    # full-hue edges; hold them all to the coloured floor 0.567 pt)
    lws = [d.get_linewidth() for d in DRAWN]
    print(f'line widths: min {min(lws):.3f} pt '
          f'(floors: colour {ar7.LW_COLOUR_MIN}, black {ar7.LW_BLACK_MIN})')
    if min(lws) < ar7.LW_COLOUR_MIN:
        fails.append(f'LINEWIDTH: {min(lws):.3f} < {ar7.LW_COLOUR_MIN}')

    # 9) greyscale: full-hue edges carry group identity; the two adjacent
    # same-shape pairs must separate by >= 30 PIL-L. Modes vs sectors (gap 4)
    # are non-adjacent, differently sized panels under different bold titles,
    # so position and titles — not colour — distinguish them.
    edges = {'technologies dark_blue': C_TECH, 'modes warm_mustard': C_MODE,
             'sectors ipcc_blue': C_SECTOR, 'systems warm_yellow': C_SYSTEM}
    Ls = {k: _pil_L(v) for k, v in edges.items()}
    print('greyscale L (edges):',
          ', '.join(f'{k} {v}' for k, v in Ls.items()))
    for a, b in (('technologies dark_blue', 'modes warm_mustard'),
                 ('sectors ipcc_blue', 'systems warm_yellow')):
        gap = abs(Ls[a] - Ls[b])
        print(f'greyscale gap: {a} vs {b}: {gap}')
        if gap < 30:
            fails.append(f'GREYSCALE: {a} vs {b} gap {gap} (< 30)')

    for f_ in fails:
        print('FAIL', f_)
    return not fails


ok = run_checks()
if not ok:
    sys.exit(1)

ar7.export(fig, os.path.join(OUT_DIR, 'FigBox14_1_integration_architecture'))
if GREY_DIR:
    os.makedirs(GREY_DIR, exist_ok=True)
    print('greyscale dump:',
          ar7.greyscale_dump(fig, os.path.join(GREY_DIR, 'FigBox14_1_integration_architecture')))
print(f'exported FigBox14_1_integration_architecture.png/.pdf '
      f'({CANVAS[0]}x{CANVAS[1]} mm, 300 dpi)')
