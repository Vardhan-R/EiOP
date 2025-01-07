from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from time import time
import streamlit as st
from uuid import getnode as get_mac
import psutil

def get_network_connections():
	connections = psutil.net_connections(kind='inet')
	for conn in connections:
		laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
		raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
		if conn.status != "NONE":
			st.write(f"Type: {conn.type}, Status: {conn.status}, Local Address: {laddr}, Remote Address: {raddr}")

def getAnonymousCookieID() -> str | None:
	"""Get remote ip."""

	try:
		ctx = get_script_run_ctx()
		if ctx is None:
			return None

		session_info = runtime.get_instance().get_client(ctx.session_id)
		if session_info is None:
			return None
	except Exception as e:
		return None

	# st.write(session_info.request.headers)
	try:
		cookies = session_info.request.headers["Cookie"].split("; ")
		for cookie in cookies:
			cookie_type, cookie_id = cookie.split("=")
			if cookie_type == "ajs_anonymous_id":
				return cookie_id
	except Exception as e:
		return None

def getSessionInfo() -> str:
	try:
		ctx = get_script_run_ctx()
		if ctx is None:
			return None

		session_info = runtime.get_instance().get_client(ctx.session_id)
		if session_info is None:
			return None
	except Exception as e:
		return None

	return session_info

	res_dict = session_info.request.headers
	res = '\n'.join([f"{k}: {res_dict[k]}" for k in res_dict.keys()])
	return f"[{time()}]\n{res}\n"

def storeInfo(str_to_append: str, path: str) -> None:
	with open(path, 'a') as fp:
		fp.write(str_to_append)

title = "Everything in One Place."
cookies_path = "pages/common/cookies.txt"
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

	# session_info = getSessionInfo()
	# storeInfo(session_info, "pages/common/session_info.txt")

# st.text(get_mac())
# get_network_connections()

# Remember device?
cookie_id = getAnonymousCookieID()

with open(cookies_path, 'r') as fp:
	while line := fp.readline():
		stored_cookie_id, stored_username = line.strip().split(' ')
		if cookie_id == stored_cookie_id:	# remember
			st.session_state.logged_in = True
			st.session_state.username = stored_username

is_disabled = not st.session_state.logged_in

st.page_link("pages/device_info.py", label="Device Info", icon='🖥')
st.page_link("home.py", label="Home", icon='🏠')
if is_disabled:
	st.page_link("pages/login.py", label="Login", icon='👤')
st.page_link("pages/fap_tracker.py", label="Fap Tracker", icon='💦', disabled=is_disabled)
st.page_link("pages/nhentai.py", label="nhentai", icon='🌚', disabled=is_disabled)
st.page_link("pages/chat.py", label="Chat", icon='💬', disabled=is_disabled)
st.page_link("pages/file_sharing.py", label="File Sharing", icon='📝', disabled=is_disabled)

if st.session_state.logged_in:
	if st.button("Logout"):
		st.session_state.logged_in = False
		st.session_state.username = None

		all_rems = []
		with open(cookies_path, 'r') as fp:
			while line := fp.readline():
				stored_cookie_id, stored_username = line.strip().split(' ')
				if cookie_id != stored_cookie_id:	# remembered
					all_rems.append(line)

		with open(cookies_path, 'w') as fp:
			fp.writelines(all_rems)

		st.switch_page("home.py")
