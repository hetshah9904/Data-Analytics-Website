import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Professional Data Analytics Dashboard")
st.markdown("Analyze, clean, visualize and prepare datasets for Machine Learning.")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Section",
    [
        "🏠 Home",
        "📂 Dataset Preview",
        "📋 Dataset Information",
        "🧹 Data Cleaning",
        "📈 Data Visualization",
        "📊 Statistics",
        "💾 Download Dataset"
    ]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx", "xls"]
)

# -----------------------------
# HOME
# -----------------------------
if uploaded_file is None:

    st.info("👈 Upload a dataset from the sidebar to begin.")

    st.markdown("""
    ### Features

    ✔ Dataset Preview

    ✔ Dataset Information

    ✔ Missing Value Detection

    ✔ Duplicate Detection

    ✔ Summary Statistics

    ✔ Correlation Matrix

    ✔ Histograms

    ✔ Boxplots

    ✔ Download Cleaned Dataset

    ✔ Machine Learning Dataset Preparation
    """)

else:

    # Read dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # -----------------------------
    # DATASET PREVIEW
    # -----------------------------
    if menu == "📂 Dataset Preview":

        st.header("Dataset Preview")

        rows = st.slider("Rows to Display", 5, 100, 10)

        st.dataframe(df.head(rows), use_container_width=True)

        st.write("Shape :", df.shape)

        st.write("Rows :", df.shape[0])

        st.write("Columns :", df.shape[1])

    # -----------------------------
    # DATASET INFORMATION
    # -----------------------------
    elif menu == "📋 Dataset Information":

        st.header("Dataset Information")

        st.subheader("Column Names")

        st.write(df.columns.tolist())

        st.subheader("Data Types")

        st.dataframe(df.dtypes.astype(str))

        st.subheader("Missing Values")

        missing = pd.DataFrame({
            "Missing Values": df.isnull().sum(),
            "Percentage": round(df.isnull().sum()/len(df)*100,2)
        })

        st.dataframe(missing)

        st.subheader("Duplicate Rows")

        st.success(df.duplicated().sum())

        st.subheader("Memory Usage")

        st.write(round(df.memory_usage(deep=True).sum()/1024,2),"KB")

    # -----------------------------
    # DATA CLEANING
    # -----------------------------
    elif menu == "🧹 Data Cleaning":

        st.header("Data Cleaning")

        option = st.selectbox(
            "Choose Cleaning Operation",
            [
                "Remove Missing Values",
                "Fill Missing Values",
                "Remove Duplicates"
            ]
        )

        if option == "Remove Missing Values":

            if st.button("Clean Dataset"):

                cleaned = df.dropna()

                st.success("Missing Values Removed")

                st.dataframe(cleaned)

        elif option == "Fill Missing Values":

            numeric = df.select_dtypes(include='number').columns

            cleaned = df.copy()

            cleaned[numeric] = cleaned[numeric].fillna(cleaned[numeric].mean())

            st.dataframe(cleaned)

        elif option == "Remove Duplicates":

            cleaned = df.drop_duplicates()

            st.success("Duplicates Removed")

            st.dataframe(cleaned)

    # -----------------------------
    # VISUALIZATION
    # -----------------------------
    elif menu == "📈 Data Visualization":

        st.header("Interactive Charts")

        numeric_columns = df.select_dtypes(include='number').columns

        if len(numeric_columns) == 0:

            st.warning("No Numeric Columns Found")

        else:

            chart = st.selectbox(
                "Choose Chart",
                [
                    "Histogram",
                    "Box Plot",
                    "Scatter Plot",
                    "Pie Chart",
                    "Correlation Heatmap"
                ]
            )

            if chart == "Histogram":

                col = st.selectbox("Select Column", numeric_columns)

                fig = px.histogram(df, x=col)

                st.plotly_chart(fig, use_container_width=True)

            elif chart == "Box Plot":

                col = st.selectbox("Select Column", numeric_columns)

                fig = px.box(df, y=col)

                st.plotly_chart(fig, use_container_width=True)

            elif chart == "Scatter Plot":

                x = st.selectbox("X Axis", numeric_columns)

                y = st.selectbox("Y Axis", numeric_columns)

                fig = px.scatter(df, x=x, y=y)

                st.plotly_chart(fig, use_container_width=True)

            elif chart == "Pie Chart":

                col = st.selectbox("Select Column", df.columns)

                pie = df[col].value_counts().reset_index()

                pie.columns=["Category","Count"]

                fig = px.pie(
                    pie,
                    names="Category",
                    values="Count"
                )

                st.plotly_chart(fig, use_container_width=True)

            elif chart == "Correlation Heatmap":

                corr = df.select_dtypes(include='number').corr()

                fig = ff.create_annotated_heatmap(
                    z=corr.values,
                    x=list(corr.columns),
                    y=list(corr.index),
                    annotation_text=round(corr,2).values,
                    colorscale="Viridis"
                )

                st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # SUMMARY STATISTICS
    # -----------------------------
    elif menu == "📊 Statistics":

        st.header("Summary Statistics")

        st.dataframe(df.describe())

        st.subheader("Unique Values")

        column = st.selectbox("Select Column", df.columns)

        st.write(df[column].value_counts())

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    elif menu == "💾 Download Dataset":

        st.header("Download Dataset")

        csv = df.to_csv(index=False).encode()

        st.download_button(
            "Download CSV",
            csv,
            file_name="clean_dataset.csv",
            mime="text/csv"
        )