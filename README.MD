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