# Box 14.7.1, Figure 1 — Digitalisation for cross-sectoral integration

Figure package for the IPCC WGIII AR7 First Order Draft, Chapter 14
(Digitalisation), Section 14.7. `CITATION.cff` carries the citable metadata and
the full caption.

## What the data is

None. This is a conceptual schematic with no underlying dataset and no displayed
numerical values, so there is no data table to archive. `data/README.md` records
that absence, and the folder is kept so every figure package in this section has
the same structure.

The complete rendered wording lives in the script's content constants:
`TECHNOLOGIES`, `MODES`, `SECTORS`, `SYSTEMS` and `OUTCOMES`.

## Input data and methods

No input data. The figure reproduces no dataset, table or published figure. Every
box, link and label is authored content: the chapter team's own framing of which
digital technology categories act through which integration modes, across which
sectors, systems and markets, and where each outcome is assessed in the report.

The section numbers printed in the outcomes strip are pointers into the
assessment itself, not data: system flexibility and variable renewable energy
integration in 14.7.4, costs and potentials with 14.8, systemic risks and
distributional implications in 14.7.5, and the quantified net emissions balance
in Chapter 9.

Because nothing is reproduced or adapted, no copyright permission is required.

## What the code does

`code/box14_7_1_fig1.py` draws the integration architecture on a 180 x 100 mm
canvas: four technology-category boxes on the left, connected through collector
bus lines to four integration-mode boxes in the centre, which operate across the
applications panel on the right (sectors, and systems and markets), with the
integration-outcomes strip along the bottom.

The layout is mapped one to one from the notebook original onto mm coordinates.
Micro-nudges of at most 0.9 mm, commented at the geometry constants, clear the
AR7 type sizes without moving any box, row, link or ordering.

Panel identity is carried by tinted fills with full-hue edges, by column position
and by the bold panel titles, so identity never rests on colour alone, and the
figure remains readable in greyscale. Acronyms are expanded at first occurrence
on the figure, so it stands alone in a slide deck: internet of things, artificial
intelligence, agriculture, forestry and other land use, variable renewable
energy. Non-obvious decisions are commented where they apply, including the white
zone fills that replace washes sitting below the 15 per cent print floor.

Before exporting, the script self-checks font resolution, minimum type size, WCAG
AA contrast, canvas and in-box containment, stack gaps, annotation clearance
against the collector lines, line-width floors and greyscale edge separation. It
prints each result, exits non-zero if any check fails, and exports only when all
pass.

## How to run it

1. Install the pinned environment, once:
   `pip install -r ../env/requirements_sec14.7.txt`. See
   `../env/README_sec14.7.md`, including the Arial and Arial Narrow system-font
   requirement, which pip cannot satisfy.
2. Run the figure script: `python code/box14_7_1_fig1.py`. It can be run from any
   working directory, because paths resolve relative to the script. There is no
   data step to run first.

On success it writes `figure/FigBox14_1_integration_architecture.png` at 300 dpi
and the matching `.pdf` as vector with TrueType embedded.

## Licences

The figure is authored content created by the chapter author team; the same
CC BY 4.0 terms as the section's final data apply to it. Code licensed MIT, as
the SPDX headers in `code/` record.
