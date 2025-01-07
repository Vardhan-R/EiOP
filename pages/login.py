from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pages.common.cookies_manager import initCookies
import streamlit as st

def checkPassword(password: str) -> bool:
	encoded_password = password.encode()
	kdf = PBKDF2HMAC(
		algorithm=SHA256(),
		length=32,
		salt=b"0123456789abcdef",
		iterations=480_000,
	)
	key = urlsafe_b64encode(kdf.derive(encoded_password))
	return key == b"W8qZ2jwiwPqH_oGL-kfkfGXuxIU9G_kXb0JlJVGmR1Q="

# def checkUsername(username: str) -> bool:
# 	with open("usernames.txt", 'r') as fp:
# 		raw_lines = fp.readlines()

# 	for line in raw_lines:
# 		if username == line[:-1]:
# 			return False

# 	return True

EXP_USRN = "nonames"	# expected username

# st.set_page_config(page_title="Login")

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
	st.error("Cookies not initialised yet.")
	st.stop()

if "username" in cookies:
	if cookies["username"]:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("home.py")

# login_tab, register_tab = st.tabs(["Login", "Register"])

# with login_tab:
st.header("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
# remember = st.checkbox("Remember me")
if st.button("Login"):
	if username == EXP_USRN:
		if checkPassword(password):
			cookies["username"] = username
			cookies.save()
			st.success("Logging in...")
			st.switch_page("home.py")
		else:
			st.error("Incorrect password.")
	else:
		st.error("Incorrect username.")

# with register_tab:
# 	st.header("Register")
# 	with st.form("register"):
# 		usrn = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
# 		pswd = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
# 		c_pswd = st.text_input("Confirm password", type="password", placeholder="Confirm password", label_visibility="collapsed")
# 		submitted = st.form_submit_button("Register")
# 		if submitted:
# 			if usrn != "":
# 				if checkUsername(usrn):
# 					if pswd == c_pswd:
# 						pswd_hash = sha256(pswd.encode()).hexdigest()
# 						with open("usernames.txt", 'a') as fp:
# 							fp.write(f"{usrn}\n")
# 						with open("users_credentials.txt", 'a') as fp:
# 							fp.write(f"{usrn} {pswd_hash}\n")
# 						st.success("Registered successfully!")
# 						st.switch_page("pages/login.py")
# 					else:
# 						st.error("Passwords don't match.")
# 				else:
# 					st.error("Username is taken.")
# 			else:
# 				st.error("Enter a username.")
