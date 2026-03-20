import pandas as pd
import re
from collections import Counter
from processing.cleaner import clean_text
from analysis.common import split_last_periods, compare_counters, rank_counter

PATTERNS = [
    r"(.+?)\s+type\s+beat",
    r"(.+?)\s+tipo\s+beat",
    r"(.+?)\s+estilo",
    r"(.+?)\s+style",
    r"(.+?)\s+inspired\s+by",
    r"(.+?)\s+inspirado\s+em",
]

BAD_PREFIX_WORDS = {
    "free", " dark", " hard", " beat", " new", " trap"," drill"," rage", "br",
    "brasil", "prod", "by", "profit", "x"

}

BAD_ARTIST_TERMERS = {
    "trap", "drill", "plug", "pluggnb", "rage",
    "dark trap", "brazilian funk", "afro rnb",
    "rnb", "funk", "beat", "type"," afro", "g a", "x"
    
}
KNOWN_ARTISTS = {
    "matue",
    "veigh",
    "alee",
    "teto",
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
    "ye",
    "kanye west",
}
def strip_beat_name(title: str) -> str:
    parts = re.split(r"\s[-]]\s", str(title), maxsplit=1)
    return parts[0].strip()

def remove_promotional_prefix(text: str) -> str:
    text = re.sub(r"^\s*\[.*?\]\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*free\s+for\s+profit\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*for\s+profit\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*free\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*prod\s+by\s+", "", text, flags=re.IGNORECASE)
    return text.strip()

def normalize_artist_candidate(text: str) -> str:
    text = remove_promotional_prefix(text)
    text = clean_text(text)
    words = text.split()
    
    while words and words[0] in BAD_PREFIX_WORDS:
        words.pop(0)
        
    return " ".join(words).strip()


def split_artist_collab(text: str) -> list[str]:
    parts = re.split(r"\s+x\s+|,|&", text, flags=re.IGNORECASE)
    cleaned_parts = []
    
    for part in parts:
        part = part.strip()
        
        if not part:
            continue
        
        if len(part) < 3:
            continue
        cleaned_parts.append(part)
    
    return cleaned_parts

def is_valid_artist(text: str) -> bool:
    if len(text) < 3:
        return False
    
    if text in BAD_ARTIST_TERMERS:
        return False
    
    words = text.split()
    
    if len(words) > 4:
        return False
    
    if all(len(word) == 1 for word in words):
        return False
    
    banned_parts = {
        "trap", "drill", "plug", "pluggnb", "rage",
        "funk", "rnb", "afro", "beat", "type", "melodic"
    }
    
    if any(word in banned_parts for word in words):
        return False
    
    return True

def extract_known_artists_from_text(text: str) -> list[str]:
    found = []
    
    for artist in KNOWN_ARTISTS:
        if artist in text:
            found.append(artist)
    return found

def extract_artist_signals(titles):
    counter = Counter()

    for title in titles:
        raw_title = strip_beat_name(title)

        # 1. detectar artistas conhecidos diretamente no título limpo
        normalized_title = clean_text(remove_promotional_prefix(raw_title))
        direct_artists = extract_known_artists_from_text(normalized_title)

        for artist in direct_artists:
            counter[artist] += 1

        # 2. detectar via padrões tipo "X type beat"
        for pattern in PATTERNS:
            match = re.search(pattern, raw_title, flags=re.IGNORECASE)

            if not match:
                continue

            candidate = normalize_artist_candidate(match.group(1))

            if is_valid_artist(candidate):
                counter[candidate] += 1

            artists = split_artist_collab(candidate)
            for artist in artists:
                if is_valid_artist(artist):
                    counter[artist] += 1

    return counter

def compare_artist_last_periods(df: pd.DataFrame, days_current: int = 7, days_previous: int = 7):

    previous_df, current_df = split_last_periods(df, days_current, days_previous)

    prev_counter = extract_artist_signals(previous_df["title"])
    curr_counter = extract_artist_signals(current_df["title"])
    
    return compare_counters(prev_counter, curr_counter)
    
def rank_current_artist_signals(df:pd.DataFrame, days_current: int = 7):
    _, current_df = split_last_periods(df, days_current, days_previous =1)
    
    counter = extract_artist_signals(current_df["title"])
    return rank_counter(counter)
   