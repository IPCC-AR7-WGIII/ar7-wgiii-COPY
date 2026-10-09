# Figure 14.7.3 — Modelled system value of digitally-enabled flexibility and integration

Figure package for the IPCC WGIII AR7 First Order Draft, Chapter 14
(Digitalisation), Section 14.7. `CITATION.cff` carries the citable metadata and
the full caption.

## What the data is

`data/fig14_7_3_modelled_system_value_data.csv` — one row per displayed entry,
5 rows, in the order they appear on the figure.

| column | content |
|---|---|
| `display_order` | position on the figure, 1 at the top |
| `entry_label` | the citation rendered as the row label |
| `system_boundary` | `city`, `sector` or `national`; sets the marker shape and colour |
| `value_low_percent`, `value_high_percent` | the reported value, or the ends of a reported range, in per cent |
| `value_kind` | `range` or `single` |
| `value_label_as_rendered` | the value string exactly as printed on the figure |
| `cost_denominator` | what the percentage is a percentage of |
| `geography` | the geographic coverage of the result |
| `study_description` | what was modelled, against what comparator |
| `source` | the full source string |
| `doi_or_url` | the locator for that source |

Units are per cent reduction, matching the figure's axis label. The denominator
differs between entries, so `cost_denominator` is part of the data rather than a
note: the sector-boundary entry is a percentage of industry-related energy costs,
not of total system cost, which is why the figure gives it its own colour and
names the boundary in the row sublabel.

**Missing values.** None. For a single reported value, `value_low_percent` and
`value_high_percent` hold the same number and `value_kind` is `single`. No
numeric sentinel is used: never `-999`, never `0`.

This is a plot-ready table of the displayed entries only. The chapter's working
evidence table, `e2_modelled_value_data.csv`, holds two further rows (Szinai et
al. 2020 and an IEA 2023 curtailment entry) that measure curtailment reduction
rather than system cost and are not displayed, so they are not part of this
figure's data or its input-data screen.

## Input data and methods

Every value is a cited result from a published study or institutional analysis. No
input dataset is committed here, and no published figure is reproduced or adapted.

- **Garcia Arenas et al. 2022**, *Energies* 15(7):2638, 10.3390/en15072638
  (MDPI, CC BY 4.0 article licence). Coupled power and residential heat operation
  against separate management, Brussels-Capital Region, 2050 city case. Author
  attribution corrected in the 29 July 2026 audit; the DOI is unchanged and
  valid.
- **Mayer et al. 2024**, *Frontiers in Energy Research* 12:1443506,
  10.3389/fenrg.2024.1443506 (Frontiers, CC BY article licence). Industrial
  demand-side management in a net-zero sector-coupled system, Switzerland. The
  study reports at two boundaries and both are shown, one against
  industry-related energy costs and one against total energy-system cost. The
  authors state the values are an upper bound, because implementation costs are
  excluded.
- **IEA 2026b**, *Scaling Up Demand Flexibility*, June 2026, pp. 9 and 54.
  CC BY 4.0. https://www.iea.org/reports/scaling-up-demand-flexibility.
  Ambitious flexibility roll-out, Ireland, 2035 case.
- **Burghardt, Schaefer and Weidlich 2025**, *iScience* 28:113381,
  10.1016/j.isci.2025.113381. Coupled against soft-linked optimisation of
  industry and energy system, Germany.

**Method.** Each entry reports a modelled result relative to the comparator
stated in its own row, so the entries are not pooled, averaged or ranked against
one another, and no cross-study statistic is computed. Values are percentage
reductions in system costs or curtailment. All are modelled; none is a measured
outcome. Where a study reports a range, the bar spans it; where it reports a
single value, a point marker is drawn.

## What the code does

`code/fig14_7_3.py` draws the five entries on a 180 x 100 mm canvas with the axes
at mm coordinates and a logarithmic x axis from 0.2 to 80 per cent, in the AR7
house style from `code/ar7_style.py`.

The five entries are held in the script's `ENTRIES` constant rather than read from
the CSV at run time, which is how the figure has always been built. The packaged
CSV is the same data in archival form, and `tools/verify_submissions.py` asserts
that the CSV equals `ENTRIES` row for row, so the two cannot drift apart.

Rows are labelled directly, with no legend box: each carries its citation over a
system-boundary sublabel, and the value at the bar or marker end. The system
boundary sets both a colour and a marker shape, and is named in text on every
row, so the boundary never rests on colour alone. Non-obvious decisions are
commented where they apply.

Before exporting, the script self-checks font resolution, minimum type size, WCAG
AA contrast, canvas containment, label-column and right-edge fit, vertical gaps,
note separation, line-width floors and greyscale separation. It prints each
result, exits non-zero if any check fails, and exports only when all pass.

## How to run it

1. Install the pinned environment, once:
   `pip install -r ../env/requirements_sec14.7.txt`. See
   `../env/README_sec14.7.md`, including the Arial and Arial Narrow system-font
   requirement, which pip cannot satisfy.
2. Run the figure script: `python code/fig14_7_3.py`. It can be run from any
   working directory, because paths resolve relative to the script.

On success it writes `figure/Fig14_7_3_modelled_system_value.png` at 300 dpi and
the matching `.pdf` as vector with TrueType embedded.

## Licences

Final data created by the chapter author team, licensed CC BY 4.0. Code licensed
MIT, as the SPDX headers in `code/` record.
