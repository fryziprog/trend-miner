from collections import Counter
from processing.cleaner import clean_text
from processing.tokenizer import tokenize
from processing.ngrams import generate_ngrams

#Ele pega todos os títulos e conta:
#bigramas
#trigramas
#Essas combinações viram candidatas a entidades.

def extract_candidate_entities(titles) -> Counter:
    counter = Counter()
    
    for title in titles:
        cleaned = clean_text(title)
        tokens = tokenize(cleaned)
        
        bigrams = generate_ngrams(tokens, 2)
        trigrams = generate_ngrams(tokens, 3)
        
        for item in bigrams + trigrams:
            counter[item] += 1
            
    return counter

import pandas as pd

#É a mesma lógica do compare_periods, mas focada em possíveis entidades
def compare_entity_periods(df: pd.DataFrame, split_date: str):
    df["date"] = pd.to_datetime(df["date"])
    split = pd.to_datetime(split_date)
    
    previous_df = df[df["date"] < split]
    current_df = df[df["date"] >= split]
    
    previous_counter = extract_candidate_entities(previous_df["title"])
    current_counter = extract_candidate_entities(current_df["title"])
    
    all_entities = set(previous_counter.keys()) | set(current_counter.keys())
    results = []
    
    for entity in all_entities:
        prev_freq = previous_counter.get(entity, 0)
        curr_freq = current_counter.get(entity, 0)
        
        if curr_freq == 0:
            continue
        
        score = (curr_freq + 1) / (prev_freq + 1)       
        results.append((entity, score, curr_freq, prev_freq))
        
    results.sort(key=lambda x: (-x[1], -x[2], x[0]))
    return results   