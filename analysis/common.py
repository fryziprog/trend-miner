import pandas as pd


def split_last_periods(df: pd.DataFrame, days_current: int = 7, days_previous: int = 7):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    max_date = df["date"].max().normalize()

    current_start = max_date - pd.Timedelta(days=days_current - 1)
    previous_end = current_start - pd.Timedelta(days=1)
    previous_start = previous_end - pd.Timedelta(days=days_previous - 1)

    current_df = df[(df["date"] >= current_start) & (df["date"] <= max_date)]
    previous_df = df[(df["date"] >= previous_start) & (df["date"] <= previous_end)]

    return previous_df, current_df

def get_current_period(df: pd.DataFrame, days_current: int = 7):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    max_date = df["date"].max().normalize()
    current_start = max_date - pd.Timedelta(days=days_current - 1)
    
    current_df = df[(df["date"] >= current_start) &(df["date"] <= max_date)]
    return current_df

def compare_counters(previous_counter, current_counter):
    all_terms = set(previous_counter.keys()) | set(current_counter.keys())
    results = []

    for term in all_terms:
        prev_freq = previous_counter.get(term, 0)
        curr_freq = current_counter.get(term, 0)

        if curr_freq == 0:
            continue

        score = (curr_freq + 1) / (prev_freq + 1)
        results.append((term, score, curr_freq, prev_freq))

    results.sort(key=lambda x: (-x[1], -x[2], x[0]))
    return results


def rank_counter(counter):
    results = [(term, freq) for term, freq in counter.items()]
    results.sort(key=lambda x: (-x[1], x[0]))
    return results