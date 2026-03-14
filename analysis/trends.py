import pandas as pd
from analysis.frequencies import count_tokens
from processing.cleaner import clean_text
from processing.tokenizer import tokenize

def build_counter_from_titles(titles) -> dict:
    token_lists = []
    for title in titles:
        cleaned = clean_text(title)
        tokens = tokenize(cleaned)
        token_lists.append(tokens)
        return count_tokens(token_lists)

def compare_periods(df: pd.DataFrame, split_date: str) -> list[tuple[str, float, int, int]]:
    df["date"] = pd.to_datetime(df["date"])
    
    split = pd.to_datetime(split_date)
    
    previous_df = df[df["date"] < split]
    current_df = df[df["date"] >= split]
    
    previous_counter = build_counter_from_titles(previous_df["title"])
    current_counter = build_counter_from_titles(current_df["title"])
    
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
      
    