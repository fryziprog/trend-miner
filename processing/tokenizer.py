from processing.stopwords import STOPWORDS

def tokenize(text: str) -> list[str]:
    tokens = text.split()
    tokens = [
        token for token in tokens
        if token not in STOPWORDS
        and len(token) > 2
        and not token.isdigit()
    ]
    return tokens