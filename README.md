# RNASQLite

RNASQLite is a tool for managing RNA-Seq data with SQLite. This package allows you to process RNA-Seq counts files, insert count files into a database, and retrieve sample information from the database.

## Installation

First, navigate to the directory containing `setup.py` and install the package:

```bash
pip install .
```

Alternatively, if the package is available on PyPI, you can install it directly:

```
pip install RNASQLite
```

## Usage
Create Database
Create a new database. 

```
RNASQLite -create
```

Process and Split RNAseq Counts File
Process the given RNAseq counts file and save the count files for each sample in the counts directory. This step uses the gene info file (gene_info.csv) to add gene information.

```
RNASQLite -split path/to/your/rna_seq_counts_file.csv
```

Insert Count Files into Database
Read the count files from the counts directory and insert them into the database.

```
RNASQLite -load
```

Fetch All Samples from Database
Retrieve all sample information from the database.

```
RNASQLite -fetch
```

Fetch Samples by Column and Value
Fetch samples from the database by specifying a column name and a value. This command extracts count data for samples matching the specified condition and saves the result as a CSV file.

```
RNASQLite -column COLUMN VALUE
```

Example:

```
RNASQLite -column GSE_number GSE201396
```

In this example, the command fetches all samples from the database where the GSE_number column matches GSE201396. The count data for these samples are then combined into a single CSV file. The file is named based on the column and value provided, e.g., filtered_GSE_number_GSE201396.csv.

## Description
RNASQLite/cli.py: Handles the command line interface.

RNASQLite/db_utils.py: Contains utility functions related to the database.

RNASQLite/process_file.py: Processes the given gene_info.csv and RNAseq counts file to generate count files.

gene_info.csv: CSV file containing gene information.

setup.py: Contains package metadata and dependencies.

README.md: This file, which includes the description and usage of the RNASQLite package.
