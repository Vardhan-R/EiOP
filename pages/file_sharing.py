import streamlit as st

st.set_page_config(page_title="File Sharing")

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("st_tst_3.py")

files_path = "pages/common/shared_files"

st.title("Share Files")

col_1, col_2 = st.columns([1, 1])

with col_1:
	st.header("Download Files")
	st.write("Coming soon...")

with col_2:
	st.header("Upload Files")
	st.write("Coming soon...")

st.page_link("st_tst_3.py", label="Back to Home", icon="🏠")
