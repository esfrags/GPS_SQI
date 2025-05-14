import gpxpy
import pandas as pd

def analyze_gpx(filepath):
    with open(filepath, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

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

    # Rough distance calc using Haversine
    from math import radians, cos, sin, asin, sqrt

    def haversine(lat1, lon1, lat2, lon2):
        if pd.isna(lat2) or pd.isna(lon2):
            return 0
        R = 6371e3  # Earth radius in meters
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    df['delta_dist'] = df.apply(lambda row: haversine(
        row['lat'], row['lon'], row['lat_shifted'], row['lon_shifted']), axis=1)
    df['speed_mps'] = df['delta_dist'] / df['delta_time'].replace(0, 1)

    # Detect anomalies
    df['spike'] = df['speed_mps'] > 6  # e.g., >21.6 km/h
    spike_points = df[df['spike']][['lat', 'lon', 'speed_mps']]

    return {
        "num_points": len(df),
        "num_spikes": len(spike_points),
        "spike_points": spike_points.to_dict(orient='records'),
        "full_data": df.to_dict(orient='records')
    }
