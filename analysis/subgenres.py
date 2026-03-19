from collections import Counter
import pandas as pd

from processing.cleaner import clean_text
from processing.tokenizer import tokenize
from processing.ngrams import generate_ngrams
from analysis.common import split_last_periods, compare_counters, rank_counter
from analysis.common import split_last_periods, get_current_period, compare_counters, rank_counter

SUBGENRE_KEYWORDS = {
    "dark trap",
    "memphis trap",
    "detroit trap",
    "flint trap",
    "pluggnb",
    "afro house",
    "jersey club",
    "rage trap",
    "phonk trap",
    "drill",
    "trapsoul",
    "boom bap",
    "ambient trap"
}


def extract_subgenre_signals(titles):
    counter = Counter()

    for title in titles:
        cleaned = clean_text(title)
        tokens = tokenize(cleaned)

        unigrams = set(tokens)
        bigrams = set(generate_ngrams(tokens, 2))
        trigrams = set(generate_ngrams(tokens, 3))

        all_items = unigrams | bigrams | trigrams

        for item in all_items:
            if item in SUBGENRE_KEYWORDS:
                counter[item] += 1

    return counter

def compare_subgenre_periods(df: pd.DataFrame, split_date: str):

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    split = pd.to_datetime(split_date)

    previous_df = df[df["date"] < split]
    current_df = df[df["date"] >= split]

    prev_counter = extract_subgenre_signals(previous_df["title"])
    curr_counter = extract_subgenre_signals(current_df["title"])

    all_terms = set(prev_counter.keys()) | set(curr_counter.keys())
    results = []

    for term in all_terms:

        prev_freq = prev_counter.get(term, 0)
        curr_freq = curr_counter.get(term, 0)

        if curr_freq == 0:
            continue

        score = (curr_freq + 1) / (prev_freq + 1)

        results.append((term, score, curr_freq, prev_freq))

    results.sort(key=lambda x: (-x[1], -x[2], x[0]))

    return results

def rank_current_subgeners(df: pd.DataFrame, split_date: str):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    split = pd.to_datetime(split_date)
    
    current_df = df[df["date"] >= split]
    counter = extract_subgenre_signals(current_df["title"])
    
    results = []
    
    for term, freq in counter.items():
        results.append((term, freq))
    
    results.sort(key=lambda x: (-x[1], x[0]))
    return results

def compare_subgenre_last_periods(df: pd.DataFrame, days_current: int = 7, days_previous: int = 7):
    previous_df, current_df = split_last_periods(df, days_current, days_previous)
    
    prev_counter = extract_subgenre_signals(previous_df["title"])
    curr_counter = extract_subgenre_signals(current_df["title"])
    
    return compare_counters(prev_counter, curr_counter)
    
def rank_current_subgenres_last_period(df: pd.DataFrame, days_current: int = 7):
    _, current_df = split_last_periods(df, days_current, days_previous=1)
    
    counter = extract_subgenre_signals(current_df["title"])
    return rank_counter(counter)
            
