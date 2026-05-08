# ======================================
# LOAD DATA
# ======================================

try:

    # CSV
    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    # XLSX
    elif uploaded_file.name.endswith(".xlsx"):

        df = pd.read_excel(
            uploaded_file,
            engine="openpyxl"
        )

    # XLS
    elif uploaded_file.name.endswith(".xls"):

        df = pd.read_excel(
            uploaded_file,
            engine="xlrd"
        )

    else:

        st.error("Unsupported file format")
        st.stop()

    df.columns = df.columns.str.strip().str.upper()

    st.success("✅ Dataset Loaded Successfully")

except Exception as e:

    st.error(f"❌ Error Loading File: {e}")
    st.stop()
