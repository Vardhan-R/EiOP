from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from time import time
import streamlit as st

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

def storeSessionInfo(path: str) -> None:
	try:
		ctx = get_script_run_ctx()
		if ctx is None:
			return None

		session_info = runtime.get_instance().get_client(ctx.session_id)
		if session_info is None:
			return None
	except Exception as e:
		return None

	str_to_append = f"[{time()}] {session_info.request.headers}\n\n"
	st.write(str_to_append)
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

# Remember device?
cookie_id = getAnonymousCookieID()

with open(cookies_path, 'r') as fp:
	while line := fp.readline():
		stored_cookie_id, stored_username = line.strip().split(' ')
		if cookie_id == stored_cookie_id:	# remember
			st.session_state.logged_in = True
			st.session_state.username = stored_username

is_disabled = not st.session_state.logged_in

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
