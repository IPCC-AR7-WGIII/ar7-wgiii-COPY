"""AR7 visual style module for the Ch14.7 figure re-run (IPCC WGIII AR7 FOD).

SPDX-License-Identifier: MIT

Import this from each per-figure script, then call apply_style() before building
the figure. Implements the AR7 visual style guide: palette, greys, fonts, type
sizes, mm-based canvas sizes, minimum line widths, print export, and the WCAG /
greyscale checkers.

Fonts: Arial and Arial Narrow are discovered through matplotlib's system font
list, so no font directory is hard-coded. Set the AR7_FONT_DIR environment
variable to add a folder to search when the families live outside the system
font path. Registration fails with a clear message when either family is
missing. Uberhand Pro is not installed on the render machine, so annotations
fall back to Arial Italic (ANNOTATION_FONT records which was chosen).
"""

import glob
import io
import os

import matplotlib
from matplotlib import font_manager

MM_PER_INCH = 25.4

# ---------------------------------------------------------------- palette ---
PALETTE = {
    'ipcc_blue':    '#5492cd',
    'warm_blue':    '#00aad0',
    'dark_blue':    '#003466',
    'warm_red':     '#990002',
    'bright_red':   '#e00000',
    'dark_orange':  '#ef550f',
    'warm_mustard': '#c47900',
    'warm_yellow':  '#ffa900',
    'warm_green':   '#004f00',
    'bright_green': '#59a900',
}

BLACK = '#000000'


def grey(t):
    """Tint of black: t is the black share on a white ground, t >= 0.15.

    grey(0.15) is the lightest grey the guide allows (15% black); anything
    lighter fails the print floor, so values below 0.15 raise.
    """
    if not 0.15 <= t <= 1.0:
        raise ValueError(f'grey tint must be in [0.15, 1.0], got {t}')
    v = round(255 * (1.0 - t))
    return '#{:02x}{:02x}{:02x}'.format(v, v, v)


NO_DATA = grey(0.15)   # 15% black — reserved for no-data / not-assessed fills


def tint(hex_colour, white_share=0.85):
    """Blend a palette hue towards white; white_share is the share of white.

    Used for light fills that carry a hue's identity while leaving enough
    lightness for black text on top. The full hue stays available for the edge,
    so the pairing reads as one category.
    """
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda v: round(v + (255 - v) * white_share)   # noqa: E731
    return '#{:02x}{:02x}{:02x}'.format(mix(r), mix(g), mix(b))

# ------------------------------------------------------------------ fonts ---
_FONT_ENV = 'AR7_FONT_DIR'                    # optional extra folder to search
_FONT_GLOBS = ('arial*.ttf', 'ARIALN*.TTF')   # Arial family + Arial Narrow family
_FONT_PREFIX = 'ARIAL'                        # file-name prefix of both families


def _font_files():
    """Arial and Arial Narrow font files, without a hard-coded font directory.

    Takes matplotlib's own scan of the system font paths and keeps the files
    whose names start with "arial", which is both the Arial family
    (arial.ttf, arialbd.ttf, ariali.ttf, ...) and the Arial Narrow family
    (ARIALN.TTF, ARIALNB.TTF, ...). When AR7_FONT_DIR is set, the two globs
    are also applied to that folder, so a machine that keeps the families
    outside the system path can still render.
    """
    files = [p for p in font_manager.findSystemFonts()
             if os.path.basename(p).upper().startswith(_FONT_PREFIX)]
    extra = os.environ.get(_FONT_ENV)
    if extra:
        for pat in _FONT_GLOBS:
            files.extend(glob.glob(os.path.normpath(os.path.join(extra, pat))))
    return sorted(set(os.path.normpath(p) for p in files))


def _registered_names():
    return {f.name for f in font_manager.fontManager.ttflist}


def _add_and_label(files):
    """addfont the files, then give the Arial Narrow entries their own family.

    The ARIALN*.TTF name tables on this machine report family "Arial"
    (style "Narrow", stretch condensed), so matplotlib would never resolve
    the family "Arial Narrow". Renaming the manager entries for those files
    (system-scanned and addfont'ed alike) makes 'Arial Narrow' selectable
    by name, exactly as the guide's type spec is written.
    """
    for path in files:
        try:
            font_manager.fontManager.addfont(path)
        except Exception:
            pass  # a single unreadable file must not block the rest
    for entry in font_manager.fontManager.ttflist:
        if os.path.basename(entry.fname).upper().startswith('ARIALN'):
            entry.name = 'Arial Narrow'


def _resolves(family):
    try:  # instance-bound findfont: the module-level one goes stale on rebuild
        font_manager.fontManager.findfont(
            font_manager.FontProperties(family=family),
            fallback_to_default=False)
        return True
    except Exception:
        return False


def register_fonts():
    """Register the Arial and Arial Narrow families with matplotlib.

    Font files come from _font_files(), which reads matplotlib's system font
    scan and, when AR7_FONT_DIR is set, that folder as well. Adds them via
    font_manager.addfont; if the manager still cannot resolve the families,
    rebuilds the font cache once and retries. Raises RuntimeError naming the
    missing family and AR7_FONT_DIR when either is unavailable.
    Returns the sorted list of family names registered from those files.
    """
    files = _font_files()
    _add_and_label(files)

    if not (_resolves('Arial') and _resolves('Arial Narrow')):
        # cache miss — rebuild the font manager without the stale cache
        try:
            font_manager.fontManager = font_manager._load_fontmanager(
                try_read_cache=False)
        except Exception:
            font_manager.fontManager = font_manager.FontManager()
        # rebind the module-level helper so matplotlib's renderers see the
        # rebuilt manager rather than the stale instance they were bound to
        font_manager.findfont = font_manager.fontManager.findfont
        _add_and_label(files)

    missing = [fam for fam in ('Arial', 'Arial Narrow') if not _resolves(fam)]
    if missing:
        raise RuntimeError(
            'The AR7 figure style needs the {} font famil{} and matplotlib '
            'cannot resolve {} from the system font path. Install {} '
            'or set the {} environment variable to a folder holding the '
            'files (patterns {}). Files searched: {}.'.format(
                ' and '.join(missing), 'y' if len(missing) == 1 else 'ies',
                'it' if len(missing) == 1 else 'them',
                'them' if len(missing) > 1 else 'it',
                _FONT_ENV, ' and '.join(_FONT_GLOBS), len(files)))
    return sorted(n for n in _registered_names()
                  if n.lower().startswith('arial'))


register_fonts()

# Annotation font: the guide asks for Uberhand Pro; it is not installed on
# this machine, so annotations use Arial Italic. ANNOTATION_FONT records the
# outcome and feeds annotation_kwargs().
if 'Uberhand Pro' in _registered_names():
    ANNOTATION_FONT = {'family': 'Uberhand Pro', 'style': 'normal'}
else:
    ANNOTATION_FONT = {'family': 'Arial', 'style': 'italic'}

# ------------------------------------------------------------- type sizes ---
SIZE_HEADLINE = 14      # bold
SIZE_SUBHEAD = 10       # bold; panel titles
SIZE_AXIS_LABEL = 8
SIZE_TICK = 7           # set in Arial Narrow
SIZE_ANNOTATION = 7.5
SIZE_MIN = 6            # hard minimum anywhere on the canvas

FONT_TICK = 'Arial Narrow'


def headline_kwargs():
    return {'family': 'Arial', 'fontsize': SIZE_HEADLINE, 'fontweight': 'bold'}


def subhead_kwargs():
    return {'family': 'Arial', 'fontsize': SIZE_SUBHEAD, 'fontweight': 'bold'}


def tick_kwargs():
    return {'family': FONT_TICK, 'fontsize': SIZE_TICK}


def annotation_kwargs():
    return {'fontsize': SIZE_ANNOTATION, **ANNOTATION_FONT}


# ------------------------------------------------------------ line widths ---
LW_COLOUR_MIN = 0.567       # pt (0.20 mm) — minimum for any coloured line
LW_BLACK_MIN = 0.255        # pt (0.09 mm) — minimum for single-colour black
LW_HISTORICAL = 0.992       # pt (0.35 mm) — historical data series

# ----------------------------------------------------------------- canvas ---


def fig_mm(w=180, h=100):
    """Figure size in inches for a canvas of w x h mm.

    Standard AR7 canvases: 180x100 (default) and 180x225 (full page).
    """
    return (w / MM_PER_INCH, h / MM_PER_INCH)


FULL_PAGE_MM = (180, 225)


def reserve_caption(fig, mm=12):
    """Keep a clear caption band of `mm` at the bottom of the canvas.

    Raises the bottom of the subplot area so no axes content enters the band.
    Figures with manually-placed axes must keep their content above
    mm / canvas-height themselves; this helper covers subplot-managed axes.
    """
    h_in = fig.get_figheight()
    frac = (mm / MM_PER_INCH) / h_in
    fig.subplots_adjust(bottom=max(fig.subplotpars.bottom, frac))
    return frac


# ------------------------------------------------------------------ style ---


def apply_style():
    """Set rcParams for the AR7 style. Call once, before building the figure."""
    matplotlib.rcParams.update({
        'font.family': 'Arial',
        'font.size': SIZE_AXIS_LABEL,
        'axes.labelsize': SIZE_AXIS_LABEL,
        'axes.titlesize': SIZE_SUBHEAD,
        'axes.titleweight': 'bold',
        'xtick.labelsize': SIZE_TICK,
        'ytick.labelsize': SIZE_TICK,
        'legend.fontsize': SIZE_TICK,
        'figure.titlesize': SIZE_HEADLINE,
        'figure.titleweight': 'bold',
        'text.color': BLACK,
        'axes.edgecolor': BLACK,
        'axes.labelcolor': BLACK,
        'xtick.color': BLACK,
        'ytick.color': BLACK,
        'axes.linewidth': LW_BLACK_MIN,
        'lines.linewidth': LW_COLOUR_MIN,
        'patch.linewidth': LW_BLACK_MIN,
        'pdf.fonttype': 42,     # embed TrueType → text stays editable
        'ps.fonttype': 42,
        'svg.fonttype': 'none',
        'figure.facecolor': 'white',
        'savefig.facecolor': 'white',
    })


# ----------------------------------------------------------------- export ---

_NEAR_BLACK_MAX = 20 / 255   # channels at/below ~8% read as intended black


def _snap_colour(c):
    """Return pure black for near-black colours, else the colour unchanged."""
    try:
        r, g, b, a = matplotlib.colors.to_rgba(c)
    except (ValueError, TypeError):
        return c
    if a > 0 and max(r, g, b) <= _NEAR_BLACK_MAX and (r, g, b) != (0, 0, 0):
        return (0.0, 0.0, 0.0, a)
    return c


def force_blacks(fig):
    """Snap every near-black text / line / edge / face colour to #000000."""
    import matplotlib.text as mtext
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches_
    from matplotlib.collections import Collection
    for art in fig.findobj():
        if isinstance(art, mtext.Text):
            art.set_color(_snap_colour(art.get_color()))
        elif isinstance(art, mlines.Line2D):
            art.set_color(_snap_colour(art.get_color()))
        elif isinstance(art, mpatches_.Patch):
            art.set_edgecolor(_snap_colour(art.get_edgecolor()))
            art.set_facecolor(_snap_colour(art.get_facecolor()))
        elif isinstance(art, Collection):
            art.set_edgecolor([_snap_colour(c) for c in art.get_edgecolor()])
            art.set_facecolor([_snap_colour(c) for c in art.get_facecolor()])


def export(fig, name):
    """Write {name}.png (300 dpi) and {name}.pdf (vector), blacks forced.

    `name` may carry a relative path prefix; extension is added here.

    Saved at the figure's own canvas: no bbox_inches='tight' and no padding,
    so the delivered files measure exactly the mm size fig_mm() set (C1) and
    keep the caption band reserve_caption() holds at the bottom (B6). A tight
    bounding box would crop the canvas to the drawn ink, which is what made
    the July exports 185.0 x 105.1 mm and 179.1 x 99.4 mm instead of
    180 x 100 mm. Each script's canvas-containment self-check already proves
    nothing sits outside the canvas, so nothing is clipped by saving it whole.
    """
    force_blacks(fig)
    fig.savefig(f'{name}.png', dpi=300, facecolor='white', edgecolor='none')
    fig.savefig(f'{name}.pdf', facecolor='white', edgecolor='none')


# --------------------------------------------------------------- checkers ---


def _rel_luminance(c):
    r, g, b = matplotlib.colors.to_rgb(c)
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
           for v in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def wcag_contrast(fg, bg):
    """WCAG 2.x contrast ratio between two colours (1.0 – 21.0)."""
    l1, l2 = _rel_luminance(fg), _rel_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def wcag_passes(fg, bg, size_pt, bold=False):
    """AA check: 4.5 for normal text, 3.0 for large text (bold >= 14 pt,
    or any text >= 18 pt). Returns (passes, ratio, threshold)."""
    large = (bold and size_pt >= 14) or size_pt >= 18
    threshold = 3.0 if large else 4.5
    ratio = wcag_contrast(fg, bg)
    return ratio >= threshold, ratio, threshold


def greyscale_dump(fig, name):
    """Save {name}_greyscale.png — the L channel of the rendered figure, for
    the greyscale-survival check. Saved at the full canvas, as export() is."""
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, facecolor='white',
                edgecolor='none')
    buf.seek(0)
    out = f'{name}_greyscale.png'
    Image.open(buf).convert('L').save(out)
    return out


# ----------------------------------------------------------------- layout ---


def layout(script_file):
    """Resolve the data and output folders for the script at `script_file`.

    HERE is the script's own folder and ROOT its parent, so one file runs both
    centrally and inside a GitHub figure package:

    * package layout, when ROOT/CITATION.cff exists: read ROOT/data, write
      ROOT/figure, and write no greyscale dump (the dump is a QA artefact and
      J2 reserves figure/ for the figure image file);
    * central layout otherwise: read CSVs from and write renders to ROOT, with
      greyscale dumps in ROOT/_qa/greyscale.

    Every path is wrapped in os.path.normpath so the 'code/../data' form does
    not push a long checkout location past the Windows 260-character limit.
    Returns (data_dir, out_dir, greyscale_dir or None).
    """
    here = os.path.dirname(os.path.abspath(script_file))
    root = os.path.normpath(os.path.join(here, os.pardir))

    def under(*parts):
        return os.path.normpath(os.path.join(root, *parts))

    if os.path.exists(under('CITATION.cff')):
        return under('data'), under('figure'), None
    return root, root, under('_qa', 'greyscale')
