from streamlit_cookies_manager import EncryptedCookieManager

def initCookies() -> EncryptedCookieManager:
	# Create a global cookie manager with a consistent prefix and password
	# cookies = EncryptedCookieManager(prefix="EiOP", password="some_secure_password")
	return EncryptedCookieManager(prefix="EiOP", password="some_secure_password")
