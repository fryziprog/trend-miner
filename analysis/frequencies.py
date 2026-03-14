from collections import Counter

def count_tokens(token_lists: list[list[str]]) -> Counter:
    counter = Counter()
    for tokens in token_lists:
        counter.update(tokens)
        return counter
    