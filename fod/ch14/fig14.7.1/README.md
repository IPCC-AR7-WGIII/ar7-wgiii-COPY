# Figure 14.7.1 — Evidenced maturity of digitalisation technology categories by integration mode

Figure package for the IPCC WGIII AR7 First Order Draft, Chapter 14
(Digitalisation), Section 14.7. `CITATION.cff` carries the citable metadata and
the full caption.

## What the data is

`data/maturity_evidence.csv` — one row per cell of the 4 x 4 maturity matrix
(technology category by integration mode), 16 rows.

| column | content |
|---|---|
| `category` | technology category (matrix row) |
| `mode` | integration mode (matrix column) |
| `maturity_class` | one of `deployed at scale`, `demonstrated in pilots`, `research and prototype`; rendered as the cell fill, marker and label |
| `key_evidence` | the assessed evidence summary behind the class assignment (not rendered) |
| `source` | full source strings for the cell's citations |
| `doi_or_url` | DOI or URL for each source, separated by a vertical bar |
| `short_citation` | the citation string rendered inside the cell |

The figure has no units: it is a classed matrix, not a measured quantity.

**Missing values.** None. All 16 category-by-mode cells carry an evidence row. A
genuinely unassessed cell is represented by an absent `(category, mode)` row,
which the script renders as a 15 per cent black "not assessed" cell following the
AR7 conventions. No numeric sentinel is used anywhere: never `-999`, never `0`.
An empty cell in a text column means nothing was recorded for that field.

The working copy of this table in the chapter folder carries one further column,
`engine_flag`, which records AI-assisted evidence triage during literature
collection. It is workflow provenance rather than figure data, so the packaged
CSV drops it. The chapter's AI Usage Declaration records the practice.

## Input data and methods

Every value in this table is a cited fact: a maturity classification the chapter
assessed from published sources, not a reproduction of any published table or
figure. Each cell's own sources and locators are in the `source` and
`doi_or_url` columns. By category of source:

- **Journal literature (cited facts).** Rodrigues et al. 2025
  (10.1007/s40518-025-00264-x); Koirala et al. 2024
  (10.1016/j.adapen.2024.100196); Pal et al. 2021 (10.1049/rpg2.12272);
  Borgaonkar et al. 2021 (10.1002/cpe.6466); Jorgensen and Ma 2025
  (10.3390/app15126475); Kiasari et al. 2024 (10.3390/en17164128); Pandey et al.
  2023 (10.1093/ce/zkad061); Henao et al. 2025 (10.1186/s42162-025-00529-1);
  Price et al. 2025, GenCast, Nature 637:84-90 (10.1038/s41586-024-08252-9);
  Palensky et al. 2022 (10.12688/digitaltwin.17435.2); Aghazadeh Ardebili et al.
  2024 (10.1186/s42162-024-00385-5); Thwe et al. 2025
  (10.1109/ACCESS.2025.3580055; TwinEU, Horizon Europe GA 101136119); Khan et al.
  2025 (10.1016/j.seta.2025.104197); Neaimeh et al. 2020
  (10.1186/s42162-020-0103-1); Sospiro et al. 2021 (10.3390/en14185637); Boeding
  et al. 2024 (10.3390/en17020373); Cheng et al. 2025
  (10.1038/s41598-025-91940-x).
- **Grey literature.** IEA 2023, *Unlocking Smart Grid Opportunities in Emerging
  Markets and Developing Economies* (3DEN), CC BY 4.0,
  https://www.iea.org/reports/unlocking-smart-grid-opportunities-in-emerging-markets-and-developing-economies.
  PJM 2025 Inside Lines announcement, public web content cited as fact; the CSV
  holds both the publisher URL and a Wayback Machine archive of 29 July 2026,
  because the announcement returns 404 to scripted clients while loading in
  browsers.

**Method.** Each cell was assigned to one of three maturity classes on the basis
of the sources cited within it, with the literature assessed to mid-2026.
Numeric technology readiness levels are not used, because published values for
integration applications rest on author or survey judgement. No input dataset is
committed here, and none is reproduced or adapted: the sources contribute cited
values and classifications only.

## What the code does

`code/fig14_7_1.py` reads `data/maturity_evidence.csv` and builds the matrix at
mm-true coordinates, one data unit to one millimetre on a 180 x 100 mm canvas, in
the AR7 house style from `code/ar7_style.py` (IPCC palette, Arial and Arial
Narrow type scale, line-width floors, exact-canvas export at 300 dpi).

The maturity ramp carries a marker per class as well as a colour, so the
classification never rests on colour alone: a filled circle for deployed at
scale, a half-filled circle for demonstrated in pilots, an open circle for
research and prototype. Non-obvious decisions are commented in the script where
they apply.

Before exporting, the script self-checks font resolution, minimum type size,
WCAG AA contrast, box containment and overlap, marker clearance, and greyscale
separation of the three class fills. It prints each result, exits non-zero if any
check fails, and exports only when all pass.

## How to run it

1. Install the pinned environment, once:
   `pip install -r ../env/requirements_sec14.7.txt`. See
   `../env/README_sec14.7.md`, including the Arial and Arial Narrow system-font
   requirement, which pip cannot satisfy.
2. Run the figure script: `python code/fig14_7_1.py`. It can be run from any
   working directory, because paths resolve relative to the script.

On success it writes `figure/Fig14_7_1_maturity_matrix.png` at 300 dpi and
`figure/Fig14_7_1_maturity_matrix.pdf` as vector with TrueType embedded.

## Licences

Final data created by the chapter author team, licensed CC BY 4.0. Code licensed
MIT, as the SPDX headers in `code/` record.
