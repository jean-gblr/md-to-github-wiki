# md-to-github-wiki
This project allows you to split one md documentation file into several pages with links allowing easy upload to your github wiki repo.

## Context
This python script has been coded to help our need, maybe it can help you too.
We used it on a generated md file that was converted by [vsxmd](https://github.com/lijunle/Vsxmd) on a .Net5 project

## Getting started

### Usage
> python3 .\parser.py [documentation.md] [output_path]

### Entry file
documentation.md is the md file converted by vsxmd.  
output_path is the directory where the files will be generated.

### Output
A folder containing all files to upload to your github.wiki
