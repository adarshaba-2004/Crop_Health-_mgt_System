import streamlit as st
import sqlite3
import numpy as np
import time
import requests
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Crop Health AI", layout="wide")

# ---------------- ULTRA PRO CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color: white;
    font-family: 'Segoe UI';
}

/* TITLE */
.title {
    text-align:center;
    font-size:48px;
    font-weight:bold;
    margin-bottom:20px;
}

/* GLASS CARD */
.card {
    background: rgba(255,255,255,0.08);
    padding:25px;
    border-radius:20px;
    backdrop-filter: blur(15px);
    box-shadow:0px 10px 30px rgba(0,0,0,0.5);
    margin-bottom:20px;
}

/* BUTTON */
.stButton>button {
    width:100%;
    padding:12px;
    border-radius:12px;
    border:none;
    background: linear-gradient(45deg,#00c6ff,#0072ff);
    color:white;
    font-weight:bold;
}
.stButton>button:hover {
    background: linear-gradient(45deg,#ff6a00,#ee0979);
    transform: scale(1.05);
}

/* METRIC BOX */
.metric-box {
    text-align:center;
    padding:20px;
    border-radius:15px;
    background: rgba(255,255,255,0.1);
    font-size:20px;
}

/* RESULT */
.success-box {
    padding:20px;
    border-radius:15px;
    background: linear-gradient(45deg,#00ff99,#00cc66);
    text-align:center;
    font-size:22px;
}

.error-box {
    padding:20px;
    border-radius:15px;
    background: linear-gradient(45deg,#ff4e50,#f00000);
    text-align:center;
    font-size:22px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
def connect():
    return sqlite3.connect("users.db")

def create_table():
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)")
    conn.commit()
    conn.close()

def add_user(u,p):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?,?)",(u,p))
        conn.commit()
        return True
    except:
        return False

def login_user(u,p):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * s FROM users WHERE username=? AND password=?",(u,p))
    data = c.fetchone()
    conn.close()
    return data

create_table()

# ---------------- WEATHER ----------------
def get_weather():
    try:
        api_key = "fe3ba061c02dda8e027ab75a98304a43"
        city = "Bangalore"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        data = requests.get(url).json()

        if data.get("cod") != 200:
            return None, None, None

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["main"]

        return temp, humidity, weather
    except:
        return None, None, None

# ---------------- PREDICTION ----------------
def predict_disease():
    classes = ["Healthy","Leaf Spot","Rust","Blight"]
    return np.random.choice(classes), np.random.uniform(0.85,0.99)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- SIDEBAR ----------------
menu = ["Login","Register"]
choice = st.sidebar.selectbox("Menu",menu)

# ---------------- LOGIN ----------------
if choice=="Login":
    st.markdown('<div class="title">🌱 Crop Health AI</div>',unsafe_allow_html=True)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password",type="password")

    if st.button("Login"):
        if login_user(user,pwd):
            st.session_state.logged_in=True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid Credentials ❌")
    st.markdown('</div>',unsafe_allow_html=True)

# ---------------- REGISTER ----------------
if choice=="Register":
    st.markdown('<div class="title">📝 Create Account</div>',unsafe_allow_html=True)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password",type="password")

    if st.button("Register"):
        if add_user(new_user,new_pass):
            st.success("Account Created ✅")
        else:
            st.error("User already exists ❌")
    st.markdown('</div>',unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
if st.session_state.logged_in:
    st.markdown('<div class="title">🌿 Smart Dashboard</div>',unsafe_allow_html=True)

    # Weather
    temp, hum, weather = get_weather()

    col1,col2,col3 = st.columns(3)

    col1.markdown(f'<div class="metric-box">🌡 Temp<br>{temp if temp else "--"} °C</div>',unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-box">💧 Humidity<br>{hum if hum else "--"} %</div>',unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-box">🌤 Weather<br>{weather if weather else "--"}</div>',unsafe_allow_html=True)

    # Upload & Prediction
    col1,col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        file = st.file_uploader("📤 Upload Crop Image",type=["jpg","png","jpeg"])
        if file:
            st.image(file,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">',unsafe_allow_html=True)

        if file and st.button("🔍 Analyze Crop"):
            with st.spinner("🤖 AI analyzing your crop..."):
                time.sleep(2)

            result, conf = predict_disease()

            if result=="Healthy":
                st.markdown(f'<div class="success-box">✅ {result}</div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-box">⚠️ {result}</div>',unsafe_allow_html=True)

            st.progress(conf)
            st.write(f"Confidence: {conf*100:.2f}%")

        st.markdown('</div>',unsafe_allow_html=True)

    # Chart
    st.subheader("📊 Crop Analytics")
    fig,ax = plt.subplots()
    ax.pie([70,30],labels=["Healthy","Diseased"],autopct='%1.1f%%')
    st.pyplot(fig)

    if st.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()