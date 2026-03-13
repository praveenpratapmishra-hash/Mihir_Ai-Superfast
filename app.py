import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. CONFIG & API ---
API_KEY = "AIzaSyBRJHW_2CMWzNJC0s6RO4OgacyfYPxnZ3I"
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    pass

st.set_page_config(page_title="Mihir AI", layout="centered")

# --- 2. SAKT PROFESSIONAL CSS (No Patti, Ads Fixed) ---
st.markdown("""
    <style>
    /* Sabhi faltu patti aur branding hide karo */
    header, footer, .stDeployButton, #MainMenu, #stDecoration {visibility: hidden !important; display: none !important;}
    [data-testid="stStatusWidget"], [data-testid="stToolbar"] {display: none !important;}
    div[class*="st-emotion-cache-1wb59as"], div[class*="st-emotion-cache-80989f"] {display: none !important;}
    [data-testid="stFileUploader"] section, [data-testid="stFileUploader"] label { display: none !important; }

    /* Black Theme */
    body, .main { background-color: #000000 !important; color: white !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }

    /* Input & Plus Button */
    .stChatInputContainer { border-radius: 30px !important; background: #1E1F20 !important; border: 1px solid #333 !important; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 35px !important; left: 20px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before { content: "＋"; font-size: 26px; color: #888; display: flex; align-items: center; justify-content: center; }
    
    /* 4-Grid Buttons */
    .stButton button { background-color: #1E1F20; color: white; border: 1px solid #333; border-radius: 15px; height: 85px; width: 100%; text-align: left; padding: 15px; }
    
    /* Banner Ad Box (Bottom) */
    .banner-ads { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; text-align: center; z-index: 999; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANNER ADS (Niche hamesha dikhega) ---
st.markdown('<div class="banner-ads"><script>if(window.AppCreator24){window.AppCreator24.showBanner();}</script></div>', unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if "user_name" not in st.session_state:
    st.markdown("<h1 style='color: white;'>Mihir AI</h1>", unsafe_allow_html=True)
    name = st.text_input("Dost, aapka naam?", key="name_input")
    if name:
        st.session_state.user_name = name
        st.rerun()
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0

# --- 5. UI DISPLAY (4 OPTIONS) ---
if not st.session_state.messages:
    st.markdown(f"<h1>Hi {st.session_state.user_name}</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#888;'>Main Mihir AI hoon. Kya madad karun?</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎨 Create Photo\n(AI Art & Images)"): st.session_state.temp = "Create art: "
        if st.button("🚀 Boost My Day\n(Sayari, Fun)"): st.session_state.temp = "Mihir dost, kuch mast sunao!"
    with c2:
        if st.button("🧠 Solve Anything\n(Subjects, Math)"): st.session_state.temp = "Help me solve: "
        if st.button("☸️ Kundali Reading\n(Career, PDF)"): st.session_state.temp = "Analyze my kundali."

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 6. INPUT & REWARD ADS LOGIC ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyzing image..."})
    with st.chat_message("assistant"):
        try:
            # Check 5 Photo Limit
            is_photo = any(x in (prompt or "").lower() for x in ["create", "photo", "art", "banao"])
            
            if is_photo and st.session_state.photo_count >= 5:
                st.warning("🔒 5 photos limit! 2 Reward Ads dekhein.")
                # Triggering 2 Ads
                st.components.v1.html("<script>if(window.AppCreator24){window.AppCreator24.showRewardVideo(); window.AppCreator24.showRewardVideo();}</script>", height=0)
                st.session_state.photo_count = 0 
                st.stop()

            if is_photo:
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.photo_count += 1
                st.session_state.messages.append({"role": "assistant", "content": f"Hi {st.session_state.user_name}, aapki photo taiyar hai!", "img": url})
            else:
                if up_file: res = model.generate_content([f"Help {st.session_state.user_name}: {prompt}", PIL.Image.open(up_file)])
                else: res = model.generate_content(f"You are Mihir AI, a friendly boy. Reply in Hinglish to {st.session_state.user_name}: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            pass 

st.markdown("<br><br>", unsafe_allow_html=True)
