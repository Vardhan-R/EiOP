import streamlit as st

EXP_PSWD = 1732
EXP_PSWD_D_N = 328

n = 3233
e = 17

st.set_page_config(page_title="Login")

if "logged_in" in st.session_state:
	if st.session_state.logged_in:
		st.write(f"You're already logged in as \"{st.session_state.username}\".")
	else:
		with st.form("creds"):
			password = st.text_input("password", type="password", placeholder="Password")
			d_key = st.text_input("d", type="password", placeholder="Decryption key")

			submitted = st.form_submit_button()
			if submitted:
				try:
					pswd = int(password)
					d = int(d_key)
					if pswd == EXP_PSWD and pswd ** d % n == EXP_PSWD_D_N:
						st.session_state.username = "nonames"
						st.session_state.n = n
						st.session_state.e = e
						st.session_state.d = d
						st.session_state.logged_in = True
						st.write("Logging in...")
						st.switch_page("home.py")
					else:
						st.write("Incorrect credentials.")
				except:
					st.write("Incorrect credentials.")
else:
	st.write("Something's not right... please visit the homepage by clicking on the link below.")

st.page_link("home.py", label="Back to Home", icon="🏠")
