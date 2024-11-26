from uuid import getnode as getMACAddr
import streamlit as st
import time

EXP_USRN = "nonames"	# expected username
PSWD_TOL = 86400		# password tolerance
devices_path = "pages/common/devices.txt"

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
								mac = getMACAddr()
								with open(devices_path, 'a') as fp:
									fp.write(f"{mac} {username}\n")

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
