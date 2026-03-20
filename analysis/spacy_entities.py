import spacy
import pandas as pd
import html
import re
from collections import Counter
from analysis.common import compare_counters

nlp = spacy.load("en_core_web_sm")

ALLOWED_LABELS = {"PERSON", "ORG", "GPE", "WORK_OF_ART"}

BAD_ENTITY_PARTS ={
    "free", 
    "type",
    "beat",
    "instrumental",
    "prod",
    "official",
    "audio",
    "video", 
    "lyrics",
    "mix", 
    "playlist",
    "beats", 
    "audio",
    "brand", 
    "new",
    "melodic",
    "trap",
    "drill",
    "rage",
    "freestyle",
    "hard",
    "plug"
}
BAD_ENTITY_EXACT ={
    "alpha", 
    "basics", 
    "chill guitar", 
    "brand new 2026 pluggnb",
    "esquece",
    "hills",
    "treino",
    "noite sem pressa",
    "sinto livre"
}

BAD_ENTITY_EXACT = {
    "alpha",
    "basics",
    "chill guitar",
    "brand new 2026 pluggnb",
    "esquece",
    "hills",
    "treino",
    "melodic",
    "noite sem pressa",
    "sinto livre",
    "afrobeat",
    "erikebeats",
    "hills trap"
}

BAD_ENTITY_PARTS = {
    "free",
    "type",
    "beat",
    "beats",
    "instrumental",
    "prod",
    "official",
    "lyrics",
    "video",
    "audio",
    "brand",
    "new",
    "melodic",
    "trap",
    "drill",
    "plug",
    "rage",
    "mix",
    "playlist",
    "freestyle",
    "hard",
}

KNOWN_RELEVANT_ENTITIES = {
    "veigh",
    "alee",
    "matue",
    "wiu",
    "yunk vino",
    "kayblack",
    "orochi",
    "vulgo fk",
    "tz da coronel",
    "caio luccas",
    "leviano",
    "brandao",
    "brandao85",
    "hoodtrap",
    "cjota",
    "chefin",
    "borges",
    "oruam",
    "ryu the runner",
    "don toliver",
    "travis scott",
    "future",
    "playboi carti",
    "ken carson",
    "yeat",
    "cabelinho",
    "filipe ret",
    "mc poze do rodo",
    "mc cabelinho",
    "js da torre",
    "pedrin",
    "nagalli",
    "lb unico",
    "raflow",
    "niink",
    "klisman",
    "romano",
    "senndy",
    "mateca",
    "reid",
    "fab godamn",
    "franco the sir",
    "franco",
    "earkid",
    "doode",
    "sotam",
    "bryson tiller",
    "kanye west",
    "vulgo fk",
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

    if all(len(word) == 1 for word in words):
        return False
    
    if any(word in BAD_ENTITY_PARTS for word in words):
        return False
    
    if text in KNOWN_RELEVANT_ENTITIES:
        return False
    
    if label not in ALLOWED_LABELS:
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
    
    
    return compare_counters(prev_entities, curr_entities)
    