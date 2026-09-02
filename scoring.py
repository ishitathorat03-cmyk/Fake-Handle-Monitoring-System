def calculate_risk(data):

    score = 0
    reasons = []

    similarity = data.get("similarity", 0)

    if similarity >= 0.85:
        score += 25
        reasons.append("High username similarity")
    elif similarity >= 0.65:
        score += 15
        reasons.append("Moderate username similarity")

    if data.get("official_claim"):
        score += 20
        reasons.append("Claims official affiliation")

    if data.get("account_age_days", 9999) < 30:
        score += 15
        reasons.append("Recently created account")

    if not data.get("verified"):
        score += 10
        reasons.append("No verification indicator")

    if not data.get("external_link_match"):
        score += 15
        reasons.append("External link mismatch")

    if data.get("following", 0) > data.get("followers", 1) * 2:
        score += 5
        reasons.append("Unusual follower/following pattern")

    score = min(score, 100)

    if score >= 81:
        level = "CRITICAL"
    elif score >= 61:
        level = "HIGH"
    elif score >= 31:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level, reasons