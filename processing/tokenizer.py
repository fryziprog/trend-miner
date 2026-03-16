from processing.stopwords import STOPWORDS

def tokenize(text: str) -> list[str]:
    tokens = text.split()
    tokens = [
        token for token in tokens
        if token not in STOPWORDS
        and len(token) > 2
        and not token.isdigit()
    ]
    
    #remover repeticoes consecutivas
    
    cleaned = []
    prev = None
    
    for token in tokens:
        if token != prev:
            cleaned.append(token)
        prev = token
        
    return cleaned