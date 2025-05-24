"""
AI Financial Reviewer - Main Application

This script serves as the entry point for the AI Financial Reviewer application.
"""

import os
import sys
import streamlit as st
import requests
import webbrowser
from dotenv import load_dotenv
import pandas as pd
import time
import random

# Load environment variables
load_dotenv()

BACKEND_URL = "http://localhost:8000"  # Adjust if backend runs elsewhere

st.set_page_config(page_title="AI Financial Reviewer", page_icon="💸")
st.title("AI Financial Reviewer")

# Session state for auth
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# Session state for upload queue
if "upload_queue" not in st.session_state:
    st.session_state.upload_queue = []

# Session state for progress
if "upload_progress" not in st.session_state:
    st.session_state.upload_progress = {}

# Session state for run log modal
if "show_run_log" not in st.session_state:
    st.session_state.show_run_log = False
if "run_log" not in st.session_state:
    st.session_state.run_log = []

# Session state for preview modal
if "preview_file_idx" not in st.session_state:
    st.session_state.preview_file_idx = None
if "preview_error" not in st.session_state:
    st.session_state.preview_error = False

# Hardcoded sheet names for demo
SHEET_NAMES = ["Budget", "Portfolio", "Tagging"]

# Helper: fetch OAuth URL from backend
def get_oauth_url():
    resp = requests.get(f"{BACKEND_URL}/auth/url")
    return resp.json()["auth_url"]

# Helper: handle OAuth callback (after redirect)
def handle_oauth_callback():
    st.info("Paste the 'code' parameter from the redirected URL after Google sign-in:")
    auth_code = st.text_input("Authorization Code", "")
    if st.button("Submit Code") and auth_code:
        resp = requests.post(f"{BACKEND_URL}/auth/callback", json={"code": auth_code})
        if resp.status_code == 200:
            st.session_state.user_info = resp.json()
            st.success(f"Signed in as {st.session_state.user_info['name']}")
        else:
            st.error("Authentication failed. Please try again.")

# File validation helper
def is_valid_file(file):
    allowed_types = ["csv", "pdf", "png", "jpg", "jpeg"]
    max_size_mb = 10
    ext = file.name.split(".")[-1].lower()
    if ext not in allowed_types:
        return False, f"Invalid file type: {ext}"
    if file.size > max_size_mb * 1024 * 1024:
        return False, "File exceeds 10 MB limit"
    return True, ""

def detect_target_sheet(file):
    ext = file.name.split(".")[-1].lower()
    if ext == "csv":
        return "Budget"
    elif ext in ["pdf", "png", "jpg", "jpeg"]:
        return "Portfolio"
    else:
        return "Unknown"

# Simulate processing rows count
def simulate_row_count(file):
    return random.randint(10, 100)

# Simulate extraction (success or fail randomly)
def simulate_extraction(file):
    # 10% chance to fail
    if random.random() < 0.1:
        return None, True
    # Simulate 100 rows of random data
    cols = [f"Col{i+1}" for i in range(8)]
    data = [[random.randint(1, 100) for _ in cols] for _ in range(100)]
    df = pd.DataFrame(data, columns=cols)
    return df, False

# Main UI logic
if st.session_state.user_info:
    st.image(st.session_state.user_info["picture"], width=48)
    st.write(f"Welcome, {st.session_state.user_info['name']}!")
    st.write("## Upload your files")
    uploaded_files = st.file_uploader(
        "Drop CSV/PDF/PNG here or Browse",
        type=["csv", "pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    # Add valid files to queue
    if uploaded_files:
        for file in uploaded_files:
            valid, msg = is_valid_file(file)
            if valid:
                if file.name not in [f["Filename"] for f in st.session_state.upload_queue]:
                    st.session_state.upload_queue.append({
                        "Filename": file.name,
                        "Detected Type": file.type,
                        "Target Sheet": detect_target_sheet(file),
                        "Status": "✅ Valid"
                    })
                    st.success(f"{file.name}: File is valid! ✅")
            else:
                st.error(f"{file.name}: {msg}")
    # Show queue table with editable Target Sheet and Preview button
    if st.session_state.upload_queue:
        st.write("### Upload Queue")
        for i, file in enumerate(st.session_state.upload_queue):
            cols = st.columns([3, 2, 2, 2, 2])
            cols[0].write(file["Filename"])
            cols[1].write(file["Detected Type"])
            # Dropdown for Target Sheet
            new_target = cols[2].selectbox(
                "Target Sheet",
                SHEET_NAMES,
                index=SHEET_NAMES.index(file["Target Sheet"]) if file["Target Sheet"] in SHEET_NAMES else 0,
                key=f"target_sheet_{i}"
            )
            if new_target != file["Target Sheet"]:
                st.session_state.upload_queue[i]["Target Sheet"] = new_target
            cols[3].write(file["Status"])
            # Preview button
            if cols[4].button("Preview", key=f"preview_{i}"):
                df, error = simulate_extraction(file)
                st.session_state.preview_file_idx = i
                st.session_state.preview_error = error
                if not error:
                    st.session_state.preview_df = df
        # Preview modal/expander
        if st.session_state.preview_file_idx is not None:
            idx = st.session_state.preview_file_idx
            with st.expander(f"Preview: {st.session_state.upload_queue[idx]['Filename']}", expanded=True):
                if st.session_state.preview_error:
                    st.error("Cannot preview – extraction error")
                else:
                    st.dataframe(st.session_state.preview_df, use_container_width=True, height=400)
                col_confirm, col_abort, col_close = st.columns([2,2,1])
                confirm_clicked = col_confirm.button("Confirm", key="confirm_btn")
                abort_clicked = col_abort.button("Abort", key="abort_btn")
                close_clicked = col_close.button("Close Preview", key="close_btn")
                if confirm_clicked:
                    st.session_state.upload_queue[idx]["Status"] = "🟢 Confirmed"
                    st.toast(f"{st.session_state.upload_queue[idx]['Filename']} confirmed for upload.", icon="✅")
                    st.session_state.preview_file_idx = None
                    st.session_state.preview_error = False
                    st.session_state.preview_df = None
                elif abort_clicked:
                    st.session_state.upload_queue[idx]["Status"] = "❌ Cancelled"
                    st.toast(f"{st.session_state.upload_queue[idx]['Filename']} upload cancelled.", icon="❌")
                    st.session_state.preview_file_idx = None
                    st.session_state.preview_error = False
                    st.session_state.preview_df = None
                elif close_clicked:
                    st.session_state.preview_file_idx = None
                    st.session_state.preview_error = False
                    st.session_state.preview_df = None
        # Simulate upload and processing
        if st.button("Start Uploads"):
            failed_files = []
            total_rows = 0
            run_log = []
            for i, file in enumerate(st.session_state.upload_queue):
                filename = file["Filename"]
                # Simulate upload progress
                progress_bar = st.progress(0, text=f"Uploading {filename}")
                for percent in range(0, 101, 10):
                    progress_bar.progress(percent, text=f"Uploading {filename} ({percent}%)")
                    time.sleep(0.05)
                progress_bar.empty()
                # Update status to Processing
                st.session_state.upload_queue[i]["Status"] = "⏳ Processing..."
                temp_df = pd.DataFrame(st.session_state.upload_queue)
                st.dataframe(temp_df, use_container_width=True)
                with st.spinner(f"Processing {filename}..."):
                    time.sleep(0.5)
                # Simulate success or error
                if filename.endswith(".csv") or filename.endswith(".pdf") or filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    n_rows = simulate_row_count(file)
                    st.session_state.upload_queue[i]["Status"] = f"✅ Done ({n_rows} rows)"
                    total_rows += n_rows
                    run_log.append({"file": filename, "status": "Done", "rows": n_rows, "target": file["Target Sheet"]})
                else:
                    st.session_state.upload_queue[i]["Status"] = "❌ Error"
                    failed_files.append(filename)
                    run_log.append({"file": filename, "status": "Error", "rows": 0, "target": file["Target Sheet"]})
                temp_df = pd.DataFrame(st.session_state.upload_queue)
                st.dataframe(temp_df, use_container_width=True)
            st.session_state.run_log = run_log
            # Show summary toast
            if failed_files:
                if st.toast(f"Failed files: {', '.join(failed_files)}. Click for details.", icon="❌"):
                    st.session_state.show_run_log = True
            else:
                if st.toast(f"All files uploaded successfully! Total rows inserted: {total_rows}. Click for details.", icon="✅"):
                    st.session_state.show_run_log = True
    # Run log modal placeholder
    if st.session_state.show_run_log:
        with st.expander("Run Log Details", expanded=True):
            st.write(pd.DataFrame(st.session_state.run_log))
            if st.button("Close Log"):
                st.session_state.show_run_log = False
else:
    st.write("## Please sign in to continue")
    if st.button("Sign in with Google"):
        oauth_url = get_oauth_url()
        webbrowser.open_new(oauth_url)
        st.info("After signing in, you will be redirected. Copy the 'code' from the URL and paste it below.")
    handle_oauth_callback()

if __name__ == "__main__":
    main()
