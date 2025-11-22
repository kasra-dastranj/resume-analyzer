# streamlit_app.py (Updated for Optimized Parsers)
import streamlit as st
import os
import shutil
import cv_parser 
import optimized_report_generator as reporter # CHANGED: Importing the new optimized reporter

# --- Main function to run the full process ---
def run_full_process(api_key, uploaded_files):
    # --- Initial setup ---
    # Clean up folders for a fresh run
    for folder in ['resumes', 'output', 'structured_reports']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    # --- Initialize Groq clients with the API key ---
    try:
        cv_parser.client = cv_parser.Groq(api_key=api_key)
        reporter.client = reporter.Groq(api_key=api_key)
        st.info("✅ API clients initialized successfully.")
    except Exception as e:
        st.error(f"❌ Error initializing API clients: {e}")
        return

    # --- Save uploaded files to the 'resumes' folder ---
    for uploaded_file in uploaded_files:
        with open(os.path.join("resumes", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # --- Step 1: Parse Resumes (Optimized) ---
    with st.spinner("Step 1: Analyzing resumes with the optimized parser..."):
        try:
            files_to_process = os.listdir('resumes')
            failed_files = []
            
            progress_bar_parser = st.progress(0, text="Starting analysis...")
            status_text_parser = st.empty()
            
            for i, filename in enumerate(files_to_process):
                status_text_parser.text(f"Analyzing file: {filename} ({i+1}/{len(files_to_process)})")
                
                # REMOVED: No longer needs feedback_examples
                success, is_size_error = cv_parser.process_file(filename, chunk_size=cv_parser.CHUNK_SIZE_NORMAL)
                if not success and is_size_error:
                    st.warning(f"File {filename} is large. Retrying with a smaller chunk size...")
                    status_text_parser.text(f"Retrying {filename} with emergency chunk size...")
                    success, _ = cv_parser.process_file(filename, chunk_size=cv_parser.CHUNK_SIZE_EMERGENCY)

                if not success:
                    failed_files.append(filename)
                
                progress_bar_parser.progress((i + 1) / len(files_to_process), text=f"Analysis of {filename} complete.")
            
            status_text_parser.text("Resume analysis finished.")
            st.success("✅ Resume analysis completed successfully.")
            if failed_files:
                st.warning(f"⚠️ Could not fully process the following files: {', '.join(failed_files)}")
        except Exception as e:
            st.error(f"❌ A critical error occurred during the analysis phase: {e}")
            return

    # --- Step 2: Generate Reports (Optimized) ---
    with st.spinner("Step 2: Generating simplified English reports..."):
        try:
            # CHANGED: Using the new SimplifiedReportGenerator class
            generator = reporter.SimplifiedReportGenerator()
            generator.process_all_json_files(target_language="english")
            st.success("✅ Reports generated successfully!")
        except Exception as e:
            st.error(f"❌ A critical error occurred during the report generation phase: {e}")
            return

    # --- Display Results ---
    st.header("📄 Final Assessment Reports")
    report_files = [f for f in os.listdir('structured_reports') if f.endswith('.txt')]
    if report_files:
        for report_file in report_files:
            with st.expander(f"View Report for: {report_file}"):
                with open(os.path.join('structured_reports', report_file), 'r', encoding='utf-8') as f:
                    st.text(f.read())
    else:
        st.warning("No reports were generated.")

# --- Streamlit UI Configuration ---
st.set_page_config(layout="wide", page_title="Optimized Resume Analyzer")
st.title("🚀 Optimized Resume Analyzer")
st.write("This tool uses an optimized AI process to analyze resumes and generate assessment reports.")

# --- API Key Input ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    st.success("API Key loaded successfully from Hugging Face Secrets.")
except (FileNotFoundError, KeyError):
    st.warning("API Key not found in secrets. Please provide it manually below.")
    GROQ_API_KEY = st.text_input("Enter your Groq API Key here:", type="password")


# --- File Uploader ---
uploaded_files = st.file_uploader(
    "Drag and drop resume files (PDF, DOCX) here",
    accept_multiple_files=True,
    type=['pdf', 'docx']
)

# --- Start Button ---
if st.button("Start Analysis & Report Generation"):
    if not uploaded_files:
        st.error("Please upload at least one resume file.")
    elif not GROQ_API_KEY:
        st.error("Please provide the Groq API Key.")
    else:
        run_full_process(GROQ_API_KEY, uploaded_files)