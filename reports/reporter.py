def build_report(results: list[tuple[str, float, int, int]]) -> str:
    lines = []
    lines.append("TRENDS MINER REPORT")
    lines.append("=" * 30)
    lines.append("TOP TERMOS EMERGENTES:\n")
    
    for i, (term, score, curr, prev) in enumerate(results[:10], start=1):
        lines.append(f"{i}. {term} | score={score:.2f} | atual={curr} | anterior={prev}")
    
    return "\n".join(lines)