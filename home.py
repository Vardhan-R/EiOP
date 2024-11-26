from uuid import getnode as getMACAddr
import streamlit as st

title = "Everything in One Place."
devices_path = "pages/common/devices.txt"
# st.markdown("<h3 style='font-family:Arial; color:green;'>User Data</h3>", unsafe_allow_html=True)

# def streamData():
# 	for char in title:
# 		yield char
# 		if char == ' ':
# 			time.sleep(0.2)
# 		else:
# 			time.sleep(0.05)

st.set_page_config(page_title="Home")
st.title(title)
# st.write_stream(streamData)

# Opened just now?
if "logged_in" not in st.session_state:
	st.session_state.logged_in = False
	st.session_state.username = None

# Remember device?
mac = str(getMACAddr())
with open(devices_path, 'r') as fp:
	while line := fp.readline():
		stored_mac, stored_username = line.strip().split(' ')
		if mac == stored_mac:	# remember
			st.session_state.logged_in = True
			st.session_state.username = stored_username

is_disabled = not st.session_state.logged_in

st.page_link("home.py", label="Home", icon="🏠")
if is_disabled:
	st.page_link("pages/login.py", label="Login", icon="👤")
st.page_link("pages/fap_tracker.py", label="Fap Tracker", icon="💦", disabled=is_disabled)
st.page_link("pages/nhentai.py", label="nhentai", icon="🌚", disabled=is_disabled)
st.page_link("pages/chat.py", label="Chat", icon="💬", disabled=is_disabled)
st.page_link("pages/file_sharing.py", label="File Sharing", icon="📝", disabled=is_disabled)

if st.session_state.logged_in:
	if st.button("Logout"):
		st.session_state.logged_in = False
		st.session_state.username = None

		all_rems = []
		with open(devices_path, 'r') as fp:
			while line := fp.readline():
				stored_mac, stored_username = line.strip().split(' ')
				if mac != stored_mac:	# remembered
					all_rems.append(line)

		with open(devices_path, 'w') as fp:
			fp.writelines(all_rems)

		st.switch_page("home.py")
