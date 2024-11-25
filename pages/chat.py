from time import time
import streamlit as st

st.set_page_config(page_title="Chat")

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("st_tst_3.py")

chat_path = "pages/common/chat.txt"

st.title("Chat")

st.page_link("st_tst_3.py", label="Back to Home", icon="🏠")

# Initialize session state for chat history
if "messages" not in st.session_state:
	with open(chat_path, 'r') as fp:
		st.session_state.messages = fp.readlines()  # A list to store message history

# Input for new chat messages
if msg := st.chat_input("Thots?"):
	# Store the user's message
	uts = time()
	s = f"[{uts}] {msg}\n"
	st.session_state.messages.append(s)
	with open(chat_path, 'a') as fp:
		fp.write(s)

# Display chat history
for uts_msg in st.session_state.messages:
	st.chat_message("user").write(uts_msg)
