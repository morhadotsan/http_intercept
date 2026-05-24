BASELINE_SCORE = 100
MIN_SCORE = 0
MAX_SCORE = 145


def grade(score):
    if score >= 100: return "A+"
    if score >= 90:  return "A"
    if score >= 85:  return "A-"
    if score >= 80:  return "B+"
    if score >= 70:  return "B"
    if score >= 65:  return "B-"
    if score >= 60:  return "C+"
    if score >= 50:  return "C"
    if score >= 45:  return "C-"
    if score >= 40:  return "D+"
    if score >= 30:  return "D"
    if score >= 25:  return "D-"
    return "F"


def score_results(results):
    penalties = sum(r["points"] for r in results if r["points"] < 0)
    bonuses   = sum(r["points"] for r in results if r["points"] > 0)

    score = BASELINE_SCORE + penalties
    if score >= 90:
        score += bonuses

    score = max(MIN_SCORE, min(MAX_SCORE, score))
    return score, grade(score)
