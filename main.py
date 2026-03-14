import pandas as pd
from processing.cleaner import clean_text
from processing.tokenizer import tokenize
from analysis.frequencies import count_tokens
from analysis.trends import compare_periods
from reports.reporter import build_report

def main():
    df = pd.read_csv("data/raw/sample_data.csv")
    
    unigram_results = compare_periods(df, split_date="2026-03-08",ngram_size=1)
    bigram_results = compare_periods(df, split_date="2026-03-08",ngram_size=2)
    trigram_results = compare_periods(df, split_date="2026-03-08",ngram_size=3)
    
    
    unigram_report = build_report(unigram_results, title="TREND MINER REPORT - UNIGRAMAS")
    bigram_report = build_report(bigram_results, title="TREND MINER REPORT - BIGRAMAS")
    trigram_report = build_report(trigram_results, title="TREND MINER REPORT - TRIGRAMAS")
    
    
    full_report = unigram_report + "\n\n" + bigram_report + "\n\n" + trigram_report
    
    
    print(full_report)
    
    with open("data/processed/report.txt", "w", encoding="utf-8") as file:
        file.write(full_report)
if __name__ == "__main__":
    main()