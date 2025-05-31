from calendar import timegm
from datetime import datetime, timedelta
from os.path import join
from pages.common.cookies_manager import initCookies
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
        self.tz_offset = 0      # in days

    def convertRawData(self, input_file: str, output_file: str, yyyy_0: int, mm_0: int, dd_0: int):
        self.rawGetCounts(input_file, yyyy_0, mm_0, dd_0)
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
        #     x = int(i * 255 / max_faps)
        #     custom_clrs.append(f"#{hexify(255 - x)}{hexify(255 - int(x / 1.75))}FF")

        return custom_clrs

    def getCounts(self, from_file: str, update: bool = True) -> tuple:
        if update:
            self.all_cnts = np.fromfile(from_file).reshape((31, 12))
            return self.xx_mesh, self.yy_mesh, self.all_cnts
        temp_all_cnts = np.fromfile(from_file).reshape((31, 12))
        return self.xx_mesh, self.yy_mesh, temp_all_cnts

    def rawGetCounts(self, input_file: str, yyyy_0: int, mm_0: int, dd_0: int) -> tuple:
        with open(input_file, 'r') as fp:
            raw_lines = fp.readlines()

        # yyyy_0, mm_0, dd_0 = 2024, 7, 23
        start_uts = timegm(datetime(yyyy_0, mm_0, dd_0, 0, 0, 0).timetuple())
        end_uts = timegm(datetime(yyyy_0 + 1, 1, 1, 0, 0, 0).timetuple())
        curr_uts = int(time()) + SECS_PER_DAY * self.tz_offset
        mm_curr, dd_curr = map(int, datetime.fromtimestamp(curr_uts).strftime("%m %d").split(' '))

        # n_days = int((curr_uts - start_uts) // SECS_PER_DAY + 2)
        # cnts = [0] * n_days
        # dates = [tuple(map(int, datetime.fromtimestamp(start_uts + i * SECS_PER_DAY).strftime("%m %d").split(' '))) for i in range(n_days)]

        # all_dates = np.mgrid[1:32, 1:13].reshape(2, -1).T
        self.all_cnts *= 0
        self.all_cnts[:, :mm_0 - 1] = -2
        self.all_cnts[:dd_0 - 1, mm_0 - 1] = -2
        if yyyy_0 == curr_yr:
            self.all_cnts[dd_curr:, mm_curr - 1] = -2
            self.all_cnts[:, mm_curr:] = -2
        self.all_cnts[29, 1] = self.all_cnts[30, 1] = self.all_cnts[30, 3] = self.all_cnts[30, 5] = self.all_cnts[30, 8] = self.all_cnts[30, 10] = -1
        if not(yyyy_0 % 4 == 0 and yyyy_0 % 400 != 0):
            self.all_cnts[28, 1] = -1

        for line in raw_lines:
            msg = line[30:].strip()
            if msg[0] == 'i':
                dd, mm, yy = map(int, line[1:9].split('/'))
                yyyy = yy + 2000
                uts = timegm(datetime(yyyy, mm, dd).timetuple())
                if uts >= start_uts:
                    if len(msg) > 1:
                        dd, mm, yyyy = map(int, msg[3:-1].split('/'))
                        uts = timegm(datetime(yyyy, mm, dd).timetuple())
                    if uts < end_uts:
                        # cnts[int((uts - start_uts) // SECS_PER_DAY)] += 1
                        self.all_cnts[dd - 1, mm - 1] += 1

        return self.xx_mesh, self.yy_mesh, self.all_cnts

    def saveCounts(self, output_file: str):
        self.all_cnts.tofile(output_file)
        return True

    def updateCounts(self, diff: int) -> tuple:
        # does the handle the case where curr_uts falls in the previous/next year
        curr_uts = int(time()) + SECS_PER_DAY * self.tz_offset
        mm_curr, dd_curr = map(int, datetime.fromtimestamp(curr_uts).strftime("%m %d").split(' '))
        self.all_cnts[dd_curr - 1, mm_curr - 1] = max(self.all_cnts[dd_curr - 1, mm_curr - 1] + diff, 0.0)
        return self.xx_mesh, self.yy_mesh, self.all_cnts

    def updateTzOffset(self, diff: int) -> None:
        self.tz_offset = max(min(self.tz_offset + diff, 1), -1)

def disp(tracker: Tracker) -> None:
    # Convert this grid to columnar data expected by Altair
    x, y, z = tracker.xx_mesh, tracker.yy_mesh, tracker.all_cnts

    source = pd.DataFrame(
        {"Day": x.ravel(),
         "Month": y.ravel(),
         "Count": z.ravel()}
    )

    custom_scale = alt.Scale(
        domain=[-2, z.max()],
        range=tracker.customColours()
    )

    c = alt.Chart(source).mark_rect().encode(
        alt.X("Day:O").axis(labelAngle=0),
        alt.Y("Month:O").axis(labelExpr="['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][datum.value - 1]"),
        color=alt.Color("Count:Q", scale=custom_scale)
    )
    st.write(c)

def dispCalcAverage(all_trackers: list, yyyy_0: int = 2024) -> None:
    # 1. User date range input
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        from_date = col_1.date_input("From", value=pd.to_datetime("2024-07-23"), min_value=pd.to_datetime("2024-07-23"), max_value=pd.to_datetime("today"))
    with col_2:
        to_date = col_2.date_input("To", value=pd.to_datetime("today"), min_value=from_date, max_value=pd.to_datetime("today"))
    with col_3:
        include_to_date = col_3.checkbox('Include "To"', value=True)

    if include_to_date:
        to_date += timedelta(days=1)

    # 2. Construct date range and prepare data
    date_range = pd.date_range(from_date, to_date - timedelta(days=1), freq='D')
    all_trackers_ascending = all_trackers[::-1]     # oldest to latest
    cnts = []

    for d in date_range:
        year_idx = d.year - yyyy_0
        if 0 <= year_idx < len(all_trackers_ascending):
            tracker = all_trackers_ascending[year_idx]
            day = d.day - 1     # 0-indexed
            month = d.month - 1
            if 0 <= day < 31 and 0 <= month < 12:
                cnt = tracker.all_cnts[day, month]
                if cnt >= 0:
                    cnts.append(cnt)

    if not cnts:
        st.warning("No valid data in selected range.")
        return

    st.write(f"Average = {np.mean(cnts).round(3)}")
    st.write(f"Standard deviation = {np.std(cnts).round(3)}")

def dispWeeklyHeatmap(tracker: Tracker, yyyy: int) -> None:
    x, y, z = tracker.xx_mesh, tracker.yy_mesh, tracker.all_cnts
    records = []

    for day, month, count in zip(x.ravel(), y.ravel(), z.ravel()):
        if count >= 0:      # exclude invalid days
            try:
                date = datetime(yyyy, month, day)
                iso_week = int(date.strftime("%V"))     # ISO week number
                weekday = date.weekday()    # 0 = Monday, 6 = Sunday
                records.append((iso_week, weekday, count))
            except ValueError:
                continue    # skip invalid date like 31 Feb

    df = pd.DataFrame(records, columns=["Week", "Day", "Count"])

    custom_scale = alt.Scale(
        domain=[0, df["Count"].max()],
        range=tracker.customColours()[3:]       # skip greys used for invalids
    )

    day_labels = ["'Mon'", "'Tue'", "'Wed'", "'Thu'", "'Fri'", "'Sat'", "'Sun'"]

    chart = alt.Chart(df).mark_rect().encode(
        x=alt.X("Day:O", title="Day", axis=alt.Axis(values=list(range(7)), labelExpr=f"[{', '.join(day_labels)}][datum.value]", labelAngle=0)),
        y=alt.Y("Week:O", title="Week"),
        color=alt.Color("Count:Q", scale=custom_scale)
    )

    st.write(chart)

def renderTab(tracker: Tracker, yyyy_0: int, mm_0: int, dd_0: int, cnts_path: str, editable: bool) -> None:
    st.title(f"Fap Tracker {yyyy_0}")

    if editable:
        cols = st.columns([1, 1, 2, 1, 1, 1])       # adjust the column ratios as needed

        with cols[0]:
            if st.button("+1"):
                tracker.updateCounts(1)

        with cols[1]:
            if st.button("-1"):
                tracker.updateCounts(-1)

        with cols[2]:
            if st.button("Save data"):
                tracker.saveCounts(cnts_path)

        with cols[3]:
            if st.button("◀", disabled=tracker.tz_offset < 0):
                tracker.updateTzOffset(-1)

        with cols[4]:
            curr_uts = int(time()) + SECS_PER_DAY * tracker.tz_offset
            mm_curr, dd_curr = datetime.fromtimestamp(curr_uts).strftime("%m, %d").split(',')
            st.write(MONTHS[mm_curr] + dd_curr)

        with cols[5]:
            if st.button("▶", disabled=tracker.tz_offset > 0):
                tracker.updateTzOffset(1)

    disp(tracker)

    dispWeeklyHeatmap(tracker, yyyy_0)

    if editable:
        with st.form("upload"):
            uploaded_file = st.file_uploader("Choose files")

            submitted = st.form_submit_button("Overwrite counts", icon='🚀')
            if uploaded_file and submitted:
                st.write(f"Saving {uploaded_file.name}...")
                bytes_data = uploaded_file.getvalue()
                with open(wa_chat_path, 'wb') as fp:
                    fp.write(bytes_data)
                st.write(f"Saved {uploaded_file.name}")

                tracker.convertRawData(wa_chat_path, cnts_path, yyyy_0, mm_0, dd_0)

# st.set_page_config(page_title="Fap Tracker")

cookies = initCookies()

# Ensure that the cookies are ready
if not cookies.ready():
    st.error("Cookies not initialised yet.")
    st.stop()

if "username" in cookies:
    if not cookies["username"]:
        st.switch_page("pages/403_forbidden.py")
else:
    st.switch_page("home.py")

SECS_PER_DAY = 86_400
MONTHS = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
files_path = "pages/common"
wa_chat_path = join(files_path, "_chat.txt")
curr_yr = int(datetime.fromtimestamp(time()).strftime("%Y"))    # may not work well around New Years' due to the Streamlit server's location
all_yrs = list(range(curr_yr, 2023, -1))
starts = [(1, 1) for _ in all_yrs]      # (month, day)
starts[-1] = (7, 23)
cnts_paths = [join(files_path, f"cnts_{yr}.txt") for yr in all_yrs]

if "trackers" not in st.session_state:
    st.session_state.trackers = [Tracker() for _ in all_yrs]

    for yr, (m, d), tracker, cnts_path in zip(all_yrs, starts, st.session_state.trackers, cnts_paths):
        # tracker.rawGetCounts(wa_chat_path, yr, m, d)
        # tracker.saveCounts(cnts_path)
        tracker.getCounts(cnts_path)

tabs = st.tabs(list(map(str, all_yrs)))

for yr, (m, d), tab, tracker, cnts_path in zip(all_yrs, starts, tabs, st.session_state.trackers, cnts_paths):
    with tab:
        renderTab(tracker, yr, m, d, cnts_path, yr == curr_yr)

dispCalcAverage(st.session_state.trackers, 2024)

st.page_link("home.py", label="Back to Home", icon='🏠')
