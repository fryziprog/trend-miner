import re
import html
from unidecode import unidecode

def clean_text(text: str) -> str:
    text = str(text)
    text = html.unescape(text)   # converte &quot; em "
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def strip_type_beat_extras(text: str) -> str:
    text = str(text)
    
    for sep in ["|", "~"]:
        if sep in text:
            text = text.split(sep)[0]
    return text.strip()