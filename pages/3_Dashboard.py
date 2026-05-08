import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================
# AUTH CHECK
# ======================================

if not st.session_state.get("logged_in"):
    st.error("Please login first")
    st.stop()

if "df" not in st.session_state:
    st.error("Upload data first")
    st.stop()

df = st.session_state["df"]
answer_key = st.session_state["answer_key"]

st.title("📊 MCQ Analytics Dashboard")

# ======================================
# CLEAN DATA
# ======================================

df.fillna(0, inplace=True)

# Ensure numeric safety
for col in ["CORRECT", "TIME_TAKEN", "CGPA"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ======================================
# SCORE CALCULATION
# ======================================

def calculate_score(row):
    score = 0
    for q in answer_key:
        if q in row and row[q] == answer_key[q]:
            score += 1
    return score

df["SCORE"] = df.apply(calculate_score, axis=1)

df["RESULT"] = df["SCORE"].apply(
    lambda x: "Pass" if x >= len(answer_key) / 2 else "Fail"
)

# ======================================
# METRICS
# ======================================

st.subheader("📌 Overall Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", len(df))
col2.metric("Average Score", round(df["SCORE"].mean(), 2))
col3.metric("Highest Score", df["SCORE"].max())
col4.metric("Lowest Score", df["SCORE"].min())

st.markdown("---")

# ======================================
# SCORE DISTRIBUTION
# ======================================

st.subheader("📈 Score Distribution")

fig1 = plt.figure()
sns.histplot(df["SCORE"], bins=5, kde=True)
st.pyplot(fig1)

# ======================================
# PASS / FAIL
# ======================================

st.subheader("✅ Pass vs Fail")

fig2 = plt.figure()
sns.countplot(x="RESULT", data=df)
st.pyplot(fig2)

# ======================================
# DEPARTMENT ANALYSIS
# ======================================

st.subheader("🏢 Department Performance")

if "DEPARTMENT" in df.columns:
    dept_perf = df.groupby("DEPARTMENT")["SCORE"].mean()

    fig3 = plt.figure()
    dept_perf.plot(kind="bar")
    plt.ylabel("Average Score")
    st.pyplot(fig3)

# ======================================
# COLLEGE ANALYSIS
# ======================================

if "COLLEGE" in df.columns:
    st.subheader("🏫 College Performance")

    college_perf = df.groupby("COLLEGE")["SCORE"].mean()

    fig4 = plt.figure()
    college_perf.plot(kind="bar")
    plt.ylabel("Average Score")
    st.pyplot(fig4)

# ======================================
# QUESTION ANALYSIS (FIXED)
# ======================================

st.subheader("❓ Question Analysis")

question_accuracy = {}

for q in answer_key:
    if q in df.columns:
        correct = (df[q] == answer_key[q]).sum()
        question_accuracy[q] = correct / len(df)
    else:
        question_accuracy[q] = 0

question_df = pd.DataFrame.from_dict(
    question_accuracy,
    orient="index",
    columns=["Accuracy"]
)

# 🔥 FIX: Convert to numeric (IMPORTANT)
question_df["Accuracy"] = pd.to_numeric(
    question_df["Accuracy"],
    errors="coerce"
).fillna(0)

# Plot
fig5 = plt.figure()
question_df["Accuracy"].plot(kind="bar")
plt.ylabel("Accuracy")
st.pyplot(fig5)

# ======================================
# INSIGHTS
# ======================================

st.subheader("🧠 Insights")

best_q = question_df["Accuracy"].idxmax()
worst_q = question_df["Accuracy"].idxmin()

st.write(f"✔ Easiest Question: **{best_q}**")
st.write(f"⚠ Most Difficult Question: **{worst_q}**")

# ======================================
# TOP STUDENTS
# ======================================

st.subheader("🏆 Top Students")

top_students = df.sort_values("SCORE", ascending=False).head(10)

st.dataframe(top_students)

# ======================================
# FULL DATA
# ======================================

st.subheader("📋 Full Dataset")

st.dataframe(df)

# ======================================
# DOWNLOAD REPORT
# ======================================

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Report",
    csv,
    "quiz_results.csv",
    "text/csv"
)
