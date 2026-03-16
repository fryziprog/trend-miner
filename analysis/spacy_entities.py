import spacy
import pandas as pd
import html
import re
from collections import Counter

nlp = spacy.load("en_core_web_sm")

ALLOWED_LABELS = {"PERSON", "ORG", "GPE", "WORK_OF_ART"}

BAD_ENTITY_PARTS ={
    "free", "type", "beat", "instrumental", "prod", "official",
    "audio", "video", "lyrics", "mix", "playlist", "beats", "audio",
    "brand", "new"
}
BAD_ENTITY_EXACT ={
    "alpha", "basics", "chill guitar", "brand new 2026 pluggnb"
}
def normalize_entity_text(text: str) -> str:
    text = html.unescape(str(text))
    text = text.lower().strip()
    text = re.sub(r"[\[\]\(\)\{\}\"'“”‘’]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_valid_entity(text: str, label: str) -> bool:
    if label not in ALLOWED_LABELS:
        return False
    
    if len(text) < 3:
        return False
    
    if text.isdigit():
        return False
    
    if text in BAD_ENTITY_EXACT:
        return False
    
    words = text.split()
    
    if len(words) > 4:
        return False
    
    if any(word in BAD_ENTITY_PARTS for word in words):
        return False
    
    return True

def extract_entities(titles):
    counter = Counter()
    
    for title in titles:
        clean_title = html.unescape(str(title))
        doc = nlp(clean_title)
        
        for ent in doc.ents:
            text = normalize_entity_text(ent.text)
            
            if not is_valid_entity(text, ent.label_):
                continue
            
            counter[text] += 1
            
    return counter

def compare_entity_periods(df: pd.DataFrame, split_date: str):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    split = pd.to_datetime(split_date)
    
    previous_df = df[df["date"] < split]
    current_df = df[df["date"] >= split]
    
    prev_entities = extract_entities(previous_df["title"])
    curr_entities = extract_entities(current_df["title"])
    
    all_entities = set(prev_entities.keys()) | set(curr_entities.keys())
    results = []

    for entity in all_entities:
        prev_freq = prev_entities.get(entity, 0)
        curr_freq = curr_entities.get(entity, 0)

        if curr_freq == 0:
            continue

        score = (curr_freq + 1) / (prev_freq + 1)
        results.append((entity, score, curr_freq, prev_freq))

    results.sort(key=lambda x: (-x[1], -x[2], x[0]))
    return results
    