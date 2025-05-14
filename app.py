import streamlit as st
import gpxpy
import pandas as pd
import folium
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt

st.set_page_config(layout="wide")
st.title("🏃‍♂️ GPS Analyzer & Signal Inference Tool")

uploaded_file = st.file_uploader("Upload a GPX file from your watch", type="gpx")

def haversine(lat1, lon1, lat2, lon2):
    if pd.isna(lat2) or pd.isna(lon2):
        return 0
    R = 6371e3
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

if uploaded_file:
    gpx = gpxpy.parse(uploaded_file)
    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'time': point.time,
                    'lat': point.latitude,
                    'lon': point.longitude,
                    'ele': point.elevation
                })

    df = pd.DataFrame(points)
    df['time'] = pd.to_datetime(df['time'])
    df['delta_time'] = df['time'].diff().dt.total_seconds()
    df['lat_shifted'] = df['lat'].shift()
    df['lon_shifted'] = df['lon'].shift()
    df['delta_dist'] = df.apply(lambda row: haversine(
        row['lat'], row['lon'], row['lat_shifted'], row['lon_shifted']), axis=1)
    df['speed_mps'] = df['delta_dist'] / df['delta_time'].replace(0, 1)
    df['spike'] = df['speed_mps'] > 6

    st.subheader("📊 Summary")
    st.write(f"Total GPS points: {len(df)}")
    st.write(f"Speed anomalies detected: {df['spike'].sum()}")

    st.subheader("🌍 Map")
    start_coords = [df['lat'].iloc[0], df['lon'].iloc[0]]
    m = folium.Map(location=start_coords, zoom_start=15)

    for i, row in df.iterrows():
        color = "red" if row["spike"] else "blue"
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=2,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
        ).add_to(m)

    folium_static(m)

    st.subheader("🧬 Raw GPS Data with Analysis")
    st.dataframe(df[['time', 'lat', 'lon', 'delta_dist', 'speed_mps', 'spike']])
