import streamlit as st
import pandas as pd

# Authentication check
if not st.session_state.get("logged_in"):
    st.error("Please login first")
    st.stop()

st.title("📂 Upload Quiz Data")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip().str.upper()

    st.success("✅ File Uploaded")

    st.subheader("Preview")
    st.dataframe(df.head())

    # =========================
    # DYNAMIC ANSWER KEY INPUT
    # =========================

    st.subheader("📝 Enter Answer Key")

    question_cols = [
        col for col in df.columns
        if col.startswith("Q")
    ]

    answer_key = {}

    cols = st.columns(5)

    for i, q in enumerate(question_cols):

        answer = cols[i % 5].selectbox(
            f"{q}",
            ["A", "B", "C", "D"],
            key=q
        )

        answer_key[q] = answer

    # Save to session
    st.session_state["df"] = df
    st.session_state["answer_key"] = answer_key

    if st.button("Generate Dashboard"):
        st.switch_page("pages/3_Dashboard.py")
