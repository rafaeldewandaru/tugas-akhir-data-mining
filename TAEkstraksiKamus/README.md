# Dictionary Extraction Pipeline

This repository contains the code to extract and process NLP resources from dictionary PDFs. Follow the instructions below to set up your environment and run the pipeline.

## Prerequisites
* Python 3.14.x 

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine.
```bash
git clone <your-repo-url>
cd <your-repo-directory> 
```

### 2. Create Required Directories

Create the necessary input and output directories. You run the following commands in your terminal to generate them quickly:

```bash
mkdir "[Full] Daftar Kamus Ekstraksi" 
mkdir "[Full] Bentuk JSON"
mkdir "[Full] CSV JSON all information - Final"
mkdir "[Full] CSV One Entry JSON With Font + Posisi Approach"
mkdir "[Full] Raw CSV JSON all information"
mkdir "CSV One Entry JSON With Font + Posisi Approach"
mkdir "CSV One Entry JSON With Font Approach"
mkdir "csvAnalysis"
```
### 3. Add Source Data

Place all your source dictionary PDF files directly into the "[Full] Daftar Kamus Ekstraksi directory."

### 4. Configure the Environment

Select Python 3.14.x as your active kernel. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

## Execution Order
Run the code files sequentially through the following directories to complete the extraction and evaluation process:

1. `pdfExtraction/`: Run scripts here first to parse the PDFs.

2. `dictProcessing/`: Run scripts here to clean and structure the extracted dictionary data.

3. `resourceGen/`: Run scripts here to generate the final NLP resources and parallel corpora.

4. `evaluation/`: Run scripts here last to evaluate the output quality.
