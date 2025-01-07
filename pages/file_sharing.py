from os import walk
from pages.common.cookies_manager import initCookies
import streamlit as st

# st.set_page_config(page_title="File Sharing")

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
	st.error("Cookies not initialised yet.")
	st.stop()

if "username" in cookies:
	if not cookies["username"]:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("home.py")

files_path = "pages/common/shared_files"

col_1, col_2 = st.columns([4, 1])

with col_1:
	st.title("Share Files")

with col_2:
	st.page_link("home.py", label="Back to Home", icon='🏠')

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
				file_name=file_name,
				key=i,
				icon='✨'
			)
		i += 1
