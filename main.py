import pandas as pd
from analysis.trends import compare_last_periods
from analysis.spacy_entities import compare_entity_periods
from analysis.subgenres import compare_subgenre_last_periods, rank_current_subgenres_last_period
from analysis.artist_signals import compare_artist_last_periods, rank_current_artist_signals
from analysis.br_scene_signals import compare_br_scene_last_periods, rank_current_br_scenes
from processing.dataset_filters import filter_relevant_rows, filter_type_beat_rows
from reports.reporter import build_report

def main():
    df = pd.read_csv("data/raw/youtube_music.csv")
    df = filter_relevant_rows(df)
    type_beat_df = filter_type_beat_rows(df)
    
    print("TOTAL ORIGINAL:", len(df))
    print("TOTAL TYPE BEAT:", len(type_beat_df),"\n")
    
    if len(type_beat_df) < 20:
        print(" Usando dataset geeral para subgeneros (fallback)")
        subgenre_df = df
    else:
        subgenre_df = type_beat_df

    # tendências gerais
    unigram_results = compare_last_periods(df, days_current=7, days_previous=7, ngram_size=1)
    bigram_results = compare_last_periods(df, days_current=7, days_previous=7, ngram_size=2)
    trigram_results = compare_last_periods(df, days_current=7, days_previous=7, ngram_size=3)

    # entidades
    entity_results = compare_entity_periods(df, split_date="2026-03-08")

    # subgêneros
    subgenre_results = compare_subgenre_last_periods(subgenre_df, days_current=7, days_previous=7)
    current_subgenres = rank_current_subgenres_last_period(subgenre_df, days_current=7)

    # artistas
    artist_results = compare_artist_last_periods(type_beat_df, days_current=7, days_previous=7)
    current_artists = rank_current_artist_signals(type_beat_df, days_current=7)

    # cenas BR
    br_scene_results = compare_br_scene_last_periods(df, days_current=7, days_previous=7)
    current_br_scenes = rank_current_br_scenes(df, days_current=7)

    # relatórios principais
    unigram_report = build_report(unigram_results, title="TREND MINER REPORT - UNIGRAMAS")
    bigram_report = build_report(bigram_results, title="TREND MINER REPORT - BIGRAMAS")
    trigram_report = build_report(trigram_results, title="TREND MINER REPORT - TRIGRAMAS")
    entity_report = build_report(entity_results, title="TREND MINER REPORT - ENTIDADES (spaCy)")
    subgenre_report = build_report(subgenre_results, title="TREND MINER REPORT - SUBGENEROS")
    artist_report = build_report(artist_results, title="TREND MINER REPORT - ARTISTAS EMERGENTES")
    br_scene_report = build_report(br_scene_results, title="TREND MINER REPORT - CENAS BR EMERGENTES")

    # subgêneros atuais
    current_subgenre_lines = []
    current_subgenre_lines.append("TREND MINER REPORT - SUBGENEROS ATUAIS")
    current_subgenre_lines.append("=" * 30)
    current_subgenre_lines.append("TOP SUBGENEROS NO PERIODO ATUAL:\n")

    for i, (term, freq) in enumerate(current_subgenres[:10], start=1):
        current_subgenre_lines.append(f"{i}. {term} | freq_atual = {freq}")

    current_subgenres_report = "\n".join(current_subgenre_lines)

    # artistas atuais
    current_artist_lines = []
    current_artist_lines.append("TREND MINER REPORT - ARTISTAS ATUAIS")
    current_artist_lines.append("=" * 30)
    current_artist_lines.append("TOP ARTISTAS NO PERIODO ATUAL:\n")

    for i, (term, freq) in enumerate(current_artists[:10], start=1):
        current_artist_lines.append(f"{i}. {term} | freq_atual = {freq}")

    current_artists_report = "\n".join(current_artist_lines)

    # cenas BR atuais
    current_br_scene_lines = []
    current_br_scene_lines.append("TREND MINER REPORT - CENAS BR ATUAIS")
    current_br_scene_lines.append("=" * 30)
    current_br_scene_lines.append("TOP CENAS BR NO PERIODO ATUAL:\n")

    for i, (term, freq) in enumerate(current_br_scenes[:10], start=1):
        current_br_scene_lines.append(f"{i}. {term} | freq_atual = {freq}")

    current_br_scenes_report = "\n".join(current_br_scene_lines)

    # relatório final
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
        + "\n\n"
        + artist_report
        + "\n\n"
        + current_artists_report
        + "\n\n"
        + br_scene_report
        + "\n\n"
        + current_br_scenes_report
    )

    print(full_report)

    with open("data/processed/report.txt", "w", encoding="utf-8") as file:
        file.write(full_report)
        
    

if __name__ == "__main__":
    main()