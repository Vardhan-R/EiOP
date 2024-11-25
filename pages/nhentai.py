from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import streamlit as st
# import streamlit.components.v1 as components
import time

# # embed streamlit docs in a streamlit app
# components.iframe("https://youtube.com", height=500)

logs_path = "pages/common/logs"

st.set_page_config(page_title="nhentai")

# st.switch_page("pages/403_forbidden.py")
# THIS SCRIPT ESSENTIALLY ENDS HERE

if "logged_in" in st.session_state:
	if not st.session_state.logged_in:
		st.switch_page("pages/403_forbidden.py")
else:
	st.switch_page("st_tst_3.py")

st.title("nhentai")

if st.button("Launch nhentai"):
	PATH = "drivers/chromedriver.exe"
	service = Service(PATH)
	driver = webdriver.Chrome(service=service)

	def urlType(url: str) -> str:
		lst = [part for part in url.split('/') if part]
		if "g" in lst:
			if lst[-2] == "g":  # https://nhentai.net/g/540042/
				return "gallery"
			if lst[-3] == "g":  # https://nhentai.net/g/540042/11/
				return "page"
		if "q" in lst:  # https://nhentai.net/search/?q=big+breasts
			return "search"
		if len(lst) in [2, 3]:  # [https://nhentai.net, https://nhentai.net/?page=2]
			if lst[1] == "nhentai.net":
				return "homepage"
		return "unknown"

	URL = "https://nhentai.net"
	driver.get(URL)

	pages_visited = []

	try:
		prev_url = driver.current_url  # Initialize with the starting URL
		prev_uts = time.time()
		pages_visited.append(f"[{str(prev_uts)}] {prev_url}")
		init_uts = str(prev_uts).split('.')[0]

		while True:
			# Check if the browser window is still open
			if len(driver.window_handles) == 0:
				print("Browser closed. Exiting program.")
				break

			# Get the current page URL
			current_url = driver.current_url

			match urlType(current_url):
				case "homepage" | "search":
					can_see = [href for link in driver.find_elements(By.TAG_NAME, "a") if (href := link.get_attribute("href"))]
					for link in can_see:
						if urlType(link) == "gallery":
							...
				case "gallery":
					...
				case _:
					...

			# Print the URL if it changes
			if current_url != prev_url:
				curr_uts = time.time()
				print(f"[{curr_uts}] Page changed to: {current_url}")
				# tm = tuple(map(int, datetime.fromtimestamp(uts).strftime("%y %m %d %H %M %S").split(' ')))
				pages_visited.append(f"[{str(curr_uts)}] {current_url}")
				prev_url = current_url
				prev_uts = curr_uts

			time.sleep(1)  # Check every second
	except Exception as e:
		print("Error occurred:", e)
	finally:
		driver.quit()

	for pg in pages_visited:
		print(pg)

	with open(f"{logs_path}/session_{init_uts}.log", 'w') as fp:
		fp.write('\n'.join(pages_visited))
