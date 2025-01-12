import os
import re
import pandas as pd
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count
from contextlib import closing
from tqdm import tqdm

def count_occurrences(content, expr):
  
    pattern = re.compile(re.escape(expr))
    return len(pattern.findall(content))

def evaluate_query(content, query):
    def search_expression(content, expr):
        if 'NOT' in expr:
            parts = expr.split('NOT')
            count_a = count_occurrences(content, parts[0].strip())
            count_b = count_occurrences(content, parts[1].strip())
            return max(count_a - count_b, 0)
        return count_occurrences(content, expr)

    def evaluate_logic_block(content, block):
        or_parts = block.split(" OR ")
        return max(evaluate_and_logic(content, part) for part in or_parts)

    def evaluate_and_logic(content, part):
        and_parts = part.split(" AND ")
        and_results = [search_expression(content, term.strip()) for term in and_parts]
        return min(and_results) if all(and_results) else 0

    while '(' in query:
        query = re.sub(r'\(([^()]+)\)', lambda m: str(evaluate_logic_block(content, m.group(1))), query)

    return evaluate_logic_block(content, query)

def process_file(file_info):
    root, file, queries = file_info
    file_path = os.path.join(root, file)
    results = Counter()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for query in queries:
                results[query] = evaluate_query(content, query)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return (file, results)

def process_directory(directory, queries):
    results = defaultdict(Counter)
    file_infos = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_infos.append((root, file, queries))

    max_processes = min(4, cpu_count())
    with closing(Pool(max_processes)) as pool:
        all_results = list(tqdm(pool.imap(process_file, file_infos), total=len(file_infos), desc="Processing files"))

    for file, file_results in all_results:
        results[file].update(file_results)

    return results

def save_query_statistics_to_csv(results, output_path):
    query_counts = defaultdict(int)
    high_freq_counts = defaultdict(int)
    high_freq_files = defaultdict(list)

    for filename, file_counts in results.items():
        for query, count in file_counts.items():
            if count > 0:
                query_counts[query] += 1
            if count >= 5:
                high_freq_counts[query] += 1
                high_freq_files[query].append(filename)

    df_query = pd.DataFrame(list(query_counts.items()), columns=['Query', 'Files Containing Keyword'])
    df_high_freq = pd.DataFrame(list(high_freq_counts.items()), columns=['Query', 'Files with >=5 Occurrences'])

    df_query.to_csv(output_path, index=False)
    df_high_freq.to_csv(output_path.replace('.csv', '_high_freq.csv'), index=False)

def main():
    directory = r'G:\cancer'
    #queries = ["NSCLC AND adagrasib", "NSCLC AND sotorasib","NSCLC AND amivantamb","NSCLC AND mobocertinib"]
    queries = [
"GSTP1 AND Breast cancer AND DNA methylation AND patient AND sequencing",
"GSTP1 AND Breast cancer AND DNA methylation AND patient AND PCR",
"GSTP1 AND Breast cancer AND DNA methylation AND patient AND microarray",
"GSTP1 AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"GSTP1 AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"GSTP1 AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"GSTP1 AND Lung cancer AND DNA methylation AND patient AND sequencing",
"GSTP1 AND Lung cancer AND DNA methylation AND patient AND PCR",
"GSTP1 AND Lung cancer AND DNA methylation AND patient AND microarray",
"GSTP1 AND Melanoma AND DNA methylation AND patient AND sequencing",
"GSTP1 AND Melanoma AND DNA methylation AND patient AND PCR",
"GSTP1 AND Melanoma AND DNA methylation AND patient AND microarray",
"GSTP1 AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"GSTP1 AND Prostate cancer AND DNA methylation AND patient AND PCR",
"GSTP1 AND Prostate cancer AND DNA methylation AND patient AND microarray",
"HOXA9 AND Breast cancer AND DNA methylation AND patient AND sequencing",
"HOXA9 AND Breast cancer AND DNA methylation AND patient AND PCR",
"HOXA9 AND Breast cancer AND DNA methylation AND patient AND microarray",
"HOXA9 AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"HOXA9 AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"HOXA9 AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"HOXA9 AND Lung cancer AND DNA methylation AND patient AND sequencing",
"HOXA9 AND Lung cancer AND DNA methylation AND patient AND PCR",
"HOXA9 AND Lung cancer AND DNA methylation AND patient AND microarray",
"HOXA9 AND Melanoma AND DNA methylation AND patient AND sequencing",
"HOXA9 AND Melanoma AND DNA methylation AND patient AND PCR",
"HOXA9 AND Melanoma AND DNA methylation AND patient AND microarray",
"HOXA9 AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"HOXA9 AND Prostate cancer AND DNA methylation AND patient AND PCR",
"HOXA9 AND Prostate cancer AND DNA methylation AND patient AND microarray",
"MLH1 AND Breast cancer AND DNA methylation AND patient AND sequencing",
"MLH1 AND Breast cancer AND DNA methylation AND patient AND PCR",
"MLH1 AND Breast cancer AND DNA methylation AND patient AND microarray",
"MLH1 AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"MLH1 AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"MLH1 AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"MLH1 AND Lung cancer AND DNA methylation AND patient AND sequencing",
"MLH1 AND Lung cancer AND DNA methylation AND patient AND PCR",
"MLH1 AND Lung cancer AND DNA methylation AND patient AND microarray",
"MLH1 AND Melanoma AND DNA methylation AND patient AND sequencing",
"MLH1 AND Melanoma AND DNA methylation AND patient AND PCR",
"MLH1 AND Melanoma AND DNA methylation AND patient AND microarray",
"MLH1 AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"MLH1 AND Prostate cancer AND DNA methylation AND patient AND PCR",
"MLH1 AND Prostate cancer AND DNA methylation AND patient AND microarray",
"MSH2 AND Breast cancer AND DNA methylation AND patient AND sequencing",
"MSH2 AND Breast cancer AND DNA methylation AND patient AND PCR",
"MSH2 AND Breast cancer AND DNA methylation AND patient AND microarray",
"MSH2 AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"MSH2 AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"MSH2 AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"MSH2 AND Lung cancer AND DNA methylation AND patient AND sequencing",
"MSH2 AND Lung cancer AND DNA methylation AND patient AND PCR",
"MSH2 AND Lung cancer AND DNA methylation AND patient AND microarray",
"MSH2 AND Melanoma AND DNA methylation AND patient AND sequencing",
"MSH2 AND Melanoma AND DNA methylation AND patient AND PCR",
"MSH2 AND Melanoma AND DNA methylation AND patient AND microarray",
"MSH2 AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"MSH2 AND Prostate cancer AND DNA methylation AND patient AND PCR",
"MSH2 AND Prostate cancer AND DNA methylation AND patient AND microarray",
"PTEN AND Breast cancer AND DNA methylation AND patient AND sequencing",
"PTEN AND Breast cancer AND DNA methylation AND patient AND PCR",
"PTEN AND Breast cancer AND DNA methylation AND patient AND microarray",
"PTEN AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"PTEN AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"PTEN AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"PTEN AND Lung cancer AND DNA methylation AND patient AND sequencing",
"PTEN AND Lung cancer AND DNA methylation AND patient AND PCR",
"PTEN AND Lung cancer AND DNA methylation AND patient AND microarray",
"PTEN AND Melanoma AND DNA methylation AND patient AND sequencing",
"PTEN AND Melanoma AND DNA methylation AND patient AND PCR",
"PTEN AND Melanoma AND DNA methylation AND patient AND microarray",
"PTEN AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"PTEN AND Prostate cancer AND DNA methylation AND patient AND PCR",
"PTEN AND Prostate cancer AND DNA methylation AND patient AND microarray",
"RASSF1 AND Breast cancer AND DNA methylation AND patient AND sequencing",
"RASSF1 AND Breast cancer AND DNA methylation AND patient AND PCR",
"RASSF1 AND Breast cancer AND DNA methylation AND patient AND microarray",
"RASSF1 AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"RASSF1 AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"RASSF1 AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"RASSF1 AND Lung cancer AND DNA methylation AND patient AND sequencing",
"RASSF1 AND Lung cancer AND DNA methylation AND patient AND PCR",
"RASSF1 AND Lung cancer AND DNA methylation AND patient AND microarray",
"RASSF1 AND Melanoma AND DNA methylation AND patient AND sequencing",
"RASSF1 AND Melanoma AND DNA methylation AND patient AND PCR",
"RASSF1 AND Melanoma AND DNA methylation AND patient AND microarray",
"RASSF1 AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"RASSF1 AND Prostate cancer AND DNA methylation AND patient AND PCR",
"RASSF1 AND Prostate cancer AND DNA methylation AND patient AND microarray",
"RUNX3 AND Breast cancer AND DNA methylation AND patient AND sequencing",
"RUNX3 AND Breast cancer AND DNA methylation AND patient AND PCR",
"RUNX3 AND Breast cancer AND DNA methylation AND patient AND microarray",
"RUNX3 AND Colorectal cancer AND DNA methylation AND patient AND sequencing",
"RUNX3 AND Colorectal cancer AND DNA methylation AND patient AND PCR",
"RUNX3 AND Colorectal cancer AND DNA methylation AND patient AND microarray",
"RUNX3 AND Lung cancer AND DNA methylation AND patient AND sequencing",
"RUNX3 AND Lung cancer AND DNA methylation AND patient AND PCR",
"RUNX3 AND Lung cancer AND DNA methylation AND patient AND microarray",
"RUNX3 AND Melanoma AND DNA methylation AND patient AND sequencing",
"RUNX3 AND Melanoma AND DNA methylation AND patient AND PCR",
"RUNX3 AND Melanoma AND DNA methylation AND patient AND microarray",
"RUNX3 AND Prostate cancer AND DNA methylation AND patient AND sequencing",
"RUNX3 AND Prostate cancer AND DNA methylation AND patient AND PCR",
"RUNX3 AND Prostate cancer AND DNA methylation AND patient AND microarray",
]
    


    output_csv_path = r'E:\biomarker\fan\1221\1221_matric_2.csv'

    results = process_directory(directory, queries)
    save_query_statistics_to_csv(results, output_csv_path)

    print("Results have been saved to CSV at:", output_csv_path)

if __name__ == "__main__":
    main()
