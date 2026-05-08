import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if not st.session_state.get("logged_in"):
    st.error("Please login first")
    st.stop()

if "df" not in st.session_state:
    st.error("Upload data first")
    st.stop()

df = st.session_state["df"]
answer_key = st.session_state["answer_key"]

st.title("📊 MCQ Analytics Dashboard")

# =========================
# CLEAN DATA
# =========================

df.fillna("Not Answered", inplace=True)

# =========================
# SCORE CALCULATION
# =========================

def calculate_score(row):

    score = 0

    for q in answer_key:

        if row[q] == answer_key[q]:
            score += 1

    return score

df["SCORE"] = df.apply(calculate_score, axis=1)

# =========================
# RESULT
# =========================

df["RESULT"] = df["SCORE"].apply(
    lambda x: "Pass" if x >= len(answer_key)/2 else "Fail"
)

# =========================
# METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", len(df))
col2.metric("Average", round(df["SCORE"].mean(), 2))
col3.metric("Highest", df["SCORE"].max())
col4.metric("Lowest", df["SCORE"].min())

st.markdown("---")

# =========================
# SCORE DISTRIBUTION
# =========================

st.subheader("📈 Score Distribution")

fig1 = plt.figure()

sns.histplot(df["SCORE"], bins=5, kde=True)

st.pyplot(fig1)

# =========================
# PASS FAIL
# =========================

st.subheader("✅ Pass vs Fail")

fig2 = plt.figure()

sns.countplot(x="RESULT", data=df)

st.pyplot(fig2)

# =========================
# QUESTION ANALYSIS
# =========================

st.subheader("❓ Question Analysis")

question_accuracy = {}

for q in answer_key:

    correct = (df[q] == answer_key[q]).sum()

    question_accuracy[q] = correct / len(df)

question_df = pd.DataFrame.from_dict(
    question_accuracy,
    orient="index",
    columns=["Accuracy"]
)

st.dataframe(question_df)

fig3 = plt.figure()

question_df["Accuracy"].plot(kind="bar")

st.pyplot(fig3)

# =========================
# TOP STUDENTS
# =========================

st.subheader("🏆 Top Students")

top_students = df.sort_values(
    "SCORE",
    ascending=False
).head(5)

st.dataframe(top_students)

# =========================
# DOWNLOAD REPORT
# =========================

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Results",
    csv,
    "quiz_results.csv",
    "text/csv"
)
