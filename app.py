import streamlit as st
import pandas as pd
from analyzer import analyze_handle

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Fake Handle Monitoring System",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Load Existing Monitoring Data
# -----------------------------
DATA_FILE = "data/handles.csv"

df = pd.read_csv(DATA_FILE)

monitoring_results = []

for _, row in df.iterrows():
    monitoring_results.append(analyze_handle(row))


# -----------------------------
# Header
# -----------------------------
st.title("🛡️ Fake Handle Monitoring System")
st.caption("OSINT-based social media handle analysis and monitoring")


# -----------------------------
# Statistics
# -----------------------------
low = sum(r["level"] == "LOW" for r in monitoring_results)
medium = sum(r["level"] == "MEDIUM" for r in monitoring_results)
high = sum(r["level"] == "HIGH" for r in monitoring_results)
critical = sum(r["level"] == "CRITICAL" for r in monitoring_results)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Handles", len(monitoring_results))
col2.metric("LOW", low)
col3.metric("MEDIUM", medium)
col4.metric("HIGH", high)
col5.metric("CRITICAL", critical)


st.divider()


# -----------------------------
# Analyze New Handle
# -----------------------------
st.subheader("🔍 Analyze a Social Media Handle")

with st.form("handle_analysis_form"):

    col1, col2 = st.columns(2)

    with col1:
        handle = st.text_input(
            "Handle",
            placeholder="@example_handle"
        )

        platform = st.selectbox(
            "Platform",
            ["X", "Instagram", "Facebook", "Other"]
        )

        display_name = st.text_input(
            "Display Name"
        )

        account_age = st.number_input(
            "Account Age (days)",
            min_value=0,
            value=0
        )

    with col2:
        followers = st.number_input(
            "Followers",
            min_value=0,
            value=0
        )

        following = st.number_input(
            "Following",
            min_value=0,
            value=0
        )

        verified = st.checkbox("Verified Account")
        official_claim = st.checkbox("Claims to be Official")
        external_link_match = st.checkbox(
            "External Link Matches Official Source"
        )

    submitted = st.form_submit_button(
        "Analyze Handle"
    )


# -----------------------------
# Analysis
# -----------------------------
if submitted:

    if not handle.strip():

        st.warning("Please enter a handle.")

    else:

        row = {
            "handle": handle.replace("@", ""),
            "platform": platform,
            "display_name": display_name or handle,
            "bio": "",
            "account_age_days": int(account_age),
            "followers": int(followers),
            "following": int(following),
            "verified": verified,
            "official_claim": official_claim,
            "external_link_match": external_link_match
        }

        analysis_result = analyze_handle(row)

        st.divider()
        st.subheader("📊 Analysis Result")

        score = analysis_result["score"]
        level = analysis_result["level"]
        similarity = analysis_result.get("similarity", 0)
        reasons = analysis_result.get("reasons", [])

        col1, col2, col3 = st.columns(3)

        col1.metric("Risk Score", score)
        col2.metric("Risk Level", level)
        col3.metric("Similarity", similarity)

        if level == "CRITICAL":
            st.error("🚨 CRITICAL RISK")
        elif level == "HIGH":
            st.error("⚠️ HIGH RISK")
        elif level == "MEDIUM":
            st.warning("⚠️ MEDIUM RISK")
        else:
            st.success("✅ LOW RISK")

        if reasons:
            st.write("### Reasons")

            for reason in reasons:
                st.write(f"• {reason}")


# -----------------------------
# Monitoring Dashboard
# -----------------------------
st.divider()

st.subheader("📋 Monitoring Results")

sorted_results = sorted(
    monitoring_results,
    key=lambda x: x["score"],
    reverse=True
)

if sorted_results:

    table_data = []

    for result in sorted_results:

        table_data.append({
            "Handle": result.get("handle", ""),
            "Platform": result.get("platform", ""),
            "Display Name": result.get("display_name", ""),
            "Risk Score": result.get("score", 0),
            "Risk Level": result.get("level", ""),
            "Similarity": result.get("similarity", 0)
        })

    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No monitoring results available.")


# -----------------------------
# Add New Result to Monitoring
# -----------------------------
st.subheader("➕ Add Analysis to Monitoring")

with st.form("add_monitoring_form"):

    add_handle = st.text_input("Handle", key="add_handle")
    add_platform = st.text_input("Platform", key="add_platform")
    add_display_name = st.text_input(
        "Display Name",
        key="add_display_name"
    )

    add_score = st.number_input(
        "Score",
        min_value=0,
        value=0,
        key="add_score"
    )

    add_level = st.selectbox(
        "Risk Level",
        ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        key="add_level"
    )

    add_similarity = st.number_input(
        "Similarity",
        min_value=0.0,
        value=0.0,
        key="add_similarity"
    )

    add_reasons = st.text_area(
        "Reasons (one per line)",
        key="add_reasons"
    )

    add_submitted = st.form_submit_button(
        "Add to Monitoring"
    )


if add_submitted:

    if add_handle.strip():

        new_result = {
            "handle": add_handle,
            "platform": add_platform,
            "display_name": add_display_name,
            "score": int(add_score),
            "level": add_level,
            "similarity": float(add_similarity),
            "reasons": [
                r.strip()
                for r in add_reasons.splitlines()
                if r.strip()
            ]
        }

        monitoring_results.append(new_result)

        st.success(
            f"@{add_handle.replace('@', '')} added to monitoring."
        )

        st.rerun()

    else:

        st.warning("Please enter a handle.")
