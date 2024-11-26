from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st
import time

EXP_USRN = "nonames"	# expected username
PSWD_TOL = 86400		# password tolerance
cookies_path = "pages/common/devices.txt"

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

	st.write(session_info.request.headers)
	cookies = session_info.request.headers["Cookie"].split("; ")
	for cookie in cookies:
		cookie_type, cookie_id = cookie.split("=")
		if cookie_type == "ajs_anonymous_id":
			return cookie_id

st.set_page_config(page_title="Login")

if "logged_in" in st.session_state:
	if st.session_state.logged_in:
		st.write(f"You're already logged in as \"{st.session_state.username}\".")
	else:
		with st.form("creds"):
			username = st.text_input("Username", placeholder="Username")
			password = st.text_input("Password", type="password", placeholder="Password")
			remember = st.checkbox("Remember me")

			submitted = st.form_submit_button()
			if submitted:
				if username == EXP_USRN:
					try:
						pswd = int(password)
						if abs(pswd - time.time()) <= PSWD_TOL:
							st.session_state.username = username
							st.session_state.logged_in = True

							if remember:
								cookie_id = getAnonymousCookieID()
								with open(cookies_path, 'a') as fp:
									fp.write(f"{cookie_id} {username}\n")

							st.write("Logging in...")
							st.switch_page("home.py")
						else:
							st.write("Incorrect password.")
					except ValueError:
						st.write("Incorrect password.")
				else:
					st.write("Incorrect username.")
else:
	st.write("Something's not right... please visit the homepage by clicking on the link below.")

st.page_link("home.py", label="Back to Home", icon="🏠")
