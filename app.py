
import streamlit as st
from pathlib import Path
from PIL import Image
from satellite import get_comparison_data
from fusion import calculate_stress_score, classify_stress, get_stress_color

st.set_page_config(
    page_title="AgniNet – Pre-Visual Crop Stress Detection",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
# 🔥 AgniNet – Pre-Visual Crop Stress Detection
**Detect crop stress 7–10 days before visible damage**
""")

col1, col2, col3 = st.columns([6,1,1])
with col2:
    login = st.button("🔑 Login")
with col3:
    register = st.button("📝 Register")

if login:
    st.info("Login clicked (demo)")

if register:
    st.info("Register clicked (demo)")

ASSETS_PATH = Path(__file__).parent / "assets"
image_path = ASSETS_PATH / "india_map.png"

try:
    india_map = Image.open(image_path)
    st.markdown("## India Crop Stress Overview")
    st.image(india_map, caption="India Crop Map", use_container_width=True)
except Exception as e:
    st.error(f"❌ Failed to load India map: {e}")

st.markdown("## 🚀 Start Analysis")

if "start_analysis" not in st.session_state:
    st.session_state.start_analysis = False
if "calculate_clicked" not in st.session_state:
    st.session_state.calculate_clicked = False

if st.button("Start Analysis"):
    st.session_state.start_analysis = True

if st.session_state.start_analysis:
    st.markdown("### Fill Crop & Location Info")
    
    crop = st.selectbox("Select Crop", ["Cotton", "Sugarcane", "Wheat", "Grapes", "Soybean"], key="crop")
    location = st.text_input("Enter Location (City/District)", key="location")
    climate = st.selectbox("Select Climate", ["Normal", "Hot", "Dry", "Humid"], key="climate")

    if st.button("Calculate Stress"):
        st.session_state.calculate_clicked = True

if st.session_state.calculate_clicked:
    current, baseline = get_comparison_data()
    score = calculate_stress_score(current['temp'], current['ndwi'], current['ndvi'])
    level = classify_stress(score)
    color = get_stress_color(score)

    st.markdown(f"### Stress Score: {score:.2f} ({level})")
    st.markdown(
        f"<div style='background-color:{color};padding:10px;color:white;'>Risk Level Indicator</div>",
        unsafe_allow_html=True
    )

    st.write("**Selected Crop:**", st.session_state.crop)
    st.write("**Location:**", st.session_state.location)
    st.write("**Climate:**", st.session_state.climate)
    st.write("**Current Data:**", current)
    st.write("**Baseline Data:**", baseline)
    st.success("✅ Analysis complete (demo data)")