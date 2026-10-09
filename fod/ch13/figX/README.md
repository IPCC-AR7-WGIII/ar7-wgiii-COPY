## Folder Information

`figX`: The figX/ folder is the main location for storing figure information. It contains three subfolders and one CITATION.cff file, as described below. You should duplicate the folder (including subfolders) for each figure in the chapter and name it accordingly (e.g., fig1_1, fig2_overview, box1fig1).

## Subfolders
`data`: The data/ subfolder is where you should store data to create the figure. It is meant to be self-contained, and include all information displayed in the figure. The data included here should require no substantial transformation to be used in the figure. This means for example that data units should match figure units.
`code`: The code/ subfolder is where you should store the code used to analyse input data and create the data for the figure, if any. If no such code is necessary, simply remove this directory.
`figure`: The figure/ subfolder is where you should upload the figure image file

## CITATION.cff
The file CITATION.cff holds basic information about the figure, data, or code. For FOD, this fole should contain: title, authors, message, cff-version, and abstract with the figure caption.
