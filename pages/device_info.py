import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("Device Information")

# Run JavaScript to fetch device info
device_info = streamlit_js_eval(
    js_code="""
    () => ({
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        screenResolution: `${window.screen.width}x${window.screen.height}`,
        browser: (() => {
            const ua = navigator.userAgent;
            if (ua.includes("Firefox")) return "Firefox";
            if (ua.includes("Chrome") && !ua.includes("Edg")) return "Chrome";
            if (ua.includes("Safari") && !ua.includes("Chrome")) return "Safari";
            if (ua.includes("Edg")) return "Edge";
            return "Unknown";
        })()
    })
    """
)

if device_info:
    st.subheader("Your Device Info:")
    st.json(device_info)
