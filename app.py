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
# LOAD DATA
# ======================================

try:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip().str.upper()

    st.success("✅ Dataset Loaded Successfully")

except Exception as e:
    st.error(f"Error Loading File: {e}")
    st.stop()

# ======================================
# CLEAN DATA
# ======================================

df.fillna(0, inplace=True)

# ======================================
# SIDEBAR FILTERS
# ======================================

st.sidebar.title("🎯 Filters")

# Department Filter
if "DEPARTMENT" in df.columns:

    dept = st.sidebar.selectbox(
        "Department",
        ["All"] + sorted(df["DEPARTMENT"].astype(str).unique())
    )

    if dept != "All":
        df = df[df["DEPARTMENT"] == dept]

# Difficulty Filter
if "DIFFICULTY" in df.columns:

    difficulty = st.sidebar.selectbox(
        "Difficulty",
        ["All"] + sorted(df["DIFFICULTY"].astype(str).unique())
    )

    if difficulty != "All":
        df = df[df["DIFFICULTY"] == difficulty]

# College Tier Filter
if "COLLEGE_TIER" in df.columns:

    tier = st.sidebar.selectbox(
        "College Tier",
        ["All"] + sorted(df["COLLEGE_TIER"].astype(str).unique())
    )

    if tier != "All":
        df = df[df["COLLEGE_TIER"] == tier]

# ======================================
# KPI METRICS
# ======================================

st.subheader("📌 Overall Metrics")

col1, col2, col3, col4 = st.columns(4)

total_students = df["STUDENT_ID"].nunique()

accuracy = round(
    (df["CORRECT"].sum() / len(df)) * 100,
    2
)

avg_time = round(df["TIME_TAKEN"].mean(), 2)

avg_cgpa = round(df["CGPA"].mean(), 2)

col1.metric("Students", total_students)
col2.metric("Accuracy %", accuracy)
col3.metric("Avg Time", avg_time)
col4.metric("Avg CGPA", avg_cgpa)

st.markdown("---")

# ======================================
# DIFFICULTY ANALYSIS
# ======================================

st.subheader("📈 Difficulty Analysis")

difficulty_perf = df.groupby(
    "DIFFICULTY"
)["CORRECT"].mean() * 100

fig1 = plt.figure()

difficulty_perf.plot(
    kind="bar",
    color="orange"
)

plt.ylabel("Accuracy %")

st.pyplot(fig1)

# ======================================
# DEPARTMENT ANALYSIS
# ======================================

st.subheader("🏢 Department Performance")

dept_perf = df.groupby(
    "DEPARTMENT"
)["CORRECT"].mean() * 100

fig2 = plt.figure()

dept_perf.sort_values().plot(
    kind="barh",
    color="green"
)

plt.xlabel("Accuracy %")

st.pyplot(fig2)

# ======================================
# TOPIC ANALYSIS
# ======================================

st.subheader("📚 Topic Analysis")

topic_perf = df.groupby(
    "TOPIC"
)["CORRECT"].mean() * 100

fig3 = plt.figure()

topic_perf.sort_values().plot(
    kind="barh",
    color="purple"
)

plt.xlabel("Accuracy %")

st.pyplot(fig3)

# ======================================
# TIME TAKEN DISTRIBUTION
# ======================================

st.subheader("⏱ Time Taken Distribution")

fig4 = plt.figure()

sns.histplot(
    df["TIME_TAKEN"],
    bins=30,
    kde=True
)

st.pyplot(fig4)

# ======================================
# CONCEPT UNDERSTANDING
# ======================================

st.subheader("🧠 Concept Understanding")

concept_rate = round(
    df["CONCEPT_UNDERSTOOD"].mean() * 100,
    2
)

hint_rate = round(
    df["HINT_USED"].mean() * 100,
    2
)

col5, col6 = st.columns(2)

col5.metric(
    "Concept Understood %",
    concept_rate
)

col6.metric(
    "Hint Usage %",
    hint_rate
)

# ======================================
# TEST CASE ANALYSIS
# ======================================

st.subheader("💻 Coding Performance")

fig5 = plt.figure()

sns.boxplot(
    x="DIFFICULTY",
    y="TEST_CASES_PASSED",
    data=df
)

st.pyplot(fig5)

# ======================================
# HEATMAP
# ======================================

st.subheader("🔥 Heatmap")

pivot = df.pivot_table(
    values="CORRECT",
    index="DEPARTMENT",
    columns="DIFFICULTY",
    aggfunc="mean"
)

fig6 = plt.figure(figsize=(10, 5))

sns.heatmap(
    pivot,
    annot=True,
    cmap="coolwarm"
)

st.pyplot(fig6)

# ======================================
# TOP STUDENTS
# ======================================

st.subheader("🏆 Top Students")

student_perf = df.groupby(
    "STUDENT_ID"
).agg({
    "CORRECT": "sum",
    "TIME_TAKEN": "mean",
    "CGPA": "mean"
}).reset_index()

top_students = student_perf.sort_values(
    "CORRECT",
    ascending=False
).head(10)

st.dataframe(top_students)

# ======================================
# FULL DATASET
# ======================================

st.subheader("📋 Full Dataset")

st.dataframe(df)

# ======================================
# DOWNLOAD REPORT
# ======================================

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Processed Report",
    csv,
    "learning_analytics.csv",
    "text/csv"
)
