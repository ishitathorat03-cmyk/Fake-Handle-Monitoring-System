from flask import Flask, render_template, request
import pandas as pd
from analyzer import analyze_handle

app = Flask(__name__)

DATA_FILE = "data/handles.csv"

# Existing sample monitoring data
df = pd.read_csv(DATA_FILE)

monitoring_results = []

for _, row in df.iterrows():
    monitoring_results.append(analyze_handle(row))


@app.route("/", methods=["GET", "POST"])
def dashboard():

    analysis_result = None

    if request.method == "POST":

        handle = request.form.get("handle", "").strip()
        platform = request.form.get("platform", "X")
        display_name = request.form.get("display_name", "").strip()
        account_age = request.form.get("account_age", "0")
        followers = request.form.get("followers", "0")
        following = request.form.get("following", "0")

        official_claim = request.form.get("official_claim") == "on"
        verified = request.form.get("verified") == "on"
        external_link_match = request.form.get("external_link_match") == "on"

        if handle:

            row = {
                "handle": handle.replace("@", ""),
                "platform": platform,
                "display_name": display_name or handle,
                "bio": "",
                "account_age_days": int(account_age or 0),
                "followers": int(followers or 0),
                "following": int(following or 0),
                "verified": verified,
                "official_claim": official_claim,
                "external_link_match": external_link_match
            }

            analysis_result = analyze_handle(row)

    low = sum(r["level"] == "LOW" for r in monitoring_results)
    medium = sum(r["level"] == "MEDIUM" for r in monitoring_results)
    high = sum(r["level"] == "HIGH" for r in monitoring_results)
    critical = sum(r["level"] == "CRITICAL" for r in monitoring_results)

    sorted_results = sorted(
        monitoring_results,
        key=lambda x: x["score"],
        reverse=True
    )

    return render_template(
        "index.html",
        results=sorted_results,
        total=len(monitoring_results),
        low=low,
        medium=medium,
        high=high,
        critical=critical,
        analysis=analysis_result
    )


@app.route("/add", methods=["POST"])
def add_to_monitoring():

    handle = request.form.get("handle", "")
    platform = request.form.get("platform", "")
    display_name = request.form.get("display_name", "")
    score = int(request.form.get("score", 0))
    level = request.form.get("level", "")
    similarity = float(request.form.get("similarity", 0))
    reasons = request.form.getlist("reasons")

    result = {
        "handle": handle,
        "platform": platform,
        "display_name": display_name,
        "score": score,
        "level": level,
        "similarity": similarity,
        "reasons": reasons
    }

    monitoring_results.append(result)

    return render_template(
        "index.html",
        results=sorted(
            monitoring_results,
            key=lambda x: x["score"],
            reverse=True
        ),
        total=len(monitoring_results),
        low=sum(r["level"] == "LOW" for r in monitoring_results),
        medium=sum(r["level"] == "MEDIUM" for r in monitoring_results),
        high=sum(r["level"] == "HIGH" for r in monitoring_results),
        critical=sum(r["level"] == "CRITICAL" for r in monitoring_results),
        analysis=None,
        added=True
    )


if __name__ == "__main__":
    app.run(debug=True)