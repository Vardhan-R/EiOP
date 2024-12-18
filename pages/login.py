from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import streamlit as st

def checkPassword(password: str) -> bool:
	encoded_password = password.encode()
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=b"0123456789abcdef",
		iterations=480000,
	)
	key = base64.urlsafe_b64encode(kdf.derive(encoded_password))
	return key == b"W8qZ2jwiwPqH_oGL-kfkfGXuxIU9G_kXb0JlJVGmR1Q="

EXP_USRN = "nonames"	# expected username

st.set_page_config(page_title="Login")

if "logged_in" in st.session_state:
	if st.session_state.logged_in:
		st.write(f"You're already logged in as \"{st.session_state.username}\".")
	else:
		with st.form("creds"):
			username = st.text_input("Username", placeholder="Username")
			password = st.text_input("Password", type="password", placeholder="Password")
			remember = st.checkbox("Remember me", disabled=True, help="Feature disabled")

			submitted = st.form_submit_button()
			if submitted:
				if username == EXP_USRN:
					if checkPassword(password):
						st.session_state.username = username
						st.session_state.logged_in = True
						st.success("Logging in...")
						st.switch_page("home.py")
					else:
						st.error("Incorrect password.")
				else:
					st.error("Incorrect username.")
else:
	st.write("Something's not right... please visit the homepage by clicking on the link below.")

st.page_link("home.py", label="Back to Home", icon="🏠")
