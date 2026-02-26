import streamlit as st
import folium
from streamlit_folium import st_folium
from get_ndvi import get_ndvi

st.set_page_config(layout="wide")

st.title("🌱 Satellite Plant Stress Detection System")

# Default map center
map_center = [22.7196, 75.8577]

m = folium.Map(location=map_center, zoom_start=10)

# Display map
map_data = st_folium(m, width=1200, height=600)

if map_data["last_clicked"]:

    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.write(f"📍 Selected Location: {lat}, {lon}")

    ndvi = get_ndvi(lat, lon)

    if ndvi is not None:
        st.subheader(f"NDVI Value: {ndvi}")

        # Risk Classification
        if ndvi > 0.6:
            status = "🟢 Healthy"
            color = "green"
        elif ndvi > 0.3:
            status = "🟡 Moderate Stress"
            color = "orange"
        else:
            status = "🔴 High Stress"
            color = "red"

        st.success(f"Plant Condition: {status}")

        # Add highlighted circle
        folium.Circle(
            location=[lat, lon],
            radius=500,
            color=color,
            fill=True,
            fill_color=color,
        ).add_to(m)

        st_folium(m, width=1200, height=600)
    else:
        st.error("Could not retrieve NDVI data.")