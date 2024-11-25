import altair as alt
import pandas as pd
import streamlit as st
import tracker

st.set_page_config(page_title="Fap Tracker")

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("st_tst_3.py")

cnts_path = "pages/common/cnts.txt"

def disp():
	# Convert this grid to columnar data expected by Altair
	x, y, z = st.session_state.tracker.xx_mesh, st.session_state.tracker.yy_mesh, st.session_state.tracker.all_cnts

	source = pd.DataFrame(
		{"Day": x.ravel(),
		 "Month": y.ravel(),
		 "Count": z.ravel()}
	)

	custom_scale = alt.Scale(
		domain=[-2, z.max()],
		range=st.session_state.tracker.customColours()
	)

	c = alt.Chart(source).mark_rect().encode(
		alt.X("Day:O").axis(labelAngle=0),
		alt.Y("Month:O").axis(labelExpr="['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][datum.value - 1]"),
		color=alt.Color("Count:Q", scale=custom_scale)
	)
	st.write(c)

if "tracker" not in st.session_state:
	st.session_state.tracker = tracker.Tracker()

	# x, y, z = st.session_state.tracker.rawGetCounts(r"./_chat.txt", 2024, 7, 23)
	# st.session_state.tracker.saveCounts("./cnts.txt")
	x, y, z = st.session_state.tracker.getCounts(cnts_path)

st.title("Fap Tracker (2024)")

col_1, col_2, col_3 = st.columns([1, 1, 5])	# Adjust column ratios as needed

with col_1:
	if st.button("+1"):
		st.session_state.tracker.updateCounts(1)

with col_2:
	if st.button("-1"):
		st.session_state.tracker.updateCounts(-1)

with col_3:
	if st.button("Save data"):
		st.session_state.tracker.saveCounts(cnts_path)

disp()

st.page_link("st_tst_3.py", label="Back to Home", icon="🏠")
