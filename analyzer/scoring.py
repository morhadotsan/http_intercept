MAX_SCORE = 100


def grade(score):
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    if score >= 40: return "E"
    return "F"


def score_results(results):
    earned = sum(r["points"] for r in results)
    score = max(0, min(MAX_SCORE, earned))
    return score, grade(score)
