from pages.common.cookies_manager import initCookies
import streamlit as st

title = "Everything in One Place."

# st.set_page_config(page_title="Home")

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
	st.error("Cookies not initialised yet.")
	st.stop()

st.title(title)

# Opened just now?
if "username" not in cookies:
	cookies["username"] = ""
	cookies.save()

is_disabled = not cookies["username"]

st.page_link("home.py", label="Home", icon='🏠')
if is_disabled:
	st.page_link("pages/login.py", label="Login", icon='👤')
st.page_link("pages/fap_tracker.py", label="Fap Tracker", icon='💦', disabled=is_disabled)
st.page_link("pages/nhentai.py", label="nhentai", icon='🌚', disabled=is_disabled)
st.page_link("pages/chat.py", label="Chat", icon='💬', disabled=is_disabled)
st.page_link("pages/file_sharing.py", label="File Sharing", icon='📝', disabled=is_disabled)

if cookies["username"]:
	if st.button("Logout"):
		cookies["logged in"] = ""
		cookies["username"] = ""
		cookies.save()

		st.rerun()
