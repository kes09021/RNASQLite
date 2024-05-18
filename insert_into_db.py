# insert_into_db.py
import pandas as pd
import sqlite3
import os
import argparse

def insert_counts_into_db(db_path, counts_df, identity):
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 데이터 삽입
    for column in counts_df.columns[2:]:
        for index, row in counts_df.iterrows():
            gene_id = row['gene_id']
            gene_name = row['gene_name']
            count_value = row[column]
            sample_id = column
            c.execute('''
                INSERT INTO counts (sample_id, gene_id, gene_name, count_value, identity)
                VALUES (?, ?, ?, ?, ?)
            ''', (sample_id, gene_id, gene_name, count_value, identity))

    # 변경사항 저장
    conn.commit()
    # 연결 종료
    conn.close()

def main(rna_seq_counts_path, db_path):
    # 파일명에서 identity 추출
    base_filename = os.path.splitext(os.path.basename(rna_seq_counts_path))[0]
    identity = base_filename.split('_')[0]  # 예시로 GSE 번호 추출

    # 분리된 파일 읽기
    output_dir = os.path.dirname(rna_seq_counts_path)
    file_paths = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith(base_filename) and f.endswith('.csv')]

    for file_path in file_paths:
        counts_df = pd.read_csv(file_path)
        insert_counts_into_db(db_path, counts_df, identity)

    print("데이터베이스에 데이터 삽입이 완료되었습니다.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert processed RNAseq counts files into SQLite database.')
    parser.add_argument('rna_seq_counts_path', type=str, help='Path to the original RNAseq counts file (CSV or TSV).')
    args = parser.parse_args()

    db_path = 'geo_rna_seq.db'  # SQLite 데이터베이스 파일 경로

    main(args.rna_seq_counts_path, db_path)
