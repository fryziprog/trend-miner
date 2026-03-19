import pandas as pd
from collections import Counter

from processing.cleaner import clean_text
from processing.tokenizer import tokenize
from processing.ngrams import generate_ngrams
from analysis.common import split_last_periods, compare_counters, rank_counter


BR_SCENE_KEYWORDS = {
    "sp",
    "sao paulo",
    "rj",
    "rio",
    "rio de janeiro",
    "bh",
    "belo horizonte",
    "fortaleza",
    "recife",
    "salvador",
    "brasilia",
    "goiania",
    "curitiba",
    "porto alegre"
}


def extract_br_scene_signals(titles):
    counter = Counter()

    for title in titles:
        cleaned = clean_text(title)
        tokens = tokenize(cleaned)

        unigrams = set(tokens)
        bigrams = set(generate_ngrams(tokens, 2))
        trigrams = set(generate_ngrams(tokens, 3))

        all_items = unigrams | bigrams | trigrams

        for item in all_items:
            if item in BR_SCENE_KEYWORDS:
                counter[item] += 1

    return counter


def compare_br_scene_last_periods(df: pd.DataFrame, days_current: int = 7, days_previous: int = 7):
    previous_df, current_df = split_last_periods(df, days_current, days_previous)

    prev_counter = extract_br_scene_signals(previous_df["title"])
    curr_counter = extract_br_scene_signals(current_df["title"])

    return compare_counters(prev_counter, curr_counter)


def rank_current_br_scenes(df: pd.DataFrame, days_current: int = 7):
    _, current_df = split_last_periods(df, days_current, days_previous=1)

    counter = extract_br_scene_signals(current_df["title"])
    return rank_counter(counter)