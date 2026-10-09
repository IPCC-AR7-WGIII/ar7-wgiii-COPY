#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# fig14_7_2.py — standalone export script for Fig14_7_2_flexibility_utilised_vs_need
# Extracted from ch14_schematics.ipynb (notebook retired as build system).
# AR7 restyle 2026-07-31: styled via _stylerun/ar7_style.py (IPCC palette,
# Arial/Arial Narrow, 180x100 mm canvas, 300 dpi export, WCAG/greyscale checks).
# Run from the "10_Figures" folder:  python "_stylerun/fig14_7_2.py"
# Reads e1_flexibility_data.csv (relative path); writes
# Fig14_7_2_flexibility_utilised_vs_need.png/.pdf beside the CSV at the folder
# root, with _greyscale.png in _qa/greyscale (central layout); or
# into figure/ with no greyscale dump (GitHub package layout).
import matplotlib
matplotlib.use("Agg")

import csv
import os
import sys

import matplotlib.pyplot as plt
from matplotlib import font_manager
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
matplotlib.rcParams['hatch.linewidth'] = 0.7   # coloured hatch >= 0.567 pt

MM = 25.4

# ---------------------------------------------------------------- content ---
# Content is FROZEN: every value, wording and citation string below comes
# verbatim from e1_flexibility_data.csv / the settled v3 text. The national-
# volumes box keeps the settled citations: United States line "(FERC, 2025)",
# header "(IEA, 2026a; FERC, 2025)". Acronym scan of rendered text: GW is an
# SI unit (exempt, defined by the axis label "Gigawatts (GW)"); IEA and FERC
# are organisations' citation names (kept as citations); DR / NZE / STEPS do
# not occur abbreviated — scenario names are already spelled out.
HEADLINE = ('Demand response utilised today is about one fifth\n'
            'of the volume needed by 2030')
LABEL_UTIL = 'Demand response utilised (2024, demonstrated)'
LABEL_BENCH = 'IEA Net Zero Emissions Scenario benchmark (2030)'


def tint(hex_colour, white_share=0.85):
    """Blend a hex colour towards white (white_share = share of white)."""
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda v: round(v + (255 - v) * white_share)
    return '#{:02x}{:02x}{:02x}'.format(mix(r), mix(g), mix(b))


# Palette, S2 Option A (2026-09-28). The utilised series was dark_blue and
# ipcc_blue, which made those two hues mean "end-use sector" here while meaning
# "system boundary" in Figure 14.7.3, the figure this one is read against (E3).
# The two sectors now share one ramp of tints of black, which frees the blue
# family to carry system boundary consistently across the pair. It also brings
# this figure closer to E2, "start simple, with black, greys and one colour":
# the mustard benchmark is now the only colour on the canvas, and it marks the
# one element the headline is about.
#
# The benchmark stays distinct in the mustard family, a light tint fill with a
# full-hue warm_mustard edge and a '//' hatch, so demonstrated (solid) versus
# modelled benchmark (hatched) never rests on colour alone. No red-green
# pairing anywhere. PIL greyscale L: industry 38 / buildings 140 / mustard tint
# 224, gaps 102 and 84, well clear of the 30 floor and a wider spread than the
# blues gave. White bold in-bar label on industry: 15.13, WCAG AA pass.
C_INDUSTRY = ar7.grey(0.85)
C_BUILDINGS = ar7.grey(0.45)
C_BENCH_EDGE = ar7.PALETTE['warm_mustard']
C_BENCH_FILL = tint(C_BENCH_EDGE, 0.75)
GREY_EDGE = ar7.grey(0.40)      # annotation-box borders
GREY_GRID = ar7.grey(0.20)      # x gridlines

# ------------------------------------------------------------------- data ---


def read_rows(csv_path=None):
    # Resolved through DATA_DIR so the same file reads the CSV at
    # the folder root centrally and from data/ inside a package.
    csv_path = csv_path or os.path.join(DATA_DIR, 'e1_flexibility_data.csv')
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        return {r['element']: r for r in csv.DictReader(f)}


rows = read_rows()


def val(element):
    r = rows.get(element)
    return float(r['value_low']) if r else None


industry = val('Demand response utilised (industry)')
buildings = val('Demand response utilised (buildings)')
total = val('Demand response utilised (global total)')
benchmark = val('IEA Net Zero Emissions benchmark for 2030')
needs = rows.get('Short-term flexibility needs growth by 2035')

# ------------------------------------------------------------ geometry (mm) —
CANVAS = (180, 100)
AX_MM = (4.0, 22.0, 172.0, 62.0)        # left, bottom, width, height in mm
Y_UTIL, Y_BENCH = 1.0, 0.0
BAR_H = 0.52
XLIM = (0, 570)
YLIM = (-0.40, 1.75)

fig = plt.figure(figsize=ar7.fig_mm(*CANVAS))
ax = fig.add_axes([AX_MM[0] / CANVAS[0], AX_MM[1] / CANVAS[1],
                   AX_MM[2] / CANVAS[0], AX_MM[3] / CANVAS[1]])
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_axisbelow(True)

AUDIT = []      # text audit: WCAG entries (+ measured containment)
PAIRS = []      # (upper, lower, desc): vertical-gap checks, mm
SEPARATE = []   # (a, b, desc): rectangles that must not intersect


def add_text(x, y, s, *, desc, bg, **kw):
    t = ax.text(x, y, s, **kw)
    AUDIT.append({'desc': desc, 'artist': t, 'bg': bg})
    return t


# Headline (required wording, bold 14 pt, above the figure; replaces the old
# in-image "Figure 14.7.2: ..." title line — figure number lives in the
# manuscript caption, as settled in Block 2)
head_t = fig.text(2.0 / CANVAS[0], 98.5 / CANVAS[1], HEADLINE,
                  ha='left', va='top', linespacing=1.12,
                  **ar7.headline_kwargs())
AUDIT.append({'desc': 'headline', 'artist': head_t, 'bg': '#ffffff'})

# Demonstrated utilisation (stacked; solid) — no bar without a source row.
# Direct labels at the series: series name above the bar, values at segment /
# series end; no legend box anywhere.
if industry is not None and buildings is not None:
    ax.barh(Y_UTIL, industry, height=BAR_H, color=C_INDUSTRY,
            edgecolor='white', linewidth=0.6, zorder=3)
    ax.barh(Y_UTIL, buildings, left=industry, height=BAR_H, color=C_BUILDINGS,
            edgecolor='white', linewidth=0.6, zorder=3)
    util_lab = add_text(0, Y_UTIL + BAR_H / 2 + 0.06, LABEL_UTIL,
                        desc='series label: utilised', bg='#ffffff',
                        ha='left', va='bottom', family='Arial',
                        fontsize=ar7.SIZE_AXIS_LABEL, fontweight='bold',
                        color=ar7.BLACK, zorder=4)
    ind_lab = add_text(industry / 2, Y_UTIL, f'Industry\n~{industry:g} GW',
                       desc='in-bar: industry', bg=C_INDUSTRY,
                       ha='center', va='center', family='Arial',
                       fontsize=ar7.SIZE_ANNOTATION, fontweight='bold',
                       color='#ffffff', zorder=4)
    bld_lab = add_text(industry + buildings / 2, Y_UTIL - BAR_H / 2 - 0.08,
                       f'Buildings ~{buildings:g} GW',
                       desc='below-bar: buildings', bg='#ffffff',
                       ha='center', va='top', family='Arial',
                       fontsize=ar7.SIZE_ANNOTATION, color=ar7.BLACK, zorder=4)
    if total is not None:
        tot_lab = add_text(industry + buildings + 12, Y_UTIL,
                           f'around {total:g} GW utilised in total, 2024\n'
                           f'(IEA, 2026a)',
                           desc='series end: total', bg='#ffffff',
                           ha='left', va='center', family='Arial',
                           fontsize=ar7.SIZE_ANNOTATION, color=ar7.BLACK,
                           zorder=4)

# Modelled benchmark (hatched; visually distinct from demonstrated; no text
# in the band)
if benchmark is not None:
    ax.barh(Y_BENCH, benchmark, height=BAR_H, facecolor=C_BENCH_FILL,
            edgecolor=C_BENCH_EDGE, hatch='//', linewidth=0.8, zorder=3)
    bench_lab = add_text(0, Y_BENCH + BAR_H / 2 + 0.06, LABEL_BENCH,
                         desc='series label: benchmark', bg='#ffffff',
                         ha='left', va='bottom', family='Arial',
                         fontsize=ar7.SIZE_AXIS_LABEL, fontweight='bold',
                         color=ar7.BLACK, zorder=4)
    bench_val = add_text(benchmark + 8, Y_BENCH,
                         f'{benchmark:g} GW\n(IEA, 2023)',
                         desc='series end: benchmark', bg='#ffffff',
                         ha='left', va='center', family='Arial',
                         fontsize=ar7.SIZE_ANNOTATION, color=ar7.BLACK,
                         zorder=4)

# National volumes box: aligned top-right. The United States entry carries its
# own citation (FERC, 2025) and no metric word, per the v3 addendum 2.
nationals = [
    ('United States registered demand response', None, '(FERC, 2025)'),
    ('Korea registered demand response capacity', 'registered', None),
    ('Japan successful demand response bids', 'successful bids', None),
]
nat_lines = []
for element, metric, cite in nationals:
    r = rows.get(element)
    if r:
        line = f"{r['geography']}: {float(r['value_low']):g} GW"
        if metric:
            line += f' {metric}'
        line += f" ({r['year']})"
        if cite:
            line += f' {cite}'
        nat_lines.append(line)

BOX_RIGHT = 0.985       # axes-fraction anchor for both right-hand boxes
BOX_TOP = 0.985
PAD_MM = 1.8


def measured_box(texts_kw, y_top_ax, face='#ffffff'):
    """Place stacked texts (left-aligned, right-edge anchored) and draw one
    rounded box behind them. texts_kw: list of (string, text-kwargs)."""
    arts = [ax.text(0.5, 0.5, s, transform=ax.transAxes, ha='left', va='top',
                    multialignment='left', zorder=5, **kw)
            for s, kw in texts_kw]
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    inv = ax.transAxes.inverted()
    sizes = []
    for t in arts:
        e = t.get_window_extent(renderer=ren)
        (x0, y0), (x1, y1) = inv.transform([(e.x0, e.y0), (e.x1, e.y1)])
        sizes.append((x1 - x0, y1 - y0))
    ax_w_mm, ax_h_mm = AX_MM[2], AX_MM[3]
    gap_ax = 1.0 / ax_h_mm                       # 1 mm between blocks
    pad_x, pad_y = PAD_MM / ax_w_mm, PAD_MM / ax_h_mm
    x_left = BOX_RIGHT - max(w for w, h in sizes)
    y = y_top_ax
    for t, (w, h) in zip(arts, sizes):
        t.set_position((x_left, y))
        y -= h + gap_ax
    y_bot = y + gap_ax
    rect = FancyBboxPatch(
        (x_left - pad_x, y_bot - pad_y),
        (BOX_RIGHT - x_left) + 2 * pad_x, (y_top_ax - y_bot) + 2 * pad_y,
        boxstyle='round,pad=0', transform=ax.transAxes, facecolor=face,
        edgecolor=GREY_EDGE, linewidth=ar7.LW_BLACK_MIN + 0.15, zorder=4.5,
        mutation_scale=6)
    ax.add_patch(rect)
    return arts, rect, y_bot - pad_y


nat_rect = needs_rect = None
if nat_lines:
    (nat_head, nat_body), nat_rect, nat_bot = measured_box(
        [('National volumes (IEA, 2026a; FERC, 2025)',
          dict(family='Arial', fontsize=ar7.SIZE_TICK, fontweight='bold',
               color=ar7.BLACK)),
         ('\n'.join(nat_lines),
          dict(family='Arial', fontsize=ar7.SIZE_TICK,
               color=ar7.BLACK, linespacing=1.35))],
        BOX_TOP)
    AUDIT.append({'desc': 'national box header', 'artist': nat_head,
                  'bg': '#ffffff'})
    AUDIT.append({'desc': 'national box body', 'artist': nat_body,
                  'bg': '#ffffff'})

# Needs-growth annotation: right column, below the national box; a different
# metric from demand response GW, so an annotation (annotation font recorded
# in stylerun_state.md: Arial Italic) rather than a bar
if needs is not None:
    lo, hi = float(needs['value_low']), float(needs['value_high'])
    needs_top = (nat_bot - 3.0 / AX_MM[3]) if nat_rect is not None else BOX_TOP
    (needs_t,), needs_rect, _ = measured_box(
        [('Projected short-term flexibility needs by 2035:\n'
          f'{lo:g} to {hi:g} times current levels\n'
          'modelled, Stated Policies Scenario (IEA, 2025);\n'
          'two- to ten-fold under Net Zero',
          dict(linespacing=1.3, color=ar7.BLACK, **ar7.annotation_kwargs()))],
        needs_top)
    AUDIT.append({'desc': 'needs annotation', 'artist': needs_t,
                  'bg': '#ffffff'})

# Axes furniture: ticks 7 pt Arial Narrow, axis label 8 pt Arial, light grid
ax.set_yticks([])
ax.set_xticks(range(0, 501, 100))
plt.setp(ax.get_xticklabels(), family=ar7.FONT_TICK, fontsize=ar7.SIZE_TICK)
ax.grid(axis='x', color=GREY_GRID, linewidth=ar7.LW_BLACK_MIN)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_linewidth(ar7.LW_BLACK_MIN)
ax.set_xlabel('Gigawatts (GW)', family='Arial',
              fontsize=ar7.SIZE_AXIS_LABEL, color=ar7.BLACK)

# ---------------------------------------------------------------- checks ----


def _ext_mm(artist, renderer):
    e = artist.get_window_extent(renderer=renderer)
    d = fig.dpi
    return (e.x0 / d * MM, e.x1 / d * MM, e.y0 / d * MM, e.y1 / d * MM)


def _data_mm(x, y):
    px, py = ax.transData.transform((x, y))
    return (px / fig.dpi * MM, py / fig.dpi * MM)


def _pil_L(hex_colour):
    r, g, b = (int(hex_colour.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return round(0.299 * r + 0.587 * g + 0.114 * b)


# vertical stack, left column: label / bar / label / label / bar (data-coord
# edges converted to mm inside run_checks)
BAR_EDGES = {
    'utilised bar': (Y_UTIL - BAR_H / 2, Y_UTIL + BAR_H / 2),
    'benchmark bar': (Y_BENCH - BAR_H / 2, Y_BENCH + BAR_H / 2),
}
PAIRS += [(util_lab, ('utilised bar', 'top'), 'utilised label vs bar'),
          (('utilised bar', 'bottom'), bld_lab, 'bar vs buildings label'),
          (bld_lab, bench_lab, 'buildings label vs benchmark label'),
          (bench_lab, ('benchmark bar', 'top'), 'benchmark label vs bar')]
if nat_rect is not None and needs_rect is not None:
    PAIRS.append((nat_rect, needs_rect, 'national box vs needs box'))
if needs_rect is not None:
    PAIRS.append((needs_rect, ('benchmark bar', 'top'),
                  'needs box vs benchmark bar'))
    SEPARATE.append((tot_lab, needs_rect, 'total label vs needs box'))
if nat_rect is not None:
    SEPARATE += [(util_lab, nat_rect, 'utilised label vs national box'),
                 (tot_lab, nat_rect, 'total label vs national box')]
SEPARATE.append((bench_val, needs_rect, 'benchmark value vs needs box'))


def run_checks():
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    fails = []

    def edge_mm(item, which):
        if isinstance(item, tuple):          # ('bar name', 'top'|'bottom')
            name, side = item
            lo, hi = BAR_EDGES[name]
            return _data_mm(0, hi if side == 'top' else lo)[1]
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

    # 4) containment (canvas), vertical gaps, rectangle separation
    for a in AUDIT:
        x0, x1, y0, y1 = _ext_mm(a['artist'], ren)
        if x0 < -0.2 or x1 > CANVAS[0] + 0.2 or y0 < -0.2 or y1 > CANVAS[1] + 0.2:
            fails.append(f"CANVAS: {a['desc']} "
                         f'[{x0:.1f},{x1:.1f},{y0:.1f},{y1:.1f}] off-canvas')
    for upper, lower, desc in PAIRS:
        gap = edge_mm(upper, 'bottom') - edge_mm(lower, 'top')
        print(f'gap: {desc}: {gap:.2f} mm')
        if gap < 0.3:
            fails.append(f'OVERLAP: {desc} gap {gap:.2f} mm')
    for a, b, desc in SEPARATE:
        ax0, ax1, ay0, ay1 = _ext_mm(a, ren)
        bx0, bx1, by0, by1 = _ext_mm(b, ren)
        if not (ax1 < bx0 - 0.5 or bx1 < ax0 - 0.5
                or ay1 < by0 - 0.5 or by1 < ay0 - 0.5):
            fails.append(f'INTERSECT: {desc}')

    # 5) in-bar fit: industry label inside its segment, value labels clear of
    # the axes right edge
    ix0, ix1, iy0, iy1 = _ext_mm(ind_lab, ren)
    seg_l = _data_mm(0, 0)[0]
    seg_r = _data_mm(industry, 0)[0]
    if ix0 < seg_l + 0.8 or ix1 > seg_r - 0.8:
        fails.append('IN-BAR: industry label exceeds its segment')
    for t, desc in ((bench_val, 'benchmark value'), (tot_lab, 'total label')):
        if _ext_mm(t, ren)[1] > AX_MM[0] + AX_MM[2] + 0.2:
            fails.append(f'RIGHT EDGE: {desc} past axes')

    # 6) greyscale separation of the three fills (PIL L formula) — the hatch
    # is a second, non-colour channel for the benchmark on top of this
    fills = {'industry grey(0.85)': C_INDUSTRY,
             'buildings grey(0.45)': C_BUILDINGS,
             'benchmark mustard tint': C_BENCH_FILL}
    Ls = {k: _pil_L(v) for k, v in fills.items()}
    print('greyscale L:', ', '.join(f'{k} {v}' for k, v in Ls.items()))
    vals = sorted(Ls.values())
    gaps = [b - a for a, b in zip(vals, vals[1:])]
    if min(gaps) < 30:
        fails.append(f'GREYSCALE: fill L gaps {gaps} (< 30)')

    for f_ in fails:
        print('FAIL', f_)
    return not fails


ok = run_checks()
if not ok:
    sys.exit(1)

ar7.export(fig, os.path.join(OUT_DIR, 'Fig14_7_2_flexibility_utilised_vs_need'))
if GREY_DIR:
    os.makedirs(GREY_DIR, exist_ok=True)
    print('greyscale dump:',
          ar7.greyscale_dump(fig, os.path.join(GREY_DIR, 'Fig14_7_2_flexibility_utilised_vs_need')))
print(f'exported Fig14_7_2_flexibility_utilised_vs_need.png/.pdf '
      f'({CANVAS[0]}x{CANVAS[1]} mm, 300 dpi)')
