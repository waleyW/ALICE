# Literature Database Code

## Purpose
This tool provides a comprehensive solution for:
-Downloading academic papers using DOI numbers
-Converting downloaded PDFs to searchable text format
-Building a local literature database for research

## Installation
```bash
git clone https://github.com/waleyW/ALICE.git
cd ALICE
```
## Paper downloadr
A Python tool for batch downloading academic papers using DOI numbers.

### Features
-Bulk download papers from DOI numbers
-Simple command-line interface

### Requirements
before run this script, please prepare an txt containing all the required 'DOI'

### Usage
```bash
python paper_download.py --txt 'txt_path' 
```
## PDF to TXT conversion
Convert your PDF papers into searchable text format for further analysis.
### Features
-Batch conversion of PDF documents
-Maintains folder structure
-Preserves text formatting
### Requirements
Replace with your actual folders in convert.py
``` bash
pdf_folder_path = r'pdf_path'
txt_folder_path = r'txt_path'
```
### Usage
```bash
python convert.py
```

# Searching System
## Purpose
A Python tool for automated literature searching and data extraction across scientific documents.
## Mode
-Keyword type search
-Boolean operator search
-Case sensitive search
-Keyword frequency search
## Requirements
### Replace the Keywords of Script
Before running this script, please configure your search parameters in the script:
``` bash
directory = r'article_folder_path'
queries = ["GSTP1 AND Breast cancer AND DNA methylation AND patient AND sequencing"]
output_csv_path = r'results_path'
```
### Query Guidelines
Use AND/OR operators for logical combinations
All boolean operators must be capitalized (AND, OR, NOT)
Complex Query Patterns
```bash
# Basic AND query
"GENE AND Cancer AND Method"

# Using NOT operator
"Gene NOT Variant"

# Combining multiple conditions
"(GSTP1 OR MLH1) AND Breast cancer"
```

### Output Format
Results are saved in two CSV files:
-Basic statistics: output.csv
-High-frequency matches: output_high_freq.csv

## Case-sensitive Usage
``` bash
python search_case.py
```
## Case-nosensitive Usage
``` bash
python search_nocase.py
```