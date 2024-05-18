RNASQLite
RNASQLite is a collection of Python scripts designed to store and manage RNA-seq data in an SQLite database.

File Description
setup_database.py: Creates the SQLite database and the required tables.
process_file.py: Processes RNA-seq data by separating it into files based on gene_id and gene_name, and removes files containing non-numeric values.
insert_into_db.py: Inserts the processed RNA-seq data into the SQLite database.
gene_info.csv: Contains information about gene_id, gene_type, and gene_name.
Usage
1. Create the Database
python setup_database.py

2. Process RNA-seq Data
python process_file.py path_to_your_rna_seq_counts_file

Example:

python process_file.py C:\Users\kes09\BI\tmp\GSE266762_RNAseq_counts.csv

3. Insert Processed Data into the Database
python insert_into_db.py path_to_your_rna_seq_counts_file

Example:

python insert_into_db.py C:\Users\kes09\BI\tmp\GSE266762_RNAseq_counts.csv

Dependencies
Install the packages listed in the requirements.txt file.

pip install -r requirements.txt