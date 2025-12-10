import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob

# Set up the main Streamlit page layout and basic configuration
st.set_page_config(
    page_title="USAA Fraud Article Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple title that tells the user what this app is focused on
st.title("USAA Fraud Article Intelligence Dashboard (ACFE Source)")

# Load the summarized fraud article data from the CSV file
def load_data():
    # Reading in the data that comes from the earlier scraping and summarization step
    df = pd.read_csv("fraud_articles_summarized.csv")
    # Some rows may not have keywords yet, so I fill them with empty strings
    if "keywords_found" not in df.columns:
        df["keywords_found"] = ""
    df["keywords_found"] = df["keywords_found"].fillna("")
    # Same idea for the summary text, just making sure we do not get NaN issues later
    if "summary" not in df.columns:
        df["summary"] = ""
    df["summary"] = df["summary"].fillna("")
    return df

df = load_data()

# Assign a simple fraud trend label based on detected keywords
if "trend" not in df.columns:
    def get_trend(keywords_str: str) -> str:
        # Convert to lower case once so the checks are easier to write and read
        ks = str(keywords_str).lower()
        if "money laundering" in ks:
            return "Money Laundering"
        if "embezzlement" in ks:
            return "Embezzlement"
        if "bribery" in ks:
            return "Bribery or Corruption"
        if "scam" in ks or "fraud investigation" in ks:
            return "Scams or Fraud Cases"
        # If we do not see any of our core terms, we treat it as a general or uncategorized case
        if ks.strip() == "":
            return "Uncategorized"
        return "General Fraud"
    # Apply the trend logic once up front so the rest of the app can use it
    df["trend"] = df["keywords_found"].apply(get_trend)

# Turn the comma separated keyword string into a list and count how many items there are
def parse_keywords(s):
    if pd.isna(s):
        return []
    # Here I trim extra spaces and drop any empty fragments
    return [kw.strip().lower() for kw in str(s).split(",") if kw.strip()]

df["keyword_list"] = df["keywords_found"].apply(parse_keywords)
df["keyword_count"] = df["keyword_list"].apply(len)

# Compute a simple severity score using the keywords we detect
def compute_severity(keyword_list):
    # I split these into high and medium risk for clarity when explaining to stakeholders
    high_risk_terms = {"money laundering", "embezzlement", "bribery"}
    medium_risk_terms = {"fraud investigation", "scam"}
    score = 0.0
    # Each keyword pushes the score upward depending on its risk level
    for kw in keyword_list:
        if kw in high_risk_terms:
            score += 0.4
        elif kw in medium_risk_terms:
            score += 0.2
        else:
            score += 0.1
    # Clip the score into the zero to one range so it stays on a familiar scale
    score = max(0.0, min(score, 1.0))
    return score

df["severity_score"] = df["keyword_list"].apply(compute_severity)

# Bucket severity into high, medium, and low levels based on the numeric score
def bucket_severity(score):
    # These thresholds are chosen so that one strong indicator lands in medium
    # and multiple strong indicators push an article into high severity
    if score >= 0.7:
        return "High"
    elif score >= 0.3:
        return "Medium"
    else:
        return "Low"

df["severity_level"] = df["severity_score"].apply(bucket_severity)

# Sidebar filters so the user can slice the data in different ways
st.sidebar.header("Filters")

trend_options = ["All"] + sorted(df["trend"].dropna().unique().tolist())
selected_trend = st.sidebar.selectbox("Filter by fraud trend", trend_options)

severity_options = ["All", "High", "Medium", "Low"]
selected_severity = st.sidebar.selectbox("Filter by severity level", severity_options)

keyword_options = ["All"] + sorted(
    set(
        [
            kw.strip()
            for kws in df["keywords_found"]
            for kw in str(kws).split(",")
            if kw.strip()
        ]
    )
)
selected_keyword = st.sidebar.selectbox("Filter by keyword", keyword_options)

# Apply the selected filters to the dataframe so the rest of the app sees just that slice
filtered_df = df.copy()
if selected_trend != "All":
    filtered_df = filtered_df[filtered_df["trend"] == selected_trend]
if selected_severity != "All":
    filtered_df = filtered_df[filtered_df["severity_level"] == selected_severity]
if selected_keyword != "All":
    filtered_df = filtered_df[
        filtered_df["keywords_found"].str.contains(selected_keyword, case=False)
    ]

st.markdown(f"### Showing {len(filtered_df)} articles after filters")

# Tabs help separate the high level view, the high risk stories, the raw table, and the analyzer tool
tab_overview, tab_highrisk, tab_table, tab_analyzer = st.tabs(
    ["Overview", "Top High Risk Articles", "Data Table", "Fraud Article Analyzer"]
)

# Overview tab: high level metrics and charts that summarize the current filtered view
with tab_overview:
    if filtered_df.empty:
        st.warning("No articles match the current filters.")
    else:
        total_articles = len(filtered_df)
        high_count = (filtered_df["severity_level"] == "High").sum()
        med_count = (filtered_df["severity_level"] == "Medium").sum()
        low_count = (filtered_df["severity_level"] == "Low").sum()

        # Quick metric cards, so someone scanning the page can see the mix at a glance
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total articles", total_articles)
        col2.metric("High severity", int(high_count))
        col3.metric("Medium severity", int(med_count))
        col4.metric("Low severity", int(low_count))

        st.subheader("Summary of current view")
        # Identify the most common trend in the filtered slice
        top_trend = (
            filtered_df["trend"].value_counts().idxmax()
            if not filtered_df["trend"].value_counts().empty
            else "N/A"
        )
        # Collect all keywords so we can talk about which terms dominate this view
        all_keywords = [
            kw
            for kws in filtered_df["keyword_list"]
            for kw in kws
        ]
        keyword_counts = Counter(all_keywords)
        top_keywords = ", ".join([k for k, _ in keyword_counts.most_common(3)]) if keyword_counts else "N/A"
        # This paragraph is written in a plain tone that I would feel comfortable presenting as a student
        summary_text = (
            f"In this view, we are looking at {total_articles} fraud related articles from the ACFE source. "
            f"The most common fraud trend in this part of the data is {top_trend}. "
            f"There are {high_count} high severity, {med_count} medium severity, "
            f"and {low_count} low severity cases based on the language used in each article. "
            f"The most frequently appearing fraud related terms in this view are: {top_keywords}."
        )
        st.write(summary_text)

        st.subheader("Fraud severity distribution")
        severity_counts = (
            filtered_df["severity_level"]
            .value_counts()
            .reindex(["High", "Medium", "Low"])
            .fillna(0)
        )
        fig_sev, ax_sev = plt.subplots()
        severity_counts.plot(kind="bar", ax=ax_sev)
        ax_sev.set_ylabel("Number of articles")
        ax_sev.set_title("Articles by severity level")
        st.pyplot(fig_sev)

        st.subheader("Fraud trend distribution")
        trend_counts = filtered_df["trend"].value_counts()
        fig_trend, ax_trend = plt.subplots()
        trend_counts.plot(kind="bar", ax=ax_trend)
        ax_trend.set_ylabel("Number of articles")
        ax_trend.set_title("Articles by fraud trend")
        st.pyplot(fig_trend)

        st.subheader("Top fraud keywords")
        if keyword_counts:
            top5 = keyword_counts.most_common(5)
            fig_kw, ax_kw = plt.subplots()
            ax_kw.bar([k for k, _ in top5], [v for _, v in top5])
            ax_kw.set_ylabel("Frequency")
            ax_kw.set_title("Top five fraud related keywords")
            st.pyplot(fig_kw)
        else:
            st.info("No keywords are available for the current selection.")

# Top high risk articles tab: surface the most severe cases for quick review
with tab_highrisk:
    st.subheader("Top high risk articles")
    if filtered_df.empty:
        st.info("No articles are available for this view.")
    else:
        # Sort only the high severity cases, then show the ten most severe examples
        high_risk = (
            filtered_df[filtered_df["severity_level"] == "High"]
            .sort_values(by="severity_score", ascending=False)
            .head(10)
        )
        if high_risk.empty:
            st.info("No high risk articles were found for the current filters.")
        else:
            for _, row in high_risk.iterrows():
                st.markdown(f"**{row['title']}**")
                st.markdown(f"- Author: {row['author']}")
                st.markdown(f"- URL: [{row['url']}]({row['url']})")
                st.markdown(f"- Trend: {row['trend']}")
                st.markdown(f"- Severity level: {row['severity_level']} (score: {row['severity_score']:.2f})")
                st.markdown(f"- Keywords: {row['keywords_found']}")
                st.markdown(f"- Summary: {row['summary']}")
                st.markdown("---")

# Data table tab: full filtered table plus an option to export the data
with tab_table:
    st.subheader("Filtered article data")
    if filtered_df.empty:
        st.info("No data is available to display for the current filters.")
    else:
        # This table is helpful for analysts who want to scan the raw records
        st.dataframe(
            filtered_df[
                [
                    "title",
                    "author",
                    "url",
                    "keywords_found",
                    "trend",
                    "keyword_count",
                    "severity_level",
                    "severity_score",
                    "summary",
                ]
            ]
        )
        # Offer a simple way to pull the current slice into a CSV file
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download filtered data as CSV",
            data=csv_data,
            file_name="fraud_articles_filtered.csv",
            mime="text/csv",
        )

# Analyzer tab: score a custom text input using the same rule based logic
with tab_analyzer:
    st.subheader("Fraud article analyzer")
    input_text = st.text_area(
        "Paste an article, blog post, or description of a situation:",
        height=200,
    )
    analyze_button = st.button("Run analysis")

    def analyze_text(text: str):
        # I focus on a small core list of terms to keep the explanation straightforward
        text_lower = text.lower()
        all_keywords = ["embezzlement", "bribery", "fraud investigation", "money laundering", "scam"]
        found_keywords = [kw for kw in all_keywords if kw in text_lower]

        # Trend assignment follows the same style as the main dataset
        if "money laundering" in text_lower:
            trend = "Money Laundering"
        elif "embezzlement" in text_lower:
            trend = "Embezzlement"
        elif "bribery" in text_lower:
            trend = "Bribery or Corruption"
        elif "scam" in text_lower or "fraud investigation" in text_lower:
            trend = "Scams or Fraud Cases"
        elif text.strip() == "":
            trend = "Uncategorized"
        else:
            trend = "General Fraud"

        # Severity and severity level reuse the same scoring logic used for the ACFE articles
        severity_score = compute_severity(found_keywords)
        severity_level = bucket_severity(severity_score)

        # Sentiment is included as extra context about tone rather than as a risk driver
        sentiment = TextBlob(text).sentiment.polarity
        if sentiment <= -0.3:
            tone_label = "strongly negative and focused on incidents or losses"
        elif sentiment >= 0.3:
            tone_label = "more positive and focused on prevention or response"
        else:
            tone_label = "neutral or analytical, closer to an explanation or investigation"

        return {
            "keywords": found_keywords,
            "trend": trend,
            "severity_score": severity_score,
            "severity_level": severity_level,
            "sentiment": sentiment,
            "tone_label": tone_label,
        }

    def build_explanation(result):
        # Turning the numeric output into a short narrative that is easier to talk through in a meeting
        sev = result["severity_level"]
        trend = result["trend"]
        kws = result["keywords"]
        score = result["severity_score"]
        tone_label = result["tone_label"]

        if sev == "High":
            risk_line = (
                f"This text is labeled as high severity with a score around {score:.2f} "
                f"because it includes higher risk fraud language in our current rule set."
            )
            action_line = (
                "In a real setting at USAA, this type of content could be a good candidate for a weekly fraud update "
                "and for more detailed analyst review if it connects to ongoing cases."
            )
        elif sev == "Medium":
            risk_line = (
                f"This text is labeled as medium severity with a score around {score:.2f}. "
                "It points to a meaningful fraud issue but not the highest tier in this simple scoring approach."
            )
            action_line = (
                "For USAA, this type of text is useful for ongoing monitoring and helps show how this trend develops over time, "
                "especially if similar stories begin to appear more often."
            )
        else:
            risk_line = (
                f"This text is labeled as low severity with a score around {score:.2f}. "
                "It likely reflects general commentary, education, or lower impact fraud activity."
            )
            action_line = (
                "For USAA, this kind of content is more helpful for background context and training rather than immediate response."
            )

        if kws:
            kw_line = (
                f"The main fraud terms that influence this assessment are: {', '.join(kws)}."
            )
        else:
            kw_line = (
                "None of the core fraud terms in the current rule set were detected, "
                "so the assessment is mainly driven by general language instead of specific keywords."
            )

        tone_line = f"The overall tone of the text appears {tone_label}."
        trend_line = (
            f"Based on the words used, this text is most closely aligned with the {trend} trend category in the dashboard."
        )

        explanation = " ".join([risk_line, trend_line, kw_line, tone_line, action_line])
        return explanation

    if analyze_button and input_text.strip():
        result = analyze_text(input_text)

        st.subheader("Analysis results")
        st.write(f"Detected keywords: {', '.join(result['keywords']) if result['keywords'] else 'None'}")
        st.write(f"Predicted fraud trend: {result['trend']}")
        st.write(f"Severity level: {result['severity_level']} (score: {result['severity_score']:.2f})")
        st.write(f"Tone assessment: {result['tone_label']}")
        st.write(f"Raw sentiment score (polarity): {result['sentiment']:.3f}")

        st.markdown("### Brief interpretation")
        explanation_text = build_explanation(result)
        st.write(explanation_text)

    elif analyze_button and not input_text.strip():
        # Quick reminder if someone clicks the button without entering text
        st.warning("Please paste some text to analyze.")
