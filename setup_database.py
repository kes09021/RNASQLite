# setup_database.py
import sqlite3

def setup_database(db_path):
    # 데이터베이스 연결 (db 파일이 없으면 새로 생성됨)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS samples (
        sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        tissue_type TEXT,
        collection_date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS counts (
        count_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id TEXT,
        gene_id TEXT,
        gene_name TEXT,
        count_value REAL,
        identity TEXT
    )
    ''')

    # 변경사항 저장
    conn.commit()
    # 연결 종료
    conn.close()

if __name__ == '__main__':
    db_path = 'geo_rna_seq.db'  # SQLite 데이터베이스 파일 경로
    setup_database(db_path)
    print("데이터베이스 생성이 완료되었습니다.")
