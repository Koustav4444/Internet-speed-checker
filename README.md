# Internet-speed-checker
Streamlit app to test internet speed with animated meter, voice feedback &amp; history.
🚀 Internet Speed Checker (Streamlit App)
A modern, responsive internet speed test app built with Streamlit, featuring:
🔄 Real-time digital speed animation
🎤 Voice summary of speed results
🌐 IP address, ISP, and location display
📊 Download, Upload & Ping metrics
💡 Smart connection feedback and user profile
🕓 Auto-logged test history (CSV-based)
🎨 Polished and mobile-friendly UI/UX

🔧 Features
Accurate speed test using speedtest-cli
Smooth animated meter while test runs
Voice feedback using pyttsx3
Location and ISP details via ipinfo.io
AI-style connection profiling (e.g., Power User, Mobile User)
CSV test history and quick data recall
Built with love using Python & Streamlit

📦 Installation
pip install -r requirements.txt

▶️ Run the App

streamlit run app.py
Then open http://localhost:8501 in your browser.

🌐 Deploy Online (Streamlit Cloud)


📁 Project Structure

InternetSpeedChecker/
├── app.py                # Main Streamlit App
├── requirements.txt      # Python dependencies
└── speedtest_history.csv # Auto-generated test history

🛠 Built With
Python 3.x
Streamlit
speedtest-cli
pandas
requests
pyttsx3

🧠 Author
Crafted with ❤️ by Koustav Dutta.
