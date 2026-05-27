import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from pesticide_info import pesticide_info

# --- Firebase Login/Signup Code (Corrected) ---

import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

if "user" not in st.session_state:
    st.session_state.user = None

if "show_treatment" not in st.session_state:
    st.session_state.show_treatment = False

# --- Modern Login/Signup Styling ---
def apply_auth_styles():
    st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Auth container styling */
    .auth-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Title styling */
    .auth-title {
        text-align: center;
        color: #2d3748;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .auth-subtitle {
        text-align: center;
        color: #718096;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Secondary button */
    .secondary-btn {
        background: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        box-shadow: none !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def login_ui():
    apply_auth_styles()
    
    st.markdown("""
    <div class="auth-container">
        <h1 class="auth-title">🌾 Plant Disease Detection & treatment Advisor</h1>
        <p class="auth-subtitle">Sign in to access your plant disease detection tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("📧 Email Address", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Login", use_container_width=True, key="login_btn", type="primary"):
            if email and password:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state.user = user
                    st.success("✅ Login Successful! Redirecting...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Invalid email or password. Please try again.")
            else:
                st.warning("⚠️ Please fill in all fields")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📝 Create New Account", use_container_width=True, key="signup_btn", type="primary"):
            st.session_state["show_signup"] = True
            st.rerun()

def signup_ui():
    apply_auth_styles()
    
    st.markdown("""
    <div class="auth-container">
        <h1 class="auth-title">🌱 Create Account</h1>
        <p class="auth-subtitle">Join us to protect your crops with AI-powered disease detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("📧 Email Address", placeholder="Enter your email")
        password = st.text_input("🔒 Create Password", type="password", placeholder="Minimum 6 characters", help="Password must be at least 6 characters long")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ Sign Up", use_container_width=True, key="signup_submit"):
            if email and password:
                if len(password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                else:
                    try:
                        auth.create_user_with_email_and_password(email, password)
                        st.success("✅ Account Created Successfully! Please login.")
                        st.session_state["show_signup"] = False
                        st.rerun()
                    except Exception as e:
                        error_msg = str(e)
                        if "EMAIL_EXISTS" in error_msg:
                            st.error("❌ This email is already registered. Please login instead.")
                        else:
                            st.error("❌ Signup failed. Please try again.")
            else:
                st.warning("⚠️ Please fill in all fields")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("← Back to Login", use_container_width=True, key="back_login"):
            st.session_state["show_signup"] = False
            st.rerun()

# ✅ Show login UI only if user is not logged in
if st.session_state.user is None:
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    if st.session_state.show_signup:
        signup_ui()
    else:
        login_ui()

    st.stop()   # <-- This is the key line (do not remove)

# --- User Logged In, Show Main App ---

# Apply main app styles
st.markdown("""
<style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(180deg, #f0f9f4 0%, #e8f5e9 50%, #f1f8e9 100%);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d5016 0%, #1a3009 100%);
    }
    
    /* Card Styling */
    .result-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #4caf50;
    }
    
    .treatment-card {
        background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #ff9800;
    }
    
    .info-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 15px 0;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 42px;
        text-align: center;
        background: linear-gradient(135deg, #2d5016 0%, #4caf50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #558b2f;
        font-size: 20px;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 12px;
        padding: 14px 28px;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Upload Area Styling */
    .upload-area {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border: 3px dashed #4caf50;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Confidence Badge */
    .confidence-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 16px;
    }
    
    .confidence-high {
        background: #4caf50;
        color: white;
    }
    
    .confidence-medium {
        background: #ff9800;
        color: white;
    }
    
    .confidence-low {
        background: #f44336;
        color: white;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Section Headers */
    .section-header {
        font-size: 24px;
        color: #2d5016;
        font-weight: 700;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with user info
with st.sidebar:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2d5016 0%, #4caf50 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='color: white; text-align: center; margin: 0;'>👤 User Profile</h3>
    </div>
    """, unsafe_allow_html=True)
    st.success("✅ Logged In")
    st.info(f"📧 {st.session_state.user['email']}")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.selected_class = None
        st.session_state.confidence = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📋 Quick Guide")
    st.markdown("""
    1. 📸 Upload a clear leaf image
    2. 🔍 Click 'Detect Disease'
    3. 💊 Get treatment recommendations
    4. 🌾 Follow the pesticide guidelines
    """)

# ----------------- Load model and class names -----------------
with open("class_names.txt", "r", encoding="utf-8", errors="ignore") as f:
    class_names = [line.strip() for line in f.readlines()]

from tensorflow.keras.models import load_model
@st.cache_resource
def load_model_file():
    model = load_model("plant_disease_model.keras", compile=False)
    return model

model = load_model_file()

# ---------------- Header Section ----------------
st.markdown("<h1 class='main-title'>🌾 Plant Disease Detection & Pesticide Advisor</h1>", unsafe_allow_html=True)
# st.markdown("<p class='subtitle'>AI-Powered Crop Protection for Modern Farmers</p>", unsafe_allow_html=True)

# ---------------- Upload Section ----------------
st.markdown("<h3 class='section-header'>📤 Upload Leaf Image</h3>", unsafe_allow_html=True)
st.markdown("""
<div style='background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;'>
    <p style='color: #666; text-align: center; margin: 0;'>
        <strong>📷 Tips for Best Results:</strong> Use good lighting, focus on the leaf, and ensure the image is clear and not blurry.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_image = st.file_uploader("Choose an image file", type=["jpg","jpeg","png"], help="Upload a clear image of the plant leaf")

# ---------------- Prediction function ----------------
def predict_disease(image):
    # IMPORTANT: use the same size you trained with (you used 128x128)
    image = image.resize((128, 128))
    img_array = img_to_array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array, verbose=0)
    class_index = int(np.argmax(predictions))
    class_label = class_names[class_index]
    confidence = float(np.max(predictions) * 100)
    return class_label, confidence

def get_confidence_class(confidence):
    if confidence >= 80:
        return "confidence-high"
    elif confidence >= 60:
        return "confidence-medium"
    else:
        return "confidence-low"

# ---------------- Display / Buttons ----------------
if uploaded_image:
    st.markdown("<h3 class='section-header'>🖼️ Your Image</h3>", unsafe_allow_html=True)
    image = Image.open(uploaded_image).convert("RGB")
    # Center the image with a suitable size for human viewing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, width=450)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detect button - vertically stacked
    if st.button("🔍 Detect Disease", use_container_width=True, type="primary"):
        with st.spinner("🤖 AI is analyzing your image... Please wait..."):
            predicted_class, confidence = predict_disease(image)
            st.session_state.selected_class = predicted_class
            st.session_state.confidence = confidence
            st.rerun()

    # Show detection result if it exists in session
    if "selected_class" in st.session_state and st.session_state.selected_class:
        st.markdown("---")
        disease_name = st.session_state.selected_class.replace('_', ' ').title()
        confidence = st.session_state.confidence
        conf_class = get_confidence_class(confidence)
        
        st.markdown(f"""
        <div class="result-card">
            <h2 style='color: #2d5016; margin-top: 0;'>🌿 Disease Detected</h2>
            <h3 style='color: #4caf50; font-size: 28px; margin: 10px 0;'>{disease_name}</h3>
            <p style='font-size: 18px; margin: 15px 0;'>
                <strong>Model Confidence:</strong> 
                <span class="confidence-badge {conf_class}">{confidence:.1f}%</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
                # Recommended Treatment button - vertically stacked
        if st.button("💊 Recommended Treatment", use_container_width=True, type="primary"):
            st.session_state.show_treatment = True
            st.rerun()
        
        # Only show treatment details after button click
        if st.session_state.get("show_treatment", False):
            selected_class = st.session_state.selected_class
            info = pesticide_info.get(selected_class, None)
            
            if info:
                pesticide = info.get('pesticide', 'Not Available')
                dosage = info.get('dosage', 'Not Available')
                recommendation = info.get('recommendation', 'Not Available')
                
                st.markdown(f"""
                <div class="treatment-card">
                    <h2 style='color: #e65100; margin-top: 0;'>💊 Recommended Treatment</h2>
                    <div style='background: white; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                        <h4 style='color: #2d5016; margin-top: 0;'>🧪 Pesticide:</h4>
                        <p style='font-size: 18px; color: #424242; margin: 10px 0;'><strong>{pesticide}</strong></p>
                    </div>
                    <div style='background: white; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                        <h4 style='color: #2d5016; margin-top: 0;'>📏 Dosage:</h4>
                        <p style='font-size: 18px; color: #424242; margin: 10px 0;'><strong>{dosage}</strong></p>
                    </div>
                    <div style='background: white; padding: 20px; border-radius: 10px; margin: 15px 0;'>
                        <h4 style='color: #2d5016; margin-top: 0;'>📋 Application Guidelines:</h4>
                        <p style='font-size: 16px; color: #424242; margin: 10px 0; white-space: pre-line;'>{recommendation}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
    