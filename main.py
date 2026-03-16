import pandas as pd
from analysis.trends import compare_periods
from analysis.spacy_entities import compare_entity_periods
#from analysis.subgenres import compare_subgenre_periods
#from analysis.subgenres import rank_current_subgeners
from analysis.subgenres import compare_subgenre_last_periods,rank_current_subgenres_last_period
from reports.reporter import build_report


def main():
    #df = pd.read_csv("data/raw/sample_data.csv")
    df = pd.read_csv("data/raw/youtube_music.csv")


    unigram_results = compare_periods(df, split_date="2026-03-08", ngram_size=1)
    bigram_results = compare_periods(df, split_date="2026-03-08", ngram_size=2)
    trigram_results = compare_periods(df, split_date="2026-03-08", ngram_size=3)
    
    entity_results = compare_entity_periods(df, split_date="2026-03-08")

    unigram_report = build_report(unigram_results, title="TREND MINER REPORT - UNIGRAMAS")
    bigram_report = build_report(bigram_results, title="TREND MINER REPORT - BIGRAMAS")
    trigram_report = build_report(trigram_results, title="TREND MINER REPORT - TRIGRAMAS")
    entity_report = build_report(entity_results, title="TREND MINER REPORT - ENTIDADES (spaCy)")
    
    
    #subgenre_results = compare_subgenre_periods(df, split_date="2026-03-08")
    #subgenre_report = build_report(subgenre_results, title="TREND MINER REPORT - SUBGENEROS")
    
    #current_subgenres = rank_current_subgeners(df, split_date="2026-03-08")
    
    subgenre_results = compare_subgenre_last_periods(df, days_current=7,days_previous=7)
    subgenre_report = build_report( subgenre_results, title="TREND MINER REPORT - SUBGENEROS")
    
    current_subgenres = rank_current_subgenres_last_period(df, days_current=7)
    
    current_lines = []
    current_lines.append("TREND MINER REPORT - SUBGENEROS ATUAIS")
    current_lines.append("=" * 30)
    current_lines.append("TOP SUBGENEROS NO PERIODO ATUAL:\n")
    
    for i, (term, freq) in enumerate( current_subgenres[:10], start=1):
        current_lines.append(f"{i}. {term} | freq_atual = {freq}")
    
    current_subgenres_report = "\n".join(current_lines)
    

    full_report = (
        unigram_report
        + "\n\n"
        + bigram_report
        + "\n\n"
        + trigram_report
        + "\n\n"
        + entity_report
        + "\n\n"
        + subgenre_report
        + "\n\n"
        + current_subgenres_report
    )

    print(full_report)

    with open("data/processed/report.txt", "w", encoding="utf-8") as file:
        file.write(full_report)

if __name__ == "__main__":
    main()
