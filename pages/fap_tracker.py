from calendar import timegm
from datetime import datetime
from matplotlib import colormaps
from time import time
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

class Tracker:
	def __init__(self) -> None:
		self.xx_mesh, self.yy_mesh = np.mgrid[1:32, 1:13]
		self.all_cnts = np.zeros((31, 12))
		self.tz_offset = 0	# in days

	def convertRawData(self, input_file: str, output_file: str, yy_0: int, mm_0: int, dd_0: int):
		self.rawGetCounts(input_file, yy_0, mm_0, dd_0)
		return self.saveCounts(output_file)

	def customColours(self) -> list[str]:
		def hexify(c: int) -> str:
			d = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
			return d[c // 16] + d[c % 16]

		max_faps = int(self.all_cnts.max())

		cmap = colormaps.get("Blues", 256)
		custom_clrs = ["#C0C0C0", "#808080", "#FFFFFF"]

		for clr in [cmap(int((i + 1) * 255 / max_faps)) for i in range(max_faps)]:
			custom_clrs.append(f"#{hexify(int(clr[0] * 255))}{hexify(int(clr[1] * 255))}{hexify(int(clr[2] * 255))}")

		# custom_clrs = ["#C0C0C0", "#808080", "#FFFFFF"]
		# for i in range(max_faps):
		# 	x = int(i * 255 / max_faps)
		# 	custom_clrs.append(f"#{hexify(255 - x)}{hexify(255 - int(x / 1.75))}FF")

		return custom_clrs

	def getCounts(self, from_file: str, update: bool = True) -> tuple:
		if update:
			self.all_cnts = np.fromfile(from_file).reshape((31, 12))
			return self.xx_mesh, self.yy_mesh, self.all_cnts
		temp_all_cnts = np.fromfile(from_file).reshape((31, 12))
		return self.xx_mesh, self.yy_mesh, temp_all_cnts

	def rawGetCounts(self, input_file: str, yy_0: int, mm_0: int, dd_0: int) -> tuple:
		with open(input_file, 'r') as fp:
			raw_lines = fp.readlines()

		# yy_0, mm_0, dd_0 = 2024, 7, 23
		ref_uts = timegm(datetime(yy_0, mm_0, dd_0, 0, 0, 0).timetuple())
		curr_uts = int(time()) + SECS_PER_DAY * self.tz_offset
		mm_curr, dd_curr = map(int, datetime.fromtimestamp(curr_uts).strftime("%m %d").split(' '))

		n_days = int((curr_uts - ref_uts) // SECS_PER_DAY + 2)
		cnts = [0] * n_days
		# dates = [tuple(map(int, datetime.fromtimestamp(ref_uts + i * SECS_PER_DAY).strftime("%m %d").split(' '))) for i in range(n_days)]

		# all_dates = np.mgrid[1:32, 1:13].reshape(2, -1).T
		self.all_cnts *= 0
		self.all_cnts[:, :mm_0 - 1] = -2
		self.all_cnts[:dd_0 - 1, mm_0 - 1] = -2
		self.all_cnts[dd_curr:, mm_curr - 1] = -2
		self.all_cnts[:, mm_curr:] = -2
		self.all_cnts[29, 1] = self.all_cnts[30, 1] = self.all_cnts[30, 3] = self.all_cnts[30, 5] = self.all_cnts[30, 8] = self.all_cnts[30, 10] = -1

		for line in raw_lines:
			msg = line[30:].strip()
			if msg[0] == 'i':
				dd, mm, yy = map(int, line[1:9].split('/'))
				yy += 2000
				uts = timegm(datetime(yy, mm, dd).timetuple())
				if uts >= ref_uts:
					if len(msg) > 1:
						dd, mm, yy = map(int, msg[3:-1].split('/'))
						uts = timegm(datetime(yy, mm, dd).timetuple())
					cnts[int((uts - ref_uts) // SECS_PER_DAY)] += 1
					self.all_cnts[dd - 1, mm - 1] += 1

		return self.xx_mesh, self.yy_mesh, self.all_cnts

	def saveCounts(self, output_file: str):
		self.all_cnts.tofile(output_file)
		return True

	def updateCounts(self, diff: int) -> tuple:
		curr_uts = int(time()) + SECS_PER_DAY * self.tz_offset
		mm_curr, dd_curr = map(int, datetime.fromtimestamp(curr_uts).strftime("%m %d").split(' '))
		self.all_cnts[dd_curr - 1, mm_curr - 1] = max(self.all_cnts[dd_curr - 1, mm_curr - 1] + diff, 0.0)
		return self.xx_mesh, self.yy_mesh, self.all_cnts

	def updateTzOffset(self, diff: int) -> None:
		self.tz_offset = max(min(self.tz_offset + diff, 1), -1)

st.set_page_config(page_title="Fap Tracker")

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("home.py")

SECS_PER_DAY = 86_400
MONTHS = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
files_path = "pages/common"
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
	st.session_state.tracker = Tracker()

	# x, y, z = st.session_state.tracker.rawGetCounts(r"./_chat.txt", 2024, 7, 23)
	# st.session_state.tracker.saveCounts("./cnts.txt")
	x, y, z = st.session_state.tracker.getCounts(cnts_path)

st.title("Fap Tracker (2024)")

cols = st.columns([1, 1, 2, 1, 1, 1])	# Adjust column ratios as needed

with cols[0]:
	if st.button("+1"):
		st.session_state.tracker.updateCounts(1)

with cols[1]:
	if st.button("-1"):
		st.session_state.tracker.updateCounts(-1)

with cols[2]:
	if st.button("Save data"):
		st.session_state.tracker.saveCounts(cnts_path)

with cols[3]:
	if st.button("◀", disabled=st.session_state.tracker.tz_offset < 0):
		st.session_state.tracker.updateTzOffset(-1)

with cols[4]:
	curr_uts = int(time()) + SECS_PER_DAY * st.session_state.tracker.tz_offset
	mm_curr, dd_curr = datetime.fromtimestamp(curr_uts).strftime("%m, %d").split(',')
	st.write(MONTHS[mm_curr] + dd_curr)

with cols[5]:
	if st.button("▶", disabled=st.session_state.tracker.tz_offset > 0):
		st.session_state.tracker.updateTzOffset(1)

disp()

with st.form("upload"):
	uploaded_file = st.file_uploader("Choose files")

	submitted = st.form_submit_button("Overwrite counts", icon='🚀')
	if uploaded_file and submitted:
		st.write(f"Saving {uploaded_file.name}...")
		bytes_data = uploaded_file.getvalue()
		with open(f"{files_path}/_chat.txt", 'wb') as fp:
			fp.write(bytes_data)
		st.write(f"Saved {uploaded_file.name}")

		st.session_state.tracker.convertRawData(f"{files_path}/_chat.txt", cnts_path, 2024, 7, 23)

st.page_link("home.py", label="Back to Home", icon='🏠')
