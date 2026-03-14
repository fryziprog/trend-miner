import pandas as pd
from processing.cleaner import clean_text
from processing.tokenizer import tokenize
from analysis.frequencies import count_tokens
from analysis.trends import compare_periods
from reports.reporter import build_report

def main():
    df = pd.read_csv("data/raw/sample_data.csv")
    results = compare_periods(df, split_date="2026-03-08")
    report = build_report(results)
    
    print(report)
    
    with open("data/processed/report.txt", "w", encoding="utf-8") as file:
        file.write(report)
if __name__ == "__main__":
    main()