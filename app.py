import streamlit as st
import pandas as pd


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Data Cleaning & Analysis Tool",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Data Cleaning & Analysis Tool")
st.write("Upload a CSV file, analyze it, clean it, and download the cleaned data.")


# =========================================================
# 2. UPLOAD CSV FILE
# =========================================================

uploaded_file = st.file_uploader(
    "📁 Upload your CSV file",
    type=["csv"]
)


# =========================================================
# 3. IF FILE IS UPLOADED
# =========================================================

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Create cleaned DataFrame only once for this uploaded file
    if (
        "cleaned_df" not in st.session_state
        or st.session_state.get("file_name") != uploaded_file.name
    ):
        st.session_state.cleaned_df = df.copy()
        st.session_state.file_name = uploaded_file.name

    cleaned_df = st.session_state.cleaned_df


    # =====================================================
    # 4. DATASET OVERVIEW
    # =====================================================

    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Total Missing Values", df.isnull().sum().sum())

    st.dataframe(
        df,
        use_container_width=True
    )


    # =====================================================
    # 5. COLUMN ANALYSIS
    # =====================================================

    st.subheader("🔍 Column Analysis")

    selected_column = st.selectbox(
        "Choose a column to analyze",
        df.columns
    )

    # Use original df for analysis
    column_data = df[selected_column]

    st.write("**Selected column:**", selected_column)
    st.write("**Data type:**", df.dtypes[selected_column])

    st.write(
        "**Unique values:**",
        column_data.nunique()
    )

    st.write(
        "**Missing values:**",
        column_data.isnull().sum()
    )


    # =====================================================
    # 6. NUMERICAL / CATEGORICAL ANALYSIS
    # =====================================================

    if pd.api.types.is_numeric_dtype(column_data):

        st.write("### Numerical Statistics")

        st.write(
            "**Average:**",
            column_data.mean()
        )

        st.write(
            "**Minimum:**",
            column_data.min()
        )

        st.write(
            "**Maximum:**",
            column_data.max()
        )

        st.write("### 📊 Distribution")

        st.bar_chart(column_data)

    else:

        st.write("### Categorical Statistics")

        value_counts = column_data.value_counts()

        st.dataframe(
            value_counts,
            use_container_width=True
        )

        st.bar_chart(value_counts)


    # =====================================================
    # 7. MISSING VALUE CLEANING
    # =====================================================

    st.subheader("🧹 Missing Value Cleaning")

    current_column_data = st.session_state.cleaned_df[
        selected_column
    ]

    missing_count = current_column_data.isnull().sum()

    st.write(
        "**Missing values in selected column:**",
        missing_count
    )

    if missing_count == 0:

        st.info(
            "This column has no missing values."
        )

    else:

        cleaning_method = st.selectbox(
            "Choose how to handle missing values",
            [
                "Remove rows",
                "Fill with 0",
                "Fill with mean/mode"
            ],
            key="missing_method"
        )

        if st.button(
            "Apply Missing Value Cleaning"
        ):

            # ---------------------------------------------
            # Remove rows
            # ---------------------------------------------

            if cleaning_method == "Remove rows":

                st.session_state.cleaned_df = (
                    st.session_state.cleaned_df.dropna(
                        subset=[selected_column]
                    )
                )

                st.success(
                    "Rows with missing values removed!"
                )


            # ---------------------------------------------
            # Fill with 0
            # ---------------------------------------------

            elif cleaning_method == "Fill with 0":

                if pd.api.types.is_numeric_dtype(
                    st.session_state.cleaned_df[
                        selected_column
                    ]
                ):

                    st.session_state.cleaned_df[
                        selected_column
                    ] = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].fillna(0)
                    )

                    st.success(
                        "Missing numerical values filled with 0!"
                    )

                else:

                    mode_value = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].mode()[0]
                    )

                    st.session_state.cleaned_df[
                        selected_column
                    ] = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].fillna(mode_value)
                    )

                    st.success(
                        "Missing categorical values filled with mode!"
                    )


            # ---------------------------------------------
            # Fill with mean/mode
            # ---------------------------------------------

            elif cleaning_method == "Fill with mean/mode":

                if pd.api.types.is_numeric_dtype(
                    st.session_state.cleaned_df[
                        selected_column
                    ]
                ):

                    mean_value = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].mean()
                    )

                    st.session_state.cleaned_df[
                        selected_column
                    ] = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].fillna(mean_value)
                    )

                    st.success(
                        "Missing numerical values filled with mean!"
                    )

                else:

                    mode_value = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].mode()[0]
                    )

                    st.session_state.cleaned_df[
                        selected_column
                    ] = (
                        st.session_state.cleaned_df[
                            selected_column
                        ].fillna(mode_value)
                    )

                    st.success(
                        "Missing categorical values filled with mode!"
                    )


    # =====================================================
    # 8. DUPLICATE ROW CLEANING
    # =====================================================

    st.subheader("🔄 Duplicate Rows")

    duplicate_count = (
        st.session_state.cleaned_df
        .duplicated()
        .sum()
    )

    st.write(
        "**Duplicate rows:**",
        duplicate_count
    )

    duplicate_action = st.selectbox(
        "Choose what to do with duplicate rows",
        [
            "Keep duplicates",
            "Remove duplicates"
        ],
        key="duplicate_action"
    )

    if st.button(
        "Apply Duplicate Cleaning"
    ):

        if duplicate_action == "Remove duplicates":

            before = len(
                st.session_state.cleaned_df
            )

            st.session_state.cleaned_df = (
                st.session_state.cleaned_df
                .drop_duplicates()
            )

            after = len(
                st.session_state.cleaned_df
            )

            removed = before - after

            st.success(
                f"{removed} duplicate row(s) removed!"
            )

        else:

            st.info(
                "Duplicate rows were kept."
            )


    # =====================================================
    # 9. CLEANED DATA PREVIEW
    # =====================================================

    st.subheader("✨ Cleaned Dataset")

    st.dataframe(
        st.session_state.cleaned_df,
        use_container_width=True
    )


    # =====================================================
    # 10. BEFORE VS AFTER SUMMARY
    # =====================================================

    st.subheader("📈 Cleaning Summary")

    original_rows = df.shape[0]

    cleaned_rows = (
        st.session_state.cleaned_df.shape[0]
    )

    rows_removed = (
        original_rows - cleaned_rows
    )

    missing_before = (
        df.isnull().sum().sum()
    )

    missing_after = (
        st.session_state.cleaned_df
        .isnull()
        .sum()
        .sum()
    )

    duplicate_before = (
        df.duplicated().sum()
    )

    duplicate_after = (
        st.session_state.cleaned_df
        .duplicated()
        .sum()
    )


    # Display metrics

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Original Rows",
            original_rows
        )

    with col2:
        st.metric(
            "Cleaned Rows",
            cleaned_rows
        )

    with col3:
        st.metric(
            "Rows Removed",
            rows_removed
        )


    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Missing values before:**",
            missing_before
        )

        st.write(
            "**Missing values after:**",
            missing_after
        )

    with col2:

        st.write(
            "**Duplicate rows before:**",
            duplicate_before
        )

        st.write(
            "**Duplicate rows after:**",
            duplicate_after
        )


    # =====================================================
    # 11. DOWNLOAD CLEANED CSV
    # =====================================================

    st.subheader("⬇️ Download Cleaned Dataset")

    csv_data = (
        st.session_state.cleaned_df
        .to_csv(index=False)
    )

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:

    st.info(
        "👆 Upload a CSV file to start."
    )