from time import time
import streamlit as st

st.set_page_config(page_title="Chat")

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("home.py")

chat_path = "pages/common/chat.txt"

st.title("Chat")

# Initialize session state for chat history
if "messages" not in st.session_state:
	with open(chat_path, 'r') as fp:
		st.session_state.messages = fp.readlines()  # A list to store message history
	st.session_state.disp_msgs = 10

lft_col, mid_col, rgt_col = st.columns([2, 2, 1])

messages = st.container(height=360)

# Input for new chat messages
if msg := st.chat_input("Thots?"):
	# Store the user's message
	uts = time()
	s = f"[{uts}] {msg}\n"
	st.session_state.messages.append(s)
	with open(chat_path, 'a') as fp:
		fp.write(s)

with lft_col:
	# Load more messages
	if st.button("Load more messages"):
		st.session_state.disp_msgs = max(min(2 * st.session_state.disp_msgs, len(st.session_state.messages)), 10)

with mid_col:
	# Display chat history
	with open(chat_path, 'r') as fp:
		st.session_state.messages = fp.readlines()  # A list to store message history
	for uts_msg in st.session_state.messages[-st.session_state.disp_msgs:]:
		messages.chat_message("user").write(uts_msg)

with rgt_col:
	st.page_link("home.py", label="Back to Home", icon="🏠")
