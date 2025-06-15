import streamlit as st
import speedtest
import pandas as pd
import requests
import time
import random
import pyttsx3
import threading
from datetime import datetime

# Page Config
st.set_page_config(page_title="Internet Speed Checker", page_icon="🚀", layout="centered")

# --- Styling ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f9f9f9 0%, #eaf4fc 100%);
    font-family: 'Segoe UI', sans-serif;
    color: #222;
}
.title {
    font-size: 40px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(45deg, #7928ca, #ff0080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px;
}
.metric-card {
    background-color: #ffffffdd;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}
.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #20c997;
}
.metric-label {
    font-size: 16px;
    font-weight: 500;
    color: #555;
}
div.stButton > button {
    background-image: linear-gradient(to right, #f12711, #f5af19);
    color: white !important;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    padding: 0.5em 1em;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚀 Internet Speed Checker</div>', unsafe_allow_html=True)
st.caption("Digital meter • Voice summary • Smart connection feedback • History log")

# --- Network Info Display ---
def get_network_info():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        return res.get("ip", "N/A"), res.get("org", "Unknown ISP"), f"{res.get('city', '')}, {res.get('region', '')}, {res.get('country', '')}"
    except:
        return "N/A", "N/A", "N/A"

ip, isp, loc = get_network_info()
st.markdown(f"""
<div style="background-color:#ffffffdd;padding:15px;border-radius:10px;margin-bottom:10px;">
<b>🌐 IP:</b> {ip} &nbsp;&nbsp;|&nbsp;&nbsp;
<b>🏢 ISP:</b> {isp} <br>
<b>📍 Location:</b> {loc}
</div>
""", unsafe_allow_html=True)

# --- Globals ---
result_ready = False
download = upload = ping = 0.0
result_lock = threading.Lock()

# --- Speed Test Function ---
def run_speedtest():
    global result_ready, download, upload, ping
    try:
        s = speedtest.Speedtest()
        s.get_best_server()
        d = round(s.download() / 1_000_000, 2)
        u = round(s.upload() / 1_000_000, 2)
        p = round(s.results.ping, 2)
        with result_lock:
            download, upload, ping = d, u, p
            result_ready = True
    except:
        with result_lock:
            download, upload, ping = 0.0, 0.0, 0.0
            result_ready = True

# --- Animated Meter ---
def animate_digital_display(placeholder):
    fake_speed = 40.0
    while True:
        with result_lock:
            if result_ready:
                break
        fake_speed += random.uniform(-1, 1)
        fake_speed = max(30.0, min(60.0, fake_speed))
        placeholder.markdown(f"""
        <div style="font-size:50px;font-weight:bold;text-align:center;color:#00cc96;">
            {fake_speed:.2f} Mbps
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

# --- Voice Output ---
def speak_result(download, upload, ping):
    def voice():
        summary = f"Download speed is {download} megabits, upload is {upload}, ping is {ping} milliseconds."
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(summary)
        engine.runAndWait()
    threading.Thread(target=voice).start()

# --- Feedback ---
def connection_feedback(download, upload, ping):
    if download < 5 or upload < 2:
        return "Your connection seems weak or unstable. You may encounter lags during calls or video streaming."
    elif ping > 100:
        return "Ping is quite high. Online gaming or video calls might feel laggy."
    elif download > 100 and upload > 50:
        return "Fantastic speed! You're ready for streaming, cloud backups, or smooth gaming."
    elif download > 30 and upload > 10:
        return "Solid speed for all-around use: HD video, calls, browsing—all good!"
    else:
        return "This connection works, but may struggle with high-definition streaming or multitasking."

def tech_profile(download, upload, ping):
    if download >= 100 and upload >= 50 and ping <= 20:
        return """<b>Profile:</b> Power User 🚀<br>Great for 4K streaming, cloud gaming, heavy uploads, and multiple-device multitasking."""
    elif download >= 50 and upload >= 20 and ping <= 50:
        return """<b>Profile:</b> Pro Home Office 💼<br>Excellent for Zoom, screen sharing, smart homes, and large downloads."""
    elif download >= 25 and upload >= 5:
        return """<b>Profile:</b> Everyday User 🌐<br>Ideal for browsing, casual streaming, and school or light work-from-home."""
    elif download < 10 or upload < 2:
        return """<b>Profile:</b> Limited Connection ⚠️<br>This may lag during meetings, videos, or file transfers."""
    else:
        return """<b>Profile:</b> Moderate Use 📶<br>Usable for everyday tasks, but may hit hiccups under load."""

# --- Main Test ---
if st.button("🔄 Run Speed Test"):
    result_ready = False
    placeholder = st.empty()
    st.info("📶 Testing connection…")

    threading.Thread(target=run_speedtest).start()
    animate_digital_display(placeholder)

    st.success("✅ Test Complete")
    placeholder.markdown(f"""
    <div style="font-size:50px;font-weight:bold;text-align:center;color:#00cc96;">
        {download:.2f} Mbps
    </div>
    """, unsafe_allow_html=True)

    # Results display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">📅 Download</div><div class="metric-value">{download} Mbps</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">📄 Upload</div><div class="metric-value">{upload} Mbps</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">📝 Ping</div><div class="metric-value">{ping} ms</div></div>', unsafe_allow_html=True)

    # Feedback
    feedback = connection_feedback(download, upload, ping)
    st.markdown(f"""
    <div style="text-align:center;font-size:16px;background-color:#e8f0fe;padding:15px;
    border-radius:8px;box-shadow: 0 4px 8px rgba(0,0,0,0.05); margin-top:20px;">
    💡 <b>Connection Feedback:</b><br>{feedback}
    </div>
    """, unsafe_allow_html=True)

    # Tech Profile
    profile = tech_profile(download, upload, ping)
    st.markdown(f"""
    <div style="margin-top:20px;padding:15px;border-radius:12px;
    background-color:#fff9db;border-left:6px solid #f5b700;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);font-size:16px;">
    📋 <b>Tech Profile Recommendation</b><br>{profile}
    </div>
    """, unsafe_allow_html=True)

    speak_result(download, upload, ping)

    # Save results
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {"Timestamp": now, "Download (Mbps)": download, "Upload (Mbps)": upload, "Ping (ms)": ping}
    try:
        df = pd.read_csv("speedtest_history.csv", on_bad_lines='skip')
        if not all(col in df.columns for col in row.keys()):
            df = pd.DataFrame(columns=row.keys())
    except:
        df = pd.DataFrame(columns=row.keys())
    df = pd.concat([pd.DataFrame([row]), df], ignore_index=True)
    df.to_csv("speedtest_history.csv", index=False)

# --- History Table ---
with st.expander("📜 Test History"):
    try:
        df = pd.read_csv("speedtest_history.csv", on_bad_lines='skip')
        st.dataframe(df.head(10), use_container_width=True)
    except:
        st.warning("No history found or file is corrupted.")
