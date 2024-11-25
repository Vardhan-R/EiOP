import streamlit as st
# import time

title = "Everything in One Place."
# st.markdown("<h3 style='font-family:Arial; color:green;'>User Data</h3>", unsafe_allow_html=True)

# def streamData():
# 	for char in title:
# 		yield char
# 		if char == ' ':
# 			time.sleep(0.2)
# 		else:
# 			time.sleep(0.05)

if "logged_in" not in st.session_state:
	st.session_state.logged_in = False
	st.session_state.username = None

st.set_page_config(page_title="Home")
st.title(title)
# st.write_stream(streamData)

is_disabled = not st.session_state.logged_in

st.page_link("st_tst_3.py", label="Home", icon="🏠")
if is_disabled:
	st.page_link("pages/login.py", label="Login", icon="👤")
st.page_link("pages/fap_tracker.py", label="Fap Tracker", icon="💦", disabled=is_disabled)
st.page_link("pages/nhentai.py", label="nhentai", icon="🌚", disabled=is_disabled)
st.page_link("pages/file_sharing.py", label="File Sharing", icon="📝", disabled=is_disabled)

if st.session_state.logged_in:
	if st.button("Logout"):
		st.session_state.logged_in = False
		st.session_state.username = None
		st.switch_page("st_tst_3.py")
