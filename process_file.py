# process_file.py
import pandas as pd
import os
import argparse

def process_file(gene_info_path, rna_seq_counts_path):
    # gene_info 파일 읽기
    gene_info_df = pd.read_csv(gene_info_path)

    # rna_seq_counts 파일 확장자 확인
    file_extension = os.path.splitext(rna_seq_counts_path)[1]

    # 확장자에 따라 파일 읽기
    if file_extension == '.csv':
        rna_seq_counts_df = pd.read_csv(rna_seq_counts_path)
    elif file_extension == '.tsv':
        rna_seq_counts_df = pd.read_csv(rna_seq_counts_path, sep='\t')
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. CSV 또는 TSV 파일을 사용해 주세요.")

    # 'gene_id' 열이 ENSG 형식인지 여부를 판단
    is_ensg = rna_seq_counts_df['gene_id'].str.startswith('ENSG')

    # 'gene_id'가 ENSG 형식인 경우와 아닌 경우를 나누어 처리
    rna_seq_counts_df['gene_name'] = rna_seq_counts_df['gene_id'].where(~is_ensg, None)
    rna_seq_counts_df['gene_id'] = rna_seq_counts_df['gene_id'].where(is_ensg, None)

    # gene_info 파일에서 해당하는 gene_id와 gene_name을 병합
    merged_df = rna_seq_counts_df.merge(gene_info_df[['gene_name', 'gene_id']], how='left', left_on='gene_id', right_on='gene_id', suffixes=('', '_info'))

    # gene_id가 없는 경우 빈칸으로 설정
    merged_df['gene_id'] = merged_df['gene_id'].fillna('')

    # gene_name이 없는 경우 빈칸으로 설정
    merged_df['gene_name'] = merged_df['gene_name'].combine_first(merged_df['gene_name_info']).fillna('')

    # 열 순서 조정 (gene_id, gene_name을 첫 번째와 두 번째 열로 이동)
    merged_df = merged_df[['gene_id', 'gene_name'] + [col for col in merged_df.columns if col not in ['gene_id', 'gene_name', 'gene_name_info']]]

    # 각 열을 개별 파일로 저장 (gene_id, gene_name 열 제외)
    base_filename = os.path.splitext(os.path.basename(rna_seq_counts_path))[0]
    output_dir = os.path.dirname(rna_seq_counts_path)

    for column in merged_df.columns[2:]:  # gene_id와 gene_name 열 제외
        output_path = os.path.join(output_dir, f"{base_filename}_{column}.csv")
        single_column_df = merged_df[['gene_id', 'gene_name', column]]
        single_column_df.to_csv(output_path, index=False)

        # 두 번째 열 확인 후 숫자가 아니면 파일 삭제 및 경고 메시지 출력
        second_column_values = single_column_df[column]
        if not pd.api.types.is_numeric_dtype(second_column_values):
            print(f"경고: {output_path} 파일의 두 번째 열이 숫자가 아닙니다. 파일을 삭제합니다.")
            os.remove(output_path)

    print("파일 분리가 완료되었습니다.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process RNAseq counts file and gene info file.')
    parser.add_argument('rna_seq_counts_path', type=str, help='Path to the RNAseq counts file (CSV or TSV).')
    args = parser.parse_args()

    gene_info_path = 'gene_info.csv'  # gene_info 파일 경로를 고정

    process_file(gene_info_path, args.rna_seq_counts_path)
