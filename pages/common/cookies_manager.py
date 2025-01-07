from streamlit_cookies_manager import EncryptedCookieManager

def initCookies(wait_iters: int = 10) -> EncryptedCookieManager:
	# Create a global cookie manager with a consistent prefix and password
	cookies = EncryptedCookieManager(prefix="EiOP", password="some_secure_password")
	for _ in range(wait_iters):
		if cookies.ready():
			break
	return cookies
