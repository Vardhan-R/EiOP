import streamlit as st
import time

EXP_USRN = "nonames"	# expected username
PSWD_TOL = 86400		# password tolerance
PSWD_TOL = 1e11			# password tolerance

st.set_page_config(page_title="Login")

if "logged_in" in st.session_state:
	if st.session_state.logged_in:
		st.write(f"You're already logged in as \"{st.session_state.username}\".")
	else:
		with st.form("creds"):
			username = st.text_input("Username", placeholder="Username")
			password = st.text_input("Password", type="password", placeholder="Password")

			submitted = st.form_submit_button()
			if submitted:
				if username == EXP_USRN:
					try:
						pswd = int(password)
						if abs(pswd - time.time()) <= PSWD_TOL:
							st.session_state.username = username
							st.session_state.logged_in = True
							st.write("Logging in...")
							st.switch_page("st_tst_3.py")
						else:
							st.write("Incorrect password.")
					except ValueError:
						st.write("Incorrect password.")
				else:
					st.write("Incorrect username.")
else:
	st.write("Something's not right... please visit the homepage by clicking on the link below.")

st.page_link("st_tst_3.py", label="Back to Home", icon="🏠")
# st.page_link("pages/login.py", label="Login", icon="👤")
# st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.co.in", label="Google", icon="🌎")
