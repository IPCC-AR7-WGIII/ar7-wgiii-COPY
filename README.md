# Code repository for AR7 Figures and Tables
This is the shared, WGIII-wide repository for AR7. This repository will be used to manage figure assets for AR7, including data, code, figure files, and environment information. Authors are responsible for contribuitng data and code relevant for their chapter/contribution.  

## Contents

- [1. Introduction](#introduction)
- [2. Repository structure](#respository-structure)
- [3. Key concepts](#key-concepts)
- [4. The `CITATION.cff` file](#citation)
- [5. Controlled vocabulary](#controlled-vocabulary)
- [6. Figures](#figures)

## 1. Introduction

This repository should be used for the management and submission of code underlying IPCC AR7 figures and tables. This repository is meant to store the data, code, and environment information necessary to reproduce the figures. The folder structure is described below. 

## 2. Repository structure 
The repository structure is described below and is organized by draft stage > chapter > figure. The Technical Summary, Summary for Policymakers, and Cross Chapter and Cross Working Group boxes are included as separate folders at the chapter level.

### 2.1 Report stage folders
- `fod`: Use this folder for materials submitted as part of the First Order Draft.
- `sod`: Use this folder for materials submitted as part of the Second Order Draft.
- `fgd`: Use this folder for materials submitted as part of the Final Government Distribution.

### 2.2 Chapter folders
- `ch1`: Chapter 1: Introduction and framing
- `ch2`: Chapter 2: Past and current anthropogenic emissions and their drivers
- `ch3`: Chapter 3: Projected futures in the context of sustainable development and climate change
- `ch4`: Chapter 4: Sustainable development and mitigation
- `ch5`: Chapter 5: Enablers and barriers
- `ch6`: Chapter 6: Policies and governance and international cooperation
- `ch7`: Chapter 7: Finance
- `ch8`: Chapter 8: Services and demand
- `ch9`: Chapter 9: Energy systems
- `ch10`: Chapter 10: Industry
- `ch11`: Chapter 11: Transport and mobility services and systems
- `ch12`: Chapter 12: Buildings and human settlements
- `ch13`: Chapter 13: Agriculture, Forestry, and Other Land Uses (AFOLU)
- `ch14`: Chapter 14: Integration and interactions across sectors and systems
- `ch15`: Chapter 15: Potentials, limits, and risks of Carbon Dioxide Removal (CDR)
- `ts`: Use this folder for materials being developed for the Technical Summary.
- `spm`: Use this folder for materials being developed for the Summary for Policymakers.
- `ccb`: Use this folder for materials being developed for Cross Chapter Boxes.
- `cwgb`: Use this folder for materials being developed for Cross Working Group Boxes.

### 2.3 Figure folders

- `figX`: The `figX/` folder is the main location for storing figure information. It contains four subfolders: data/, code/, figure/, and eng/, which are described below. You should duplicate the folder (including subfolders) for each figure in the chapter and name it accordingly (e.g., fig1_1, fig2_overview, box1fig1).  
- `data`: The `data/` subfolder is where you should store data to create the figure. It is meant to be self-contained, and include all information displayed in the figure. The data included here should require no substantial transformation to be used in the figure. This means for example that data units should match figure units.
- `code`: The `code/` subfolder is where you should store the code used to analyse input data and create the data for the figure, if any. If no such code is necessary, simply remove this directory.
- `figure`: The `figure/` subfolder is where you should upload the figure image file
- `env`: The `env/` folder contains environment specification files and documentation necessary to recreate the software environment used for the figure. This ensures that analyses and figures can be reproduced reliably across different systems.
- `src`: The `src/` folder may be used to store source code, datasets, workflows, or other details that apply to one or more figures in this chapter. Consider it an add-on space. It should not be used in replacement of the figure-specific folders described above.

## 3. Key concepts
- By `data`, we mean the data displayed in the figure, not the input/source datasets they derive from. Please do not commit large input datasets in this repository- such merge requests will be denied;
- By `metadata`, we mean the information about the figure, such as its title, caption, authors, and references. This information is captured in a CITATION.cff file, documented here.

## 4. The `CITATION.cff` file

The file ``CITATION.cff`` holds basic information about the figure, data, or code. It minimally requires a `title`, `authors`, `message` and the `cff-version`. Additional fields are collected depending on the draft order:

- FOD: `abstract` with the figure caption;
- SOD: `references` with the list of references (data and/or publication) used to create the figure;
- FGD: a `doi` for each reference listed in the `references` field.  

### 4.1 Example of a `CITATION.cff` file

```yaml
title: Title of figure, e.g. Figure 4.11 | Multiple lines of evidence for global surface air temperature (GSAT) changes for the long-term period, 2081–2100, relative to the average over 1995–2014, for all five priority scenarios.
abstract: Standalone description of methods necessary to understand the figure.
authors:
  - family-names: Asselin
    given-names: Alice
    orcid: "https://orcid.org/0000-0000-0000-0001"
  - family-names: Brun
    given-names: Bob
    orcid: "https://orcid.org/0000-0000-0000-0001"
references:
  - title: Data for Figure 4.11 of AR7 SRC Chapter 4
    authors:
      - name: A. Asselin et al.
    type: data
    data-type: CSV
    doi: 10.5281/zenodo.3678927
cff-version: 1.2.0
```

## 5. Controlled vocabulary

To ensure consistency with other Working Groups, please utilize the abbreiviations from the table below when referring to AR7 components.

| Type        | Full name                                 | Abbreviation |
|-------------|-------------------------------------------|-------------|
| ``report``  |                                           |             |  
|             | Special Report on Cities                  | src         |
|             | Working Group I                           | wg1         |
|             | Working Group II                          | wg2         |
|             | Working Group III                         | wg3         |
|             | Synthesis Report                          | syr         |
| ``draft``   |                                           |             |
|             | Zero Order Draft                          | zod         | 
|             | First Order Draft                         | fod         |
|             | Second Order Draft                        | sod         |
|             | Final Government Distribution             | fgd         |
| ``chapter`` |                                           |             |
|             | Summary for Policymakers                  | spm         |
|             | Technical Summary                         | ts          |
|             | Chapter 1                                 | ch1         |
|             | Cross-Chapter Paper 1                     | ccp1        |
|             | Annex III                                 | ann3        |
| ``figure``  |                                           |             |
|             | Figure 4.1                                | fig1        |
|             | Cross-Chapter Box 4.1, Figure 1           | ccb1fig1    |
|             | Cross-Section Box TS.1, Figure 1          | csb1fig1    |
|             | Cross-WG Box 4.1, Figure 1                | cwgbfig1    |
|             | Box 4.1, Figure 1                         | box1fig1    |
|             | Frequently Asked Questions 4.1, Figure 1  | faq1fig1    |
