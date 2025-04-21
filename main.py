import streamlit as st
st.set_page_config(
        page_title="AutoEDA",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import Counter
import plotly.express as px
import data_analysis_functions as function
import data_preprocessing_function as preprocessing_function
import home_page
import base64
from auth_ui import check_auth, show_logout_button
from report_service import report_service

def main():
    # Check authentication
    if not check_auth():
        return

    # Show logout button in sidebar
    show_logout_button()

    # Add custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Streamlit Components - Use Default Font */
        .stApp h1, 
        .stApp h2, 
        .stApp h3, 
        .stApp h4, 
        .stApp h5, 
        .stApp h6,
        .stApp p,
        .stApp div,
        .stApp span,
        .stApp button,
        .stApp input,
        .stApp select,
        .stApp textarea,
        .stApp label,
        .stApp .stButton > button,
        .stApp .stSelectbox > div > div,
        .stApp .stTabs [data-baseweb="tab"],
        .stApp .stFileUploader > div,
        .stApp .sidebar .sidebar-content {
            font-family: inherit !important;
        }
        
        /* App Background */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #eaeaea;
        }

        section[data-testid="stSidebar"] .stMarkdown {
            color: white;
        }

        /* File uploader in sidebar should match sidebar color */
        section[data-testid="stSidebar"] .stFileUploader > div {
            background-color: #ffffff;
        }

        .stApp {
            background-color: #ffffff;
        }

        div[data-testid="stToolbar"] {
            background-color: #ffffff;
        }

        div[data-testid="stDecoration"] {
            background-color: #ffffff;
        }

        div[data-testid="stStatusWidget"] {
            background-color: #ffffff;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #3489fb;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #E0E0E0;
            transform: translateY(-2px);
        }
        
        /* Select Boxes */
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #1a237e;
            font-weight: 600;
        }
        
        /* Text */
        p {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #424242;
        }
        
        /* Dataframes */
        .stDataFrame {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background-color: transparent;

        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
           
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
        
            color: #2196F3;
        }
        
        /* File Uploader */
        .stFileUploader > div {
            background-color: #2196F3 !important;
            border-radius: 8px;
            padding: 2rem;
            color: white !important;
        }

        /* Style the drag and drop text */
        .stFileUploader > div > div {
            color: white !important;
        }

        /* Style the "Drag and drop file here" text */
        .stFileUploader > div [data-testid="stFileUploadDropzone"] {
            color: white !important;
        }

        /* Style the "Browse files" button in uploader */
        .stFileUploader > div button {
            background-color: blue !important;
            color: #white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }

        .stFileUploader > div button:hover {
            background-color: rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }

        /* Style the file size limit text */
        .stFileUploader > div small {
            color: rgba(255, 255, 255, 0.8) !important;
        }

        /* Style the uploaded file name */
        .stFileUploader > div [data-testid="stMarkdownContainer"] {
            color: white !important;
        }

        /* Style the upload progress bar */
        .stFileUploader > div .st-emotion-cache-1yycg8b {
            background-color: rgba(255, 255, 255, 0.2) !important;
        }

        .stFileUploader > div .st-emotion-cache-1yycg8b > div {
            background-color: white !important;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #2196F3;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #1976D2;
        }

        /* Additional Light Theme Overrides */
        .main {
            background-color: #ffffff;
        }

        .stMarkdown {
            color: #white;
        }

        div[class*="stTextInput"] label {
            color: #424242;
        }

        div[class*="stTextInput"] input {
            background-color: #ffffff;
            color: #424242;
        }

        .sidebar .sidebar-content {
            background-color: #ffffff;
        }

        div[data-baseweb="select"] {
            background-color: #ffffff;
        }

        /* Add this to your existing CSS */
        a button {
            background-color: #2196F3 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            cursor: pointer !important;
        }
        
        a button:hover {
            background-color: #1976D2 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            transform: translateY(-2px) !important;
        }

        .report-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create a Streamlit sidebar
    st.sidebar.title(f"Welcome, {st.session_state.username}!")

    # Create the introduction section
    st.title("Welcome to AutoEDA")
    st.write('<div class="tagline">Unleash the Power of Data with AutoEDA!</div>', unsafe_allow_html=True)
    st.write('<div style="margin: 10px;"></div>', unsafe_allow_html=True)

    # Replace option_menu with tabs
    tab_icons = {"Home": "🏠", "Data Exploration": "📊", "Data Preprocessing": "🔧"}
    selected = st.tabs([f"{tab_icons[tab]} {tab}" for tab in ["Home", "Data Exploration", "Data Preprocessing"]])

    # Create a button in the sidebar to upload CSV
    uploaded_file = st.sidebar.file_uploader("Upload Your CSV File Here", type=["csv","xls"])
    use_example_data = st.sidebar.checkbox("Use Example Titanic Dataset", value=False)

    # Create columns in the sidebar for LinkedIn and GitHub icons
    col1, col2 = st.sidebar.columns(2)

    if uploaded_file:
        df = function.load_data(uploaded_file)
        if 'new_df' not in st.session_state:
            st.session_state.new_df = df.copy()
    elif use_example_data:
        df = function.load_data(file="example_dataset/titanic.csv")
        if 'new_df' not in st.session_state:
            st.session_state.new_df = df

    # Display content based on selected tab
    with selected[0]:  # Home tab
        home_page.show_home_page()

    if uploaded_file is not None or use_example_data:
        with selected[1]:  # Data Exploration tab
            tab1, tab2 = st.tabs(['📊 Dataset Overview', "🔎 Data Exploration and Visualization"])
            num_columns, cat_columns = function.categorical_numerical(df)
            
            with tab1:
                st.subheader("1. Dataset Preview")
                st.markdown("This section provides an overview of your dataset. You can select the number of rows to display and view the dataset's structure.")
                function.display_dataset_overview(df,cat_columns,num_columns)

                st.subheader("3. Missing Values")
                function.display_missing_values(df)
                
                st.subheader("4. Data Statistics and Visualization")
                function.display_statistics_visualization(df,cat_columns,num_columns)

                st.subheader("5. Data Types")
                function.display_data_types(df)

                st.subheader("Search for a specific column or datatype")
                function.search_column(df)

            with tab2: 
                function.display_individual_feature_distribution(df,num_columns)

                st.subheader("Scatter Plot")
                function.display_scatter_plot_of_two_numeric_features(df,num_columns)

                if len(cat_columns)!=0:
                    st.subheader("Categorical Variable Analysis")
                    function.categorical_variable_analysis(df,cat_columns)
                else:
                    st.info("The dataset does not have any categorical columns")

                st.subheader("Feature Exploration of Numerical Variables")
                if len(num_columns)!=0:
                    function.feature_exploration_numerical_variables(df,num_columns)
                else:
                    st.warning("The dataset does not contain any numerical variables")

                # Create a bar graph to get relationship between categorical variable and numerical variable
                st.subheader("Categorical and Numerical Variable Analysis")
                if len(num_columns)!=0 and len(cat_columns)!=0:
                    function.categorical_numerical_variable_analysis(df,cat_columns,num_columns)
                else:
                    st.warning("The dataset does not have any numerical variables. Hence Cannot Perform Categorical and Numerical Variable Analysis")
        
        with selected[2]:  # Data Preprocessing tab
            if 'new_df' in st.session_state:
                revert = st.button("Revert to Original Dataset",key="revert_button")
                if revert:
                    st.session_state.new_df = df.copy()

                # REMOVING UNWANTED COLUMNS
                st.subheader("Remove Unwanted Columns")
                columns_to_remove = st.multiselect(label='Select Columns to Remove',options=st.session_state.new_df.columns)

                if st.button("Remove Selected Columns"):
                    if columns_to_remove:
                        st.session_state.new_df = preprocessing_function.remove_selected_columns(st.session_state.new_df,columns_to_remove)
                        st.success("Selected Columns Removed Sucessfully")
                
                st.dataframe(st.session_state.new_df)
               
               # Handle missing values in the dataset
                st.subheader("Handle Missing Data")
                missing_count = st.session_state.new_df.isnull().sum()

                if missing_count.any():
                    selected_missing_option = st.selectbox(
                        "Select how to handle missing data:",
                        ["Remove Rows in Selected Columns", "Fill Missing Data in Selected Columns (Numerical Only)"]
                    )

                    if selected_missing_option == "Remove Rows in Selected Columns":
                        columns_to_remove_missing = st.multiselect("Select columns to remove rows with missing data", options=st.session_state.new_df.columns)
                        if st.button("Remove Rows with Missing Data"):
                            st.session_state.new_df = preprocessing_function.remove_rows_with_missing_data(st.session_state.new_df, columns_to_remove_missing)
                            st.success("Rows with missing data removed successfully.")

                    elif selected_missing_option == "Fill Missing Data in Selected Columns (Numerical Only)":
                        numerical_columns_to_fill = st.multiselect("Select numerical columns to fill missing data", options=st.session_state.new_df.select_dtypes(include=['number']).columns)
                        fill_method = st.selectbox("Select fill method:", ["mean", "median", "mode"])
                        if st.button("Fill Missing Data"):
                            if numerical_columns_to_fill:
                                st.session_state.new_df = preprocessing_function.fill_missing_data(st.session_state.new_df, numerical_columns_to_fill, fill_method)
                                st.success(f"Missing data in numerical columns filled with {fill_method} successfully.")
                            else:
                                st.warning("Please select a column to fill in the missing data")

                    function.display_missing_values(st.session_state.new_df)
                else:
                    st.info("The dataset does not contain any missing values")

                encoding_tooltip = '''**One-Hot encoding** converts categories into binary values (0 or 1). It's like creating checkboxes for each category. This makes it possible for computers to work with categorical data.
                **Label encoding** assigns unique numbers to categories. It's like giving each category a name (e.g., Red, Green, Blue becomes 1, 2, 3). This helps computers understand and work with categories.
                '''
                st.markdown("""
                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
                        <h3 style="color: #1a237e; margin-bottom: 1rem;">🔄 Encode Categorical Data</h3>
                    </div>
                """, unsafe_allow_html=True)

                new_df_categorical_columns = st.session_state.new_df.select_dtypes(include=['object']).columns

                if not new_df_categorical_columns.empty:
                    select_categorical_columns = st.multiselect("Select Columns to Encode",new_df_categorical_columns)

                    #choose the encoding method
                    encoding_method = st.selectbox("Select Encoding Method:",['One Hot Encoding','Label Encoding'],help=encoding_tooltip)
            
                    if st.button("Apply Encoding", type="primary"):
                        if encoding_method=="One Hot Encoding":
                            st.session_state.new_df = preprocessing_function.one_hot_encode(st.session_state.new_df,select_categorical_columns)
                            st.success("✨ One-Hot Encoding Applied Successfully")

                        if encoding_method=="Label Encoding":
                            st.session_state.new_df = preprocessing_function.label_encode(st.session_state.new_df,select_categorical_columns)
                            st.success("✨ Label Encoding Applied Successfully")

                    st.dataframe(st.session_state.new_df, use_container_width=True)
                else:
                    st.info("ℹ️ The dataset does not contain any categorical columns")

                feature_scaling_tooltip='''**Standardization** scales your data to have a mean of 0 and a standard deviation of 1. It helps in comparing variables with different units. Think of it like making all values fit on the same measurement scale.
                **Min-Max scaling** transforms your data to fall between 0 and 1. It's like squeezing data into a specific range. This makes it easier to compare data points that vary widely.'''

                st.markdown("""
                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
                        <h3 style="color: #1a237e; margin-bottom: 1rem;">📏 Feature Scaling</h3>
                    </div>
                """, unsafe_allow_html=True)

                new_df_numerical_columns = st.session_state.new_df.select_dtypes(include=['number']).columns
                selected_columns = st.multiselect("Select Numerical Columns to Scale", new_df_numerical_columns)

                scaling_method = st.selectbox("Select Scaling Method:", ['Standardization', 'Min-Max Scaling'],help=feature_scaling_tooltip)

                if st.button("Apply Scaling", type="primary"):
                    if selected_columns:
                        if scaling_method == "Standardization":
                            st.session_state.new_df = preprocessing_function.standard_scale(st.session_state.new_df, selected_columns)
                            st.success("✨ Standardization Applied Successfully")
                        elif scaling_method == "Min-Max Scaling":
                            st.session_state.new_df = preprocessing_function.min_max_scale(st.session_state.new_df, selected_columns)
                            st.success("✨ Min-Max Scaling Applied Successfully")
                    else:
                        st.warning("⚠️ Please select numerical columns to scale")

                st.dataframe(st.session_state.new_df, use_container_width=True)

                st.markdown("""
                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
                        <h3 style="color: #1a237e; margin-bottom: 1rem;">🎯 Identify and Handle Outliers</h3>
                    </div>
                """, unsafe_allow_html=True)

                # Select numeric column for handling outliers
                selected_numeric_column = st.selectbox("Select Numeric Column for Outlier Analysis:", new_df_numerical_columns)

                # Display outliers in a box plot
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.set_style("whitegrid")
                sns.boxplot(data=st.session_state.new_df, x=selected_numeric_column, ax=ax)
                ax.set_title(f'Box Plot of {selected_numeric_column}', pad=20)
                st.pyplot(fig)

                outliers = preprocessing_function.detect_outliers_zscore(st.session_state.new_df, selected_numeric_column)
                if outliers:
                    st.warning("⚠️ Detected Outliers:")
                    st.write(outliers)
                else:
                    st.info("ℹ️ No outliers detected using IQR")

                # Choose handling method
                outlier_handling_method = st.selectbox("Select Outlier Handling Method:", ["Remove Outliers", "Transform Outliers"])

                # Perform outlier handling based on the method chosen
                if st.button("Handle Outliers", type="primary"):
                    if outlier_handling_method == "Remove Outliers":
                        st.session_state.new_df = preprocessing_function.remove_outliers(st.session_state.new_df, selected_numeric_column,outliers)
                        st.success("✨ Outliers removed successfully")

                    elif outlier_handling_method == "Transform Outliers":
                        st.session_state.new_df = preprocessing_function.transform_outliers(st.session_state.new_df, selected_numeric_column,outliers)
                        st.success("✨ Outliers transformed successfully")

                # Show the updated dataset
                st.dataframe(st.session_state.new_df, use_container_width=True)
                
                if st.session_state.new_df is not None:
                    st.markdown("""
                        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
                            <h3 style="color: #1a237e; margin-bottom: 1rem;">💾 Save Your Work</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    # Convert the DataFrame to CSV
                    csv = st.session_state.new_df.to_csv(index=False)
                    # Encode as base64
                    b64 = base64.b64encode(csv.encode()).decode()
                    # Create a download link with a styled button
                    st.markdown(f'''
                        <a href="data:file/csv;base64,{b64}" download="preprocessed_data.csv">
                            <button style="
                                background-color: #1a237e;
                                color: white;
                                padding: 0.75rem 1.5rem;
                                border: none;
                                border-radius: 4px;
                                cursor: pointer;
                                font-size: 1rem;
                                transition: background-color 0.3s;
                                display: inline-flex;
                                align-items: center;
                                gap: 0.5rem;
                            ">
                                <span>📥</span> Download Preprocessed Data
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No preprocessed data available to download")

                # Prepare analysis results for report generation
                def get_data_summary(df):
                    if df is None:
                        return None
                    
                    # Convert Int64 to standard int64 to avoid Arrow conversion issues
                    df = df.copy()
                    for col in df.select_dtypes(include=['Int64']).columns:
                        df[col] = df[col].astype('float64')  # Convert to float64 to handle NaN values
                    
                    num_cols = df.select_dtypes(include=['number']).columns
                    cat_cols = df.select_dtypes(include=['object']).columns
                    
                    summary = {
                        'total_rows': int(len(df)),  # Ensure integer type
                        'total_columns': int(len(df.columns)),  # Ensure integer type
                        'numerical_columns': list(num_cols),  # Convert to list for JSON serialization
                        'categorical_columns': list(cat_cols),  # Convert to list for JSON serialization
                        'column_types': {str(k): str(v) for k, v in df.dtypes.items()},  # Convert dtypes to strings
                        'missing_values': {str(k): int(v) for k, v in df.isnull().sum().items()}  # Convert to int
                    }
                    
                    # Add numerical statistics
                    if len(num_cols) > 0:
                        stats = df[num_cols].describe()
                        summary['numerical_stats'] = {
                            str(col): {
                                'mean': float(stats.loc['mean', col]),
                                'std': float(stats.loc['std', col]),
                                'min': float(stats.loc['min', col]),
                                'max': float(stats.loc['max', col])
                            }
                            for col in num_cols
                        }
                    
                    # Add categorical value counts (top 5 for each)
                    if len(cat_cols) > 0:
                        summary['categorical_stats'] = {
                            str(col): {str(k): int(v) for k, v in df[col].value_counts().head(5).items()}
                            for col in cat_cols
                        }
                    
                    return summary

                analysis_data = {
                    'original_data': get_data_summary(df),
                    'processed_data': get_data_summary(st.session_state.new_df) if 'new_df' in st.session_state else None
                }
                
                add_report_generation_button(analysis_data)
    else:
        with selected[1]:  # Data Exploration tab
            st.markdown("""
                <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
                    <h2 style="color: #1a237e; margin-bottom: 1rem;">📊 Ready to Explore Your Data?</h2>
                    <p style="color: #424242; font-size: 1.1rem; line-height: 1.6; max-width: 600px; margin: 0 auto;">
                        To begin exploring your data, please use the sidebar to upload your dataset or select the example Titanic dataset.
                        Once your data is loaded, you'll have access to powerful exploration tools and visualizations.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with selected[2]:  # Data Preprocessing tab
            st.markdown("""
                <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
                    <h2 style="color: #1a237e; margin-bottom: 1rem;">🛠️ Prepare Your Data</h2>
                    <p style="color: #424242; font-size: 1.1rem; line-height: 1.6; max-width: 600px; margin: 0 auto;">
                        To start preprocessing your data, please upload your dataset using the sidebar or select the example Titanic dataset.
                        Once loaded, you'll be able to clean, transform, and prepare your data for analysis.
                    </p>
                </div>
            """, unsafe_allow_html=True)

def add_report_generation_button(analysis_results):
    """Add a button to generate and email a PDF report"""
    st.markdown("""
        <div style='
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 1px solid #e9ecef;
        '>
            <h3 style='color: #1a237e; margin-bottom: 10px;'>📊 Generate Analysis Report</h3>
            <p style='color: #6c757d; margin-bottom: 15px;'>
                Get a complete PDF report of your analysis delivered to your email.
                The report will include all visualizations and insights from your current session.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Generate and Email Report", key="generate_report"):
        if 'user_email' in st.session_state:
            with st.spinner("📸 Capturing analysis... This may take a few seconds."):
                # Add a small delay to ensure UI is updated
                st.empty().markdown("Preparing report...")
                st.session_state['generating_report'] = True
                st.rerun()  # This will trigger a rerun after UI is fully rendered
        else:
            st.error("Please sign in to generate reports.")
            
    # Handle report generation after rerun
    if st.session_state.get('generating_report', False):
        success, message = report_service.generate_and_email_report(
            st.session_state.user_email,
            analysis_results
        )
        
        if success:
            st.success("✅ " + message)
        else:
            st.error("❌ " + message)
        
        # Reset the flag
        st.session_state['generating_report'] = False

if __name__ == "__main__":
    main()