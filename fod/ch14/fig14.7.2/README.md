# Figure 14.7.2 — Demonstrated demand response versus assessed need

Figure package for the IPCC WGIII AR7 First Order Draft, Chapter 14
(Digitalisation), Section 14.7. `CITATION.cff` carries the citable metadata and
the full caption.

## What the data is

`data/e1_flexibility_data.csv` — one row per element shown on the figure, 8 rows.

| column | content |
|---|---|
| `element` | the figure element the row supplies (the key the script looks up) |
| `value_low`, `value_high` | the reported value, or the ends of a reported range |
| `unit` | the unit of the value, gigawatts (GW) or a multiplier |
| `year` | the year the value refers to |
| `geography` | the geographic coverage of the value |
| `status` | whether the value is demonstrated utilisation or a modelled benchmark |
| `source` | the full source string, as cited on the figure |
| `doi_or_url` | the locator for that source |
| `note` | the assessment note behind the row (not rendered) |

Units are gigawatts of demand response, matching the figure's axis label, except
the needs-growth rows, which are dimensionless multipliers.

**Missing values.** None. Every row carries a value. An empty cell in a text
column means nothing was recorded for that field. No numeric sentinel is used:
never `-999`, never `0`.

The working copy of this table in the chapter folder carries one further column,
`engine_flag`, recording AI-assisted evidence triage during literature
collection. It is workflow provenance rather than figure data, so the packaged
CSV drops it.

## Input data and methods

All values are cited facts drawn from institutional analyses. No input dataset is
committed here, and no published figure is reproduced or adapted.

- **IEA 2026a**, *Electricity 2026*, Flexibility chapter. CC BY 4.0.
  https://www.iea.org/reports/electricity-2026/flexibility. Supplies the global
  utilised total and the industry and buildings volumes for 2024.
- **IEA 2023**, *Unlocking Smart Grid Opportunities in Emerging Markets and
  Developing Economies*, p. 27. CC BY 4.0.
  https://www.iea.org/reports/unlocking-smart-grid-opportunities-in-emerging-markets-and-developing-economies.
  Supplies the roughly 500 GW of demand response required by 2030 in the IEA Net
  Zero Emissions scenario. Re-attributed following the 29 July 2026 audit.
- **IEA 2025**, *World Energy Outlook 2025*, p. 64, Figure 1.24. CC BY 4.0.
  https://www.iea.org/reports/world-energy-outlook-2025. Supplies the
  needs-growth multipliers. The values are cited in a text annotation; the IEA
  figure itself is not reproduced or adapted, so no copyright permission is
  needed.
- **IEA demand-response energy-system page**, reached through the chapter's DR07
  record. CC BY 4.0.
  https://www.iea.org/energy-system/energy-efficiency-and-demand/demand-response.
  Supplies the Korea and Japan volumes.
- **FERC 2025**, *Assessment of Demand Response and Advanced Metering*. A United
  States federal government public document, public domain under 17 U.S.C. 105.
  https://www.ferc.gov/power-sales-and-markets/demand-response/reports-demand-response-and-advanced-metering.
  Supplies the United States volume of 33.3 GW.

**Method.** Demonstrated utilisation and the modelled benchmark are different
metrics of different vintages, so they are cited separately and never combined
into one total: utilisation follows the 2024 methodology, the benchmark the 2023
Net Zero Emissions trajectory. The benchmark is a normative target, not a
projection. National volumes carry the metric word their source uses, so Korea
reads "registered" and Japan "successful bids"; those words are not
interchangeable and were not harmonised. The segment and total values are the
sources' own order-of-magnitude statements, reproduced verbatim.

## What the code does

`code/fig14_7_2.py` reads `data/e1_flexibility_data.csv` and draws the
comparison on a 180 x 100 mm canvas with the axes placed at mm coordinates, in
the AR7 house style from `code/ar7_style.py`.

Series are labelled directly, with no legend box: each bar carries its name above
it and its value at the segment or bar end, which is why the y tick labels are
removed. Demonstrated utilisation is drawn solid and the modelled benchmark is
drawn as a tinted fill with a full-hue edge and a diagonal hatch, so the
distinction between a demonstrated volume and a normative benchmark never rests
on colour alone. Non-obvious decisions are commented where they apply.

Before exporting, the script self-checks font resolution, minimum type size,
WCAG AA contrast, canvas containment, vertical gaps, box separation, in-bar label
fit and greyscale separation. It prints each result, exits non-zero if any check
fails, and exports only when all pass.

## How to run it

1. Install the pinned environment, once:
   `pip install -r ../env/requirements_sec14.7.txt`. See
   `../env/README_sec14.7.md`, including the Arial and Arial Narrow system-font
   requirement, which pip cannot satisfy.
2. Run the figure script: `python code/fig14_7_2.py`. It can be run from any
   working directory, because paths resolve relative to the script.

On success it writes `figure/Fig14_7_2_flexibility_utilised_vs_need.png` at
300 dpi and the matching `.pdf` as vector with TrueType embedded.

## Licences

Final data created by the chapter author team, licensed CC BY 4.0. Code licensed
MIT, as the SPDX headers in `code/` record.
