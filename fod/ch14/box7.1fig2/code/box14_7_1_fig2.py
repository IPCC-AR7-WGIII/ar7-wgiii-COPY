#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# box14_7_1_fig2.py — standalone export script for FigBox14_2_net_effect
# Extracted from ch14_schematics.ipynb (notebook retired as build system).
# AR7 restyle 2026-07-31 (Block 6): styled via _stylerun/ar7_style.py — IPCC
# palette (blues + mustard family + settled grey, no red-green anywhere),
# Arial/Arial Narrow type scale, 180x100 mm canvas, 300 dpi export, WCAG /
# greyscale / layout self-checks with export gated on all passing.
#
# Layout and content are FROZEN from the notebook original. The arrangement is
# mapped 1:1 from the old data coordinates (x 0-12, y 0.25-5.6) onto mm:
#   x_mm = 15 * u          y_mm = 13 + 15 * (u - 0.35)
# so the net-effect box bottom (old y 0.35) lands on the 13 mm caption floor.
# Micro-nudges (<= 0.9 mm, commented at the constants) keep the AR7 type sizes
# clear of the counterfactual baseline; no arrow, row or wording was moved or
# reordered. Style-mandated changes only:
#   - the mandated headline (14 pt bold) replaces the old in-image
#     "Box 14.7.1 Figure 2: ..." title line (the figure number lives in the
#     manuscript caption, as settled in Block 2);
#   - dashed-element convention UNCHANGED: dashes carry the uncertainty
#     meaning (rebound arrow, systemic arrow, counterfactual baseline);
#   - the systemic-effects arrow design is settled and NOT redrawn
#     (bidirectional '<|-|>', dashed, grey);
#   - acronym scan of all rendered text: no acronyms occur, nothing to expand.
# Run from the "10_Figures" folder:
#   python "_stylerun/box14_7_1_fig2.py"
# No data inputs; writes FigBox14_2_net_effect.png/.pdf at the folder root with
# FigBox14_2_net_effect_greyscale.png in _qa/greyscale
# (central layout), or into figure/ with no greyscale dump
# (GitHub package layout).
import matplotlib
matplotlib.use("Agg")

import os
import sys

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
# FROZEN wording from the notebook original; only the old title line is
# replaced by the mandated headline (line break inserted for the 180 mm width).
HEADLINE = ('Whether digitalisation cuts emissions is a net balance\n'
            'of direct, application-level and economy-wide effects')

BASELINE_LABEL = 'Counterfactual baseline:\nemissions without digitalisation'
DIR_LEFT = 'effects decreasing emissions'
DIR_RIGHT = 'effects increasing emissions'
NET_TEXT = ('Net effect: the sum of these effects measured against the '
            'counterfactual;\nsign and magnitude vary by application, '
            'region and time.')

# ---------------------------------------------------------------- palette ---
# AR7 remap of the effect categories. The old scheme coded direction as
# bluish-green (decreasing) vs vermillion (increasing) — a red-green pairing,
# which the guide bans for a critical distinction. New scheme, four distinct
# PIL-L lightnesses (all 6 pairwise gaps >= 43):
#   application-level  dark_blue    L 42   (decreasing side, solid)
#   direct             warm_mustard L 130  (increasing side, solid)
#   rebound + induced  warm_yellow  L 175  (increasing side, dashed)
#   systemic           grey(2/3)    L 85   (both directions, dashed — the
#                      settled grey '#555555' of the original, kept verbatim)
# Colour is never the only channel: direction is drawn by the arrow geometry
# and named by the two axis labels, and dashes carry uncertainty as before.
C_APP = ar7.PALETTE['dark_blue']
C_DIRECT = ar7.PALETTE['warm_mustard']
C_REBOUND = ar7.PALETTE['warm_yellow']
C_SYSTEMIC = ar7.grey(2 / 3)   # == '#555555', the original systemic grey

# The original structural greys are all exact ar7 greys — mapped, not changed:
GREY_TXT = ar7.grey(0.70)      # effect details, direction labels
GREY_AXIS = ar7.grey(0.40)     # direction axis (old '#999999')
GREY_BASE = ar7.grey(0.80)     # baseline line + label (old '#333333')
GREY_EDGE = ar7.grey(0.60)     # net-effect box edge (old '#666666')
WHITE = '#ffffff'              # net-box fill: the old '#f5f5f5' wash is below
                               # the grey(0.15) print floor, so the box is
                               # white + edged (Block-5 precedent).

# ------------------------------------------------------------- type sizes ---
S_NAME = 8       # effect names, Arial bold, black
S_DET = 7        # effect details '(...)', Arial, grey
S_BASE = 8       # counterfactual baseline label, Arial, grey(0.80)
S_NET = 8        # net-effect statement, Arial, black
# direction labels use ar7.annotation_kwargs(): 7.5 pt Arial Italic

# ------------------------------------------------------------ line widths ---
LW_ARROW = 2.0     # all four effect arrows equal, so no magnitude is implied
MS_ARROW = 10      # arrow-head mutation scale (old 18, scaled to the canvas)
LW_AXIS = 0.9      # direction axis
LW_BASELINE = 1.2  # counterfactual baseline (dashed)
LW_BOX = 0.9       # net-effect box edge
HALF_BASE = LW_BASELINE * 0.3528 / 2   # baseline half-width in mm

# ------------------------------------------------------------ geometry (mm) —


def X(u):
    return 15.0 * u                     # 12 notebook units -> 180 mm


def Y(u):
    return 13.0 + 15.0 * (u - 0.35)     # net-box bottom -> 13 mm caption floor


BASE_X = X(6.0)                                   # counterfactual baseline
DIR_Y = Y(4.25)                                   # direction axis
DIR_X0, DIR_X1 = X(1.2), X(10.8)
DIR_LBL_Y = Y(4.33)
DIR_LBL_XL, DIR_LBL_XR = X(2.9), X(9.1)
LINE_Y0, LINE_Y1 = Y(2.05), Y(4.55)               # baseline line span
BASE_LBL_Y = Y(4.68)
LEFT_TIP, RIGHT_TIP = X(3.4), X(8.6)              # effect-arrow tips
BOTH_X0, BOTH_X1 = X(4.2), X(7.8)                 # systemic arrow span
NAME_DY, DET_DY = 15.0 * 0.12, -15.0 * 0.14       # label offsets off the shaft
NET_BOX = (X(0.8), Y(0.35), 15.0 * 10.4, 15.0 * 0.75)
NET_TXT_Y = Y(0.725)

# Micro-nudged label anchors (old-mapped values in comments): the 8 pt bold
# names sit 0.9 mm further from the baseline than the old 11.5 pt design did,
# keeping >= 0.3 mm clearance to the dashed line; nothing else moved.
TITLE_X_LEFT = 69.6      # old 4.7u -> 70.5 (-0.9 mm)
TITLE_X_RIGHT = 112.65   # old 7.45u -> 111.75 (+0.9 mm, both right-side rows)
SUB_X_LEFT = X(5.85)     # detail anchor, ha right (unchanged)
SUB_X_RIGHT = X(6.2)     # detail anchor, ha left (unchanged)
HEADLINE_XY = (2.0, 99.2)   # fig-level, va top (fig14_7_2 convention)

# Effect rows, FROZEN order and directions (name, detail, direction, colour,
# linestyle, old y). Dash styles are the original convention: uncertainty.
EFFECTS = [
    ('Application-level effects',
     'optimisation, substitution, cross-sectoral integration',
     'left', C_APP, 'solid', 3.7),
    ('Direct effects',
     'energy and materials of digital infrastructure',
     'right', C_DIRECT, 'solid', 3.0),
    ('Rebound and induced effects',
     'demand growth from cheaper and faster services',
     'right', C_REBOUND, 'dashed', 2.3),
    ('Systemic and structural effects',
     'reorganisation of behaviour, markets and infrastructure',
     'both', C_SYSTEMIC, 'dashed', 1.6),
]

fig = plt.figure(figsize=ar7.fig_mm(*CANVAS))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, CANVAS[0])
ax.set_ylim(0, CANVAS[1])
ax.axis('off')

AUDIT = []     # WCAG + containment audit: {'desc', 'artist', 'bg'}
PAIRS = []     # (upper, lower, desc): vertical gap >= 0.3 mm; 'mm' = fixed edge
BOXES = []     # (rect(x0,y0,w,h), [texts], desc): in-box fit, pad >= 0.3 mm
DRAWN = []     # every line/patch drawn: line-width floor check
BASE_CLEAR = []   # (text, 'left'|'right', desc): clearance to baseline >= 0.3


def add_text(x, y, s, *, desc, bg, **kw):
    t = ax.text(x, y, s, **kw)
    AUDIT.append({'desc': desc, 'artist': t, 'bg': bg})
    return t


# Headline (required wording, bold 14 pt; replaces the old in-image title)
head_t = fig.text(HEADLINE_XY[0] / CANVAS[0], HEADLINE_XY[1] / CANVAS[1],
                  HEADLINE, ha='left', va='top', linespacing=1.12,
                  **ar7.headline_kwargs())
AUDIT.append({'desc': 'headline', 'artist': head_t, 'bg': WHITE})

# --- Direction axis (no scale: directions only; solid — direction is not
# uncertain, so it takes no dashes) ---
dir_arrow = FancyArrowPatch((DIR_X0, DIR_Y), (DIR_X1, DIR_Y),
                            arrowstyle='<->', mutation_scale=7,
                            lw=LW_AXIS, color=GREY_AXIS, shrinkA=0, shrinkB=0,
                            zorder=2)
ax.add_patch(dir_arrow)
DRAWN.append(dir_arrow)
dir_l = add_text(DIR_LBL_XL, DIR_LBL_Y, DIR_LEFT,
                 desc='direction label: decreasing', bg=WHITE,
                 ha='center', va='bottom', color=GREY_TXT, zorder=4,
                 **ar7.annotation_kwargs())
dir_r = add_text(DIR_LBL_XR, DIR_LBL_Y, DIR_RIGHT,
                 desc='direction label: increasing', bg=WHITE,
                 ha='center', va='bottom', color=GREY_TXT, zorder=4,
                 **ar7.annotation_kwargs())

# --- Counterfactual baseline (dashed: the counterfactual is unobserved;
# shortened in the original so no text crosses it — preserved) ---
(base_ln,) = ax.plot([BASE_X, BASE_X], [LINE_Y0, LINE_Y1], color=GREY_BASE,
                     lw=LW_BASELINE, linestyle=(0, (3.5, 2.3)),
                     solid_capstyle='butt', zorder=2)
DRAWN.append(base_ln)
base_lbl = add_text(BASE_X, BASE_LBL_Y, BASELINE_LABEL,
                    desc='baseline label', bg=WHITE, ha='center', va='bottom',
                    family='Arial', fontsize=S_BASE, color=GREY_BASE,
                    linespacing=1.15, zorder=4)

# --- Effect arrows: equal lengths and weights by design, so no magnitude is
# implied. Labels sit clear of the baseline (original standing rule 5). ---
row_arts = []    # (name_text, arrow, detail_text) per row, for the gap checks
for name, detail, direction, colour, style, u in EFFECTS:
    y = Y(u)
    if direction == 'left':
        start, end, arrowstyle = (BASE_X, y), (LEFT_TIP, y), '-|>'
        title_x, title_ha = TITLE_X_LEFT, 'center'
        sub_x, sub_ha = SUB_X_LEFT, 'right'
    elif direction == 'right':
        start, end, arrowstyle = (BASE_X, y), (RIGHT_TIP, y), '-|>'
        title_x, title_ha = TITLE_X_RIGHT, 'center'
        sub_x, sub_ha = SUB_X_RIGHT, 'left'
    else:   # the settled systemic-effects arrow: bidirectional, dashed, grey
        start, end, arrowstyle = (BOTH_X0, y), (BOTH_X1, y), '<|-|>'
        title_x, title_ha = BASE_X, 'center'
        sub_x, sub_ha = BASE_X, 'center'
    arr = FancyArrowPatch(start, end, arrowstyle=arrowstyle, color=colour,
                          lw=LW_ARROW, mutation_scale=MS_ARROW,
                          linestyle=style, shrinkA=0, shrinkB=0, zorder=3)
    ax.add_patch(arr)
    DRAWN.append(arr)
    nm = add_text(title_x, y + NAME_DY, name, desc=f'name: {name}', bg=WHITE,
                  ha=title_ha, va='bottom', family='Arial', fontsize=S_NAME,
                  fontweight='bold', color=ar7.BLACK, zorder=4)
    det = add_text(sub_x, y + DET_DY, f'({detail})', desc=f'detail: {name}',
                   bg=WHITE, ha=sub_ha, va='top', family='Arial',
                   fontsize=S_DET, color=GREY_TXT, zorder=4)
    row_arts.append((nm, arr, det))
    PAIRS += [(nm, arr, f'name vs arrow: {name}'),
              (arr, det, f'arrow vs detail: {name}')]
    if direction == 'left':
        BASE_CLEAR += [(nm, 'left', f'name vs baseline: {name}'),
                       (det, 'left', f'detail vs baseline: {name}')]
    elif direction == 'right':
        BASE_CLEAR += [(nm, 'right', f'name vs baseline: {name}'),
                       (det, 'right', f'detail vs baseline: {name}')]

# --- Net-effect statement (author-approved exception to the no-sentence
# rule; wording frozen) ---
net_box = FancyBboxPatch((NET_BOX[0], NET_BOX[1]), NET_BOX[2], NET_BOX[3],
                         boxstyle='round,pad=0,rounding_size=1.5',
                         facecolor=WHITE, edgecolor=GREY_EDGE,
                         linewidth=LW_BOX, zorder=1)
ax.add_patch(net_box)
DRAWN.append(net_box)
net_t = add_text(BASE_X, NET_TXT_Y, NET_TEXT, desc='net-effect statement',
                 bg=WHITE, ha='center', va='center', family='Arial',
                 fontsize=S_NET, color=ar7.BLACK, linespacing=1.15, zorder=4)
BOXES.append((NET_BOX, [net_t], 'net-effect box'))

# Vertical-stack pairs (top of canvas downwards). The direction labels and the
# baseline label do not overlap horizontally, so only true stacks are paired.
PAIRS += [(head_t, base_lbl, 'headline vs baseline label'),
          (base_lbl, ('mm', LINE_Y1), 'baseline label vs baseline line top'),
          (dir_l, dir_arrow, 'direction label (left) vs direction axis'),
          (dir_r, dir_arrow, 'direction label (right) vs direction axis'),
          (row_arts[3][2], ('mm', NET_BOX[1] + NET_BOX[3]),
           'systemic detail vs net-box top'),
          (('mm', LINE_Y0), row_arts[3][0],
           'baseline line bottom vs systemic name')]
for above, below in ((0, 1), (1, 2), (2, 3)):
    PAIRS.append((row_arts[above][2], row_arts[below][0],
                  f'row {above + 1} detail vs row {below + 1} name'))
# Direction labels clear the baseline horizontally by construction; audited:
BASE_CLEAR += [(dir_l, 'left', 'direction label (left) vs baseline'),
               (dir_r, 'right', 'direction label (right) vs baseline')]

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

    # 5) in-box fit: the net-effect text inside its patch, >= 0.3 mm padding
    worst_pad = 99.0
    for (bx, by, bw, bh), arts, desc in BOXES:
        for t in arts:
            x0, x1, y0, y1 = _ext_mm(t, ren)
            pad = min(x0 - bx, bx + bw - x1, y0 - by, by + bh - y1)
            worst_pad = min(worst_pad, pad)
            if pad < 0.3:
                fails.append(f'IN-BOX: {desc} pad {pad:.2f} mm')
    print(f'in-box padding, worst: {worst_pad:.2f} mm (floor 0.3)')

    # 6) vertical gaps down the stacks (arrow extents include the heads)
    for upper, lower, desc in PAIRS:
        gap = edge_mm(upper, 'bottom') - edge_mm(lower, 'top')
        print(f'gap: {desc}: {gap:.2f} mm')
        if gap < 0.3:
            fails.append(f'OVERLAP: {desc} gap {gap:.2f} mm')

    # 7) no text crosses the counterfactual baseline (original standing rule):
    # horizontal clearance to the dashed line >= 0.3 mm, ink included
    for t, side, desc in BASE_CLEAR:
        x0, x1, _, _ = _ext_mm(t, ren)
        clear = (BASE_X - HALF_BASE - x1 if side == 'left'
                 else x0 - BASE_X - HALF_BASE)
        print(f'baseline clearance: {desc}: {clear:.2f} mm')
        if clear < 0.3:
            fails.append(f'BASELINE: {desc} clearance {clear:.2f} mm')

    # 8) line-width floors on everything drawn (grey structural lines are
    # held to the coloured floor 0.567 pt as well, like Block 5)
    lws = [d.get_linewidth() for d in DRAWN]
    print(f'line widths: min {min(lws):.3f} pt '
          f'(floors: colour {ar7.LW_COLOUR_MIN}, black {ar7.LW_BLACK_MIN})')
    if min(lws) < ar7.LW_COLOUR_MIN:
        fails.append(f'LINEWIDTH: {min(lws):.3f} < {ar7.LW_COLOUR_MIN}')

    # 9) greyscale: the four effect categories must separate in print; every
    # pairwise PIL-L gap >= 30 (dashes and geometry are the extra channels)
    cats = {'application dark_blue': C_APP,
            'direct warm_mustard': C_DIRECT,
            'rebound warm_yellow': C_REBOUND,
            'systemic grey': C_SYSTEMIC}
    Ls = {k: _pil_L(v) for k, v in cats.items()}
    print('greyscale L (arrows):',
          ', '.join(f'{k} {v}' for k, v in sorted(Ls.items(),
                                                  key=lambda kv: kv[1])))
    names = list(cats)
    min_gap = 255
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            gap = abs(Ls[a] - Ls[b])
            min_gap = min(min_gap, gap)
            if gap < 30:
                fails.append(f'GREYSCALE: {a} vs {b} gap {gap} (< 30)')
    print(f'greyscale min pairwise gap: {min_gap} (floor 30)')

    for f_ in fails:
        print('FAIL', f_)
    return not fails


ok = run_checks()
if not ok:
    sys.exit(1)

ar7.export(fig, os.path.join(OUT_DIR, 'FigBox14_2_net_effect'))
if GREY_DIR:
    os.makedirs(GREY_DIR, exist_ok=True)
    print('greyscale dump:',
          ar7.greyscale_dump(fig, os.path.join(GREY_DIR, 'FigBox14_2_net_effect')))
print(f'exported FigBox14_2_net_effect.png/.pdf '
      f'({CANVAS[0]}x{CANVAS[1]} mm, 300 dpi)')
