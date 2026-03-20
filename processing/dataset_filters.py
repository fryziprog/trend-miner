from processing.cleaner import clean_text

BAD_TITLE_TERMS = {
    "playlist",
    "mix",
    "react",
    "tierlist",
    "analisando",
    "review",
    "melhores",
    "best",
    "set trap",
    "clipe oficial",
    "official music video",
    "official audio",
    "ep completo",
    "shorts",
    "spotify",
    "verdade sobre",
    "videos que voce precisa assistir",
    "audio oficial",
    "music video",
}

BAD_CHANNEL_TERMS = {
    "viral hits",
    "qg do maik",
    "thief reage",
    "hip hop brasil"
    "som music brazil"
}

def is_relevant_title(title: str) -> bool:
    text = clean_text(title)
    
    for term in BAD_TITLE_TERMS:
        if term in text:
            return False
    return True

def is_relevant_source(source: str) -> bool:
    text = clean_text(source)
    
    for term in BAD_CHANNEL_TERMS:
        if term in text:
            return False
    return True

def filter_relevant_rows(df):
    df = df.copy()
    
    mask = df.apply(
        lambda row: is_relevant_title(str(row["title"])) and is_relevant_source(str(row["source"])),
        axis = 1
    )
    
    return df[mask].copy()

def filter_type_beat_rows(df):
    df = df.copy()
    
    mask = df["title"].astype(str).str.lower().apply(
        lambda text: (
            "type beat" in text
            or "tipo beat" in text
            or "estilo" in text
            or "typebeat" in text
            or "trap type" in text
            or "free" in text
            or "(free)" in text
            or "[free]" in text
        )
    )
    
    return df[mask].copy()

