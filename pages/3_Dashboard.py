import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI Learning Analytics",
    layout="wide"
)

st.title("📊 AI Learning Analytics Dashboard")

# ======================================
# LOGIN SYSTEM
# ======================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("✅ Login Successful")
            st.rerun()

        else:
            st.error("❌ Invalid Credentials")

    st.stop()

# ======================================
# FILE UPLOAD
# ======================================

st.sidebar.title("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.warning("Please upload dataset")
    st.stop()

# ======================================
# LOAD DATA (SAFE)
# ======================================

try:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip().str.upper()

    st.success("✅ Dataset Loaded Successfully")

except Exception as e:
    st.error(f"❌ Error Loading File: {e}")
    st.stop()

# ======================================
# CLEAN DATA
# ======================================

df.fillna(0, inplace=True)

# Convert numeric-safe columns
for col in ["CORRECT", "TIME_TAKEN"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.title("🎯 Filters")

if "DEPARTMENT" in df.columns:

    dept = st.sidebar.selectbox(
        "Department",
        ["All"] + sorted(df["DEPARTMENT"].astype(str).unique())
    )

    if dept != "All":
        df = df[df["DEPARTMENT"] == dept]

if "DIFFICULTY" in df.columns:

    difficulty = st.sidebar.selectbox(
        "Difficulty",
        ["All"] + sorted(df["DIFFICULTY"].astype(str).unique())
    )

    if difficulty != "All":
        df = df[df["DIFFICULTY"] == difficulty]

if "COLLEGE_TIER" in df.columns:

    tier = st.sidebar.selectbox(
        "College Tier",
        ["All"] + sorted(df["COLLEGE_TIER"].astype(str).unique())
    )

    if tier != "All":
        df = df[df["COLLEGE_TIER"] == tier]

# ======================================
# SCORE CALCULATION (SAFE)
# ======================================

answer_key = st.session_state.get("answer_key", {})

if not answer_key:
    answer_key = {
        "Q1": "A",
        "Q2": "C",
        "Q3": "C",
        "Q4": "B",
        "Q5": "D"
    }

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
# KPI METRICS
# ======================================

st.subheader("📌 Overall Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", len(df))
col2.metric("Average Score", round(df["SCORE"].mean(), 2))
col3.metric("Highest Score", df["SCORE"].max())
col4.metric("Lowest Score", df["SCORE"].min())

# ======================================
# SAFE CGPA FIX (MAIN ERROR FIX)
# ======================================

if "CGPA" in df.columns:

    df["CGPA"] = pd.to_numeric(df["CGPA"], errors="coerce")

    avg_cgpa = round(df["CGPA"].mean(), 2)

else:

    avg_cgpa = 0

col4.metric("Avg CGPA", avg_cgpa)

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

if "DEPARTMENT" in df.columns:

    st.subheader("🏢 Department Performance")

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
# QUESTION ANALYSIS (SAFE)
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

question_df["Accuracy"] = pd.to_numeric(
    question_df["Accuracy"],
    errors="coerce"
).fillna(0)

fig5 = plt.figure()
plt.bar(question_df.index, question_df["Accuracy"])
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
