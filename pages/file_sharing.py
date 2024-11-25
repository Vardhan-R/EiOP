from os import walk
import streamlit as st

st.set_page_config(page_title="File Sharing")

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("st_tst_3.py")

files_path = "pages/common/shared_files"

st.title("Share Files")

_, rgt_col = st.columns([4, 1])
with rgt_col:
	st.page_link("st_tst_3.py", label="Back to Home", icon="🏠")

col_1, col_2 = st.columns([1, 1])

with col_1:
	st.header("Upload Files")

	with st.form("uploads"):
		uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

		submitted = st.form_submit_button("Upload", icon='🚀')
		if submitted:
			for uploaded_file in uploaded_files:
				st.write(f"Saving {uploaded_file.name}...")
				bytes_data = uploaded_file.getvalue()
				with open(f"{files_path}/{uploaded_file.name}", 'wb') as fp:
					fp.write(bytes_data)
				st.write(f"Saved {uploaded_file.name}")

with col_2:
	st.header("Download Files")

	file_names = next(walk(files_path), (None, None, []))[2]	# [] if no file
	i = 0
	for file_name in file_names:
		with open(f"{files_path}/{file_name}", 'rb') as file:
			btn = st.download_button(
				label=file_name,
				data=file,
				key=i,
				icon='✨'
			)
		i += 1
