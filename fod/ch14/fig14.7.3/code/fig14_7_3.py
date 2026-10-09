#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# fig14_7_3.py — standalone export script for Fig14_7_3_modelled_system_value
# Extracted from ch14_schematics.ipynb (notebook retired as build system).
# AR7 restyle 2026-07-31: styled via _stylerun/ar7_style.py (IPCC palette,
# Arial/Arial Narrow, 180x100 mm canvas, 300 dpi export, WCAG/greyscale checks).
# Run from the "10_Figures" folder:  python "_stylerun/fig14_7_3.py"
# Entries are hard-coded from e2_modelled_value_data.csv (29 July 2026 audit),
# exactly as in the notebook original — no runtime CSV read. Writes
# Fig14_7_3_modelled_system_value.png/.pdf beside the CSV at the folder
# root, with _greyscale.png in _qa/greyscale (central layout); or
# into figure/ with no greyscale dump (GitHub package layout).
import matplotlib
matplotlib.use("Agg")

import os
import sys

import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from matplotlib import font_manager

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

# ---------------------------------------------------------------- content ---
# Content is FROZEN: every entry, value and citation below is verbatim from
# the notebook original (mapped from e2_modelled_value_data.csv, 29 July
# 2026). The Mayer et al. sector-boundary entry stays. Acronym scan of
# rendered text: IEA is an organisation's citation name (kept as a citation,
# as in Blocks 2-3); "%" / "per cent" are units (exempt); no other all-caps
# tokens render.
HEADLINE = ('Modelled system value of digitally-enabled flexibility is\n'
            'consistently positive. Measured outcomes have yet to be reported.')
XLABEL = ('System cost reduction (per cent)\n'
          'On a logarithmic scale, equal spacing means equal multiples.')
# S10: the axis label names the scale; this line says how to read it,
# which D3 asks of an annotation on a complex part. It sits in the strip
# freed by raising the axes for the caption band (S12).
# Range-vs-point key, worded as in the settled Block-7 caption ("bars span
# reported ranges, point markers denote single reported values")
NOTE = 'Bars span reported ranges; point markers denote single reported values.'

# (entry label, boundary class, low, high, kind, value label)
ENTRIES = [
    # CSV row: Coordination value / Garcia Arenas et al. 2022, Energies 15(7):2638 (attribution corrected per audit)
    ('Garcia Arenas et al. (2022)', 'city', 23.0, 30.9, 'range', '23 to 30.9%'),
    # CSV row: System cost reduction / Mayer et al. 2024 note field (12 to 20 per cent of
    # industry-related energy costs): the sector-boundary reporting of the same study
    ('Mayer et al. (2024)', 'sector', 12.0, 20.0, 'range', '12 to 20%'),
    # CSV row: System cost reduction / IEA Scaling Up Demand Flexibility (grey literature)
    ('IEA (2026b)', 'national', 10.0, 10.0, 'point', 'up to 10%'),
    # CSV row: System cost reduction / Mayer et al. 2024 (total energy-system cost)
    ('Mayer et al. (2024)', 'national', 2.0, 4.4, 'range', '2 to 4.4%'),
    # CSV row: Coordination value / Burghardt, Schaefer and Weidlich 2025, iScience 28:113381
    ('Burghardt et al. (2025)', 'national', 0.3, 0.3, 'point', '0.3%'),
]
BOUNDARY_NAME = {
    'city': 'City energy system',
    'sector': 'Sector (industry-related energy costs)',
    'national': 'National energy system',
}

# Palette remap (AR7): the three system boundaries get three distinct
# lightnesses AND three marker shapes, so colour is never the only channel.
# national = dark_blue (3 of 5 entries; diamond), city = ipcc_blue (circle);
# the sector boundary — a different denominator (industry-related energy
# costs, not total system cost) — sits apart from the blues in warm_yellow
# (square). No red-green pairing. PIL greyscale L: dark_blue 42 / ipcc_blue
# 134 / warm_yellow 175 — gaps >= 30. Boundary is also named in text on
# every row (sublabel), so no legend box is needed.
BOUNDARY_COLOUR = {
    'city': ar7.PALETTE['ipcc_blue'],
    'sector': ar7.PALETTE['warm_yellow'],
    'national': ar7.PALETTE['dark_blue'],
}
BOUNDARY_MARKER = {                 # marker, size (pt)
    'city': ('o', 5.5),
    'sector': ('s', 5.0),
    'national': ('D', 4.5),
}
LW_RANGE = 2.2                      # range bars — >= 0.567 pt colour floor
MEW = 0.4                           # black marker edges — >= 0.255 pt floor
GREY_GRID = ar7.grey(0.20)          # x gridlines
GREY_SUB = ar7.grey(0.70)           # boundary sublabels (8.45:1 on white)

# ------------------------------------------------------------ geometry (mm) —
CANVAS = (180, 100)
AX_MM = (49.0, 25.0, 127.0, 59.0)   # left, bottom, width, height in mm
LABEL_X_MM = 2.0                    # left edge of the entry-label column
XLIM = (0.2, 80)
XTICKS = [0.3, 1, 3, 10, 30]
YLIM = (-0.6, 4.6)                  # entry rows at y = 4 (top) .. 0 (bottom)

fig = plt.figure(figsize=ar7.fig_mm(*CANVAS))
ax = fig.add_axes([AX_MM[0] / CANVAS[0], AX_MM[1] / CANVAS[1],
                   AX_MM[2] / CANVAS[0], AX_MM[3] / CANVAS[1]])
ax.set_xscale('log')
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_axisbelow(True)

AUDIT = []          # text audit: WCAG entries (+ measured containment)
PAIRS = []          # (upper, lower, desc): vertical-gap checks, mm
SEPARATE = []       # (a, b, desc): text extents that must not intersect
RANGE_LINES = []    # coloured range bars (linewidth floor check)
MARKER_LINES = []   # marker artists (edge-width floor check)


def add_text(*args, desc, bg='#ffffff', **kw):
    t = ax.text(*args, **kw)
    AUDIT.append({'desc': desc, 'artist': t, 'bg': bg})
    return t


# Headline (required wording, bold 14 pt; replaces the old in-image
# "Figure 14.7.3: ..." title line — figure number lives in the manuscript
# caption, as settled in Block 2)
head_t = fig.text(LABEL_X_MM / CANVAS[0], 98.5 / CANVAS[1], HEADLINE,
                  ha='left', va='top', linespacing=1.12,
                  **ar7.headline_kwargs())
AUDIT.append({'desc': 'headline', 'artist': head_t, 'bg': '#ffffff'})

# Entry rows: direct labels in a left column (citation plain Arial 8 pt,
# boundary sublabel 7 pt Arial grey), bar/marker and value label to
# the right. Replaces the original y-tick labels and legend box.
lab_tr = mtransforms.blended_transform_factory(fig.transFigure, ax.transData)
cit_texts, sub_texts, val_texts = [], [], []
for i, (label, boundary, low, high, kind, value_label) in enumerate(ENTRIES):
    y = len(ENTRIES) - 1 - i
    colour = BOUNDARY_COLOUR[boundary]
    marker, ms = BOUNDARY_MARKER[boundary]
    if kind == 'range':
        ln, = ax.plot([low, high], [y, y], color=colour, lw=LW_RANGE,
                      solid_capstyle='butt', zorder=3)
        RANGE_LINES.append(ln)
        mx = [low, high]            # boundary marker at both range ends
    else:
        mx = [high]                 # single reported value
    mk, = ax.plot(mx, [y] * len(mx), linestyle='none', marker=marker, ms=ms,
                  mfc=colour, mec=ar7.BLACK, mew=MEW, zorder=4)
    MARKER_LINES.append(mk)
    cit_texts.append(add_text(
        LABEL_X_MM / CANVAS[0], y + 0.05, label, transform=lab_tr,
        desc=f'entry label: {label}', ha='left', va='bottom',
        family='Arial', fontsize=ar7.SIZE_AXIS_LABEL, color=ar7.BLACK,
        zorder=5))
    sub_texts.append(add_text(
        LABEL_X_MM / CANVAS[0], y - 0.05, BOUNDARY_NAME[boundary],
        transform=lab_tr, desc=f'boundary sublabel: {boundary} (row {i})',
        ha='left', va='top', family='Arial', fontsize=ar7.SIZE_TICK,
        color=GREY_SUB, zorder=5))
    val_texts.append(add_text(
        high * 1.12, y, value_label, desc=f'value label: {value_label}',
        ha='left', va='center', family='Arial',
        fontsize=ar7.SIZE_ANNOTATION, color=ar7.BLACK, zorder=5))

# Range-vs-point key in the free lower-right area; annotation font recorded
# in stylerun_state.md (Arial Italic), 7.5 pt
note_t = add_text(76, -0.42, NOTE, desc='range/point note', ha='right',
                  va='center', color=ar7.BLACK, zorder=5,
                  **ar7.annotation_kwargs())

# Axes furniture: ticks 7 pt Arial Narrow, axis label 8 pt Arial, light grid
ax.set_yticks([])
ax.set_xticks(XTICKS)
ax.set_xticklabels([str(t) for t in XTICKS])
ax.minorticks_off()
plt.setp(ax.get_xticklabels(), family=ar7.FONT_TICK, fontsize=ar7.SIZE_TICK)
ax.grid(axis='x', color=GREY_GRID, linewidth=ar7.LW_BLACK_MIN)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_linewidth(ar7.LW_BLACK_MIN)
ax.set_xlabel(XLABEL, family='Arial', fontsize=ar7.SIZE_AXIS_LABEL,
              color=ar7.BLACK)

# vertical stack: headline / rows (citation over sublabel) / note
PAIRS.append((head_t, cit_texts[0], 'headline vs top entry label'))
for i in range(len(ENTRIES) - 1):
    PAIRS.append((sub_texts[i], cit_texts[i + 1],
                  f'row {i} sublabel vs row {i + 1} label'))
PAIRS.append((val_texts[-1], note_t, 'bottom value label vs note'))
SEPARATE += [(note_t, val_texts[-1], 'note vs 0.3% label'),
             (note_t, val_texts[-2], 'note vs 2-4.4% label'),
             (note_t, sub_texts[-1], 'note vs bottom sublabel')]

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

    # 4) containment (canvas), vertical gaps, rectangle separation
    for a in AUDIT:
        x0, x1, y0, y1 = _ext_mm(a['artist'], ren)
        if x0 < -0.2 or x1 > CANVAS[0] + 0.2 or y0 < -0.2 or y1 > CANVAS[1] + 0.2:
            fails.append(f"CANVAS: {a['desc']} "
                         f'[{x0:.1f},{x1:.1f},{y0:.1f},{y1:.1f}] off-canvas')
    for upper, lower, desc in PAIRS:
        gap = _ext_mm(upper, ren)[2] - _ext_mm(lower, ren)[3]
        print(f'gap: {desc}: {gap:.2f} mm')
        if gap < 0.3:
            fails.append(f'OVERLAP: {desc} gap {gap:.2f} mm')
    for a, b, desc in SEPARATE:
        ax0, ax1, ay0, ay1 = _ext_mm(a, ren)
        bx0, bx1, by0, by1 = _ext_mm(b, ren)
        if not (ax1 < bx0 - 0.5 or bx1 < ax0 - 0.5
                or ay1 < by0 - 0.5 or by1 < ay0 - 0.5):
            fails.append(f'INTERSECT: {desc}')

    # 5) column fit: label column clear of the axes, value labels and note
    # inside the axes right edge, note above the bottom spine
    ax_l, ax_r = AX_MM[0], AX_MM[0] + AX_MM[2]
    for t in cit_texts + sub_texts:
        if _ext_mm(t, ren)[1] > ax_l - 1.0:
            fails.append(f'COLUMN: {t.get_text()[:30]!r} into the axes')
    for t in val_texts + [note_t]:
        if _ext_mm(t, ren)[1] > ax_r + 0.3:
            fails.append(f'RIGHT EDGE: {t.get_text()[:30]!r} past axes')
    if _ext_mm(note_t, ren)[2] < AX_MM[1] + 0.5:
        fails.append('NOTE: sits on the bottom spine')

    # 6) line-width floors: coloured range bars >= 0.567 pt, black marker
    # edges >= 0.255 pt
    lw_min = min(ln.get_linewidth() for ln in RANGE_LINES)
    mew_min = min(mk.get_markeredgewidth() for mk in MARKER_LINES)
    print(f'range bars: {len(RANGE_LINES)} at >= {lw_min} pt; '
          f'marker edges >= {mew_min} pt')
    if lw_min < ar7.LW_COLOUR_MIN:
        fails.append(f'LINEWIDTH: range bar {lw_min} < {ar7.LW_COLOUR_MIN}')
    if mew_min < ar7.LW_BLACK_MIN:
        fails.append(f'LINEWIDTH: marker edge {mew_min} < {ar7.LW_BLACK_MIN}')

    # 7) greyscale separation of the three boundary colours (PIL L formula)
    # — marker shape is the second, non-colour channel on top of this
    Ls = {k: _pil_L(v) for k, v in BOUNDARY_COLOUR.items()}
    print('greyscale L:', ', '.join(f'{k} {v}' for k, v in Ls.items()))
    vals = sorted(Ls.values())
    gaps = [b - a for a, b in zip(vals, vals[1:])]
    if min(gaps) < 30:
        fails.append(f'GREYSCALE: boundary L gaps {gaps} (< 30)')

    for f_ in fails:
        print('FAIL', f_)
    return not fails


ok = run_checks()
if not ok:
    sys.exit(1)

ar7.export(fig, os.path.join(OUT_DIR, 'Fig14_7_3_modelled_system_value'))
if GREY_DIR:
    os.makedirs(GREY_DIR, exist_ok=True)
    print('greyscale dump:',
          ar7.greyscale_dump(fig, os.path.join(GREY_DIR, 'Fig14_7_3_modelled_system_value')))
print(f'exported Fig14_7_3_modelled_system_value.png/.pdf '
      f'({CANVAS[0]}x{CANVAS[1]} mm, 300 dpi)')
