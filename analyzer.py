from difflib import SequenceMatcher
from scoring import calculate_risk


REFERENCE_NAME = "Indian Army"


def to_bool(value):
    if isinstance(value, bool):
        return value

    return str(value).strip().lower() in ["true", "yes", "1", "on"]


def username_similarity(handle):

    clean_handle = (
        handle.lower()
        .replace("_", "")
        .replace("-", "")
        .replace(".", "")
        .replace("@", "")
    )

    reference = REFERENCE_NAME.lower().replace(" ", "")

    return SequenceMatcher(
        None,
        clean_handle,
        reference
    ).ratio()


def analyze_handle(row):

    similarity = username_similarity(row["handle"])

    data = {
        "similarity": similarity,
        "official_claim": to_bool(row["official_claim"]),
        "account_age_days": int(row["account_age_days"]),
        "verified": to_bool(row["verified"]),
        "external_link_match": to_bool(row["external_link_match"]),
        "followers": int(row["followers"]),
        "following": int(row["following"])
    }

    score, level, reasons = calculate_risk(data)

    return {
        "handle": row["handle"],
        "platform": row["platform"],
        "display_name": row["display_name"],
        "similarity": round(similarity * 100, 1),
        "score": score,
        "level": level,
        "reasons": reasons
    }