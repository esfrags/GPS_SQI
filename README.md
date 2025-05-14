# GPS_SQI
### Precision Guesswork on GPS Signal Quality Inference vs RF Noise 

Inference == conclusion based on evidence and reasoning

Project divided in two main parts:

## 1. GPS Accuracy analyzer
Goal: Detect and visualize GPS anomalies from your Suunto watch—things like:
- Teleport jumps or Speed/pace spikes
- Jitter while stationary
- Zig-zags in a straight section
- Inconsistent sampling rate

Data Input: GPX or FIT files exported from your Suunto watch. Use gpxpy (for GPX) or fitparse (for FIT) in Python 

Key Metrics:
- Instantaneous pace (vs average)
- Delta distance between points
- Sampling interval (check for irregular timing)
- Direction variance (sharp angle changes in short distances)
- Optional: elevation change rate (if relevant)

Outputs: Route map with color-coded segments by GPS quality

Graphs: 
- Pace vs Time with spikes highlighted
- Distance delta histogram
- Sampling rate timeline


## 2. Signal Quality Inference via GPS Noise
Goal: Use GPS data quirks to infer where signal quality might be bad, as a kind of proxy RF analysis.

Strategy: Use GPS noise/clustering/jitter as an indirect sign of:
- Reflections (multipath)
- Obstruction (urban canyons, forest)
- Satellite visibility reduction
- Track repeated anomalies in the same locations over multiple runs
- Flag zones as “signal-hostile” (good for future route planning or cross-checking)

Optional Enhancements:
- Compare against open datasets (e.g., OpenCelliD tower locations)
- Layer in terrain/building data via GIS sources

Outputs:
- Heatmap of “GPS-noisy zones”
- Timeline of GPS noise over route
- Segment scoring: green (stable), yellow (degraded), red (bad)


## Architecture workflow:
  Suunto Run (GPX/FIT)  
          ↓  
  Parse + Clean Data (Python)  
          ↓  
  Run Analyzer:  
    - Speed spikes  
    - Jump detection  
    - Direction anomalies  
          ↓  
  Mark low-GPS-quality segments  
          ↓  
  Map output:  
    - Route trace + heatmap  
    - GPS error chart  
    - Possible signal-hostile zones  

    
## Possible Toolbox:
| Purpose     | Tool                                 |
| ----------- | ------------------------------------ |
| GPX parsing | `gpxpy`                              |
| FIT parsing | `fitparse`                           |
| Analysis    | `pandas`, `numpy`, `scipy`           |
| Maps        | `folium` or `plotly.express`         |
| Optional UI | Jupyter Notebook, or Flask dashboard |



