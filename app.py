# app.py
import streamlit as st
import pandas as pd
from satellite import get_comparison_data
from fusion import calculate_stress_score, classify_stress, get_stress_color

st.set_page_config(page_title="AgniNet Prototype", layout="wide")

st.title("🌾 AgniNet – Pre-Visual Crop Stress Detection")
st.markdown("### 24-Hour Hackathon Prototype")

st.divider()

if st.button("🔍 Analyze Field Stress"):

    day1, day7 = get_comparison_data()

    score1 = calculate_stress_score(day1["temp"], day1["ndwi"], day1["ndvi"])
    score7 = calculate_stress_score(day7["temp"], day7["ndwi"], day7["ndvi"])

    level1 = classify_stress(score1)
    level7 = classify_stress(score7)

    # ---- INDICATOR SECTION ----
    st.subheader("📊 Satellite Indicators")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📅 Day 1")
        st.write(day1)
        st.metric("Stress Score", score1)

    with col2:
        st.markdown("#### 📅 Day 7")
        st.write(day7)
        st.metric("Stress Score", score7, delta=round(score7 - score1, 3))

    st.divider()

    # ---- BAR CHART ----
    st.subheader("📈 Stress Comparison Chart")
    chart_data = pd.DataFrame({
        "Day": ["Day 1", "Day 7"],
        "Stress Score": [score1, score7]
    })
    st.bar_chart(chart_data.set_index("Day"))

    st.divider()

    # ---- CLASSIFICATION ----
    st.subheader("🧠 Stress Analysis")
    st.write(f"**Day 1:** {level1}")
    st.write(f"**Day 7:** {level7}")

    color = get_stress_color(score7)
    if color == "green":
        st.success("🟢 LOW RISK – Crop condition stable.")
    elif color == "orange":
        st.warning("🟠 MODERATE RISK – Monitor irrigation.")
    else:
        st.error("🔴 HIGH RISK – Immediate intervention required.")

    st.divider()
    st.markdown("""
    ### 💡 Innovation Insight
    AgniNet detects crop stress before visible yellowing by combining:
    - 🌡 Canopy temperature anomaly  
    - 💧 Water index reduction  
    - 🌿 Vegetation health decline  

    This allows early intervention decisions.
    """)