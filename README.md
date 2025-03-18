



### **README.md**

# Earthquake Triangulator (Time Domain)

## 📌 Overview

This program simulates **earthquake triangulation** using **seismic station arrival times**. It places **random monitoring stations** in a 30 km radius, generates a random earthquake **between 500m and 10,000m underground**, and estimates its location using **least squares minimization** based on the time it takes for seismic waves to reach each station.

---
## See Video

〚  [Youtube Explaination Video](https://studio.youtube.com/video/QIMX9HYyIVk/edit)  〛

---

### 🔥 Features:
- **Randomly placed earthquake event** beneath the stations.
- **Seismic stations with slightly varied elevations** to improve depth accuracy.
- **Seismic wave travel time modeling**, assuming a constant velocity.
- **Random timestamp assignment** for the first receiving station.
- **Gaussian noise simulation** for realistic measurement errors.
- **Least squares estimation** to determine earthquake location.
- **3D visualization** of true and estimated earthquake locations.

---

## 📥 Installation

### **1. Clone the Repository**
```sh
git clone https://github.com/BigAltitude/Earthquakes.git
```
https://github.com/bigAltitude/Earthquakes

### **2. Install Required Libraries**
Ensure Python 3.x is installed, then install dependencies:
```sh
pip install numpy matplotlib scipy
```

---

## 🚀 Usage

Run the script with:
```sh
python earthquake_triangulator.py
```

The program will:
1. Randomly generate **7 seismic stations**.
2. Randomly determine an **earthquake location**.
3. Compute **arrival times** at each station.
4. Assign a **random real-world timestamp** to the first station.
5. Solve for the earthquake’s location using **least squares minimization**.
6. Print the **true and estimated earthquake locations**.
7. Display a **3D visualization** of the process.

### 🎯 Example Output:
```plaintext
# -*- coding: utf-8 -*-
# Program: Earthquake Triangulator (Timestamped)
# Date: 2025-03-18
# Author: S Perkins
# Company: Geo Consulting Limited
# Work: Geo-Science Engineering

First station to receive earthquake signal: Station 3
Station Arrival Times:
  Station 1: 2028-05-14 12:34:21.150
  Station 2: 2028-05-14 12:34:22.324
  Station 3: 2028-05-14 12:34:20.897  # First to detect the earthquake
  Station 4: 2028-05-14 12:34:22.776
  Station 5: 2028-05-14 12:34:23.140
  Station 6: 2028-05-14 12:34:21.800
  Station 7: 2028-05-14 12:34:24.012

True Earthquake Location:  [-10456.23,  8694.12,  -6700.56]
Estimated Location:        [-10239.77,  8587.33,  -6785.43]
Error (m):                212.56
```

---

## 📊 How It Works

### **1️⃣ Generating Seismic Stations**
- `gen_station_positions(n, rad)`: Places `n` stations in a **30 km radius**.
- Stations have **slight elevation variations** to improve depth estimation.

### **2️⃣ Simulating an Earthquake**
- `gen_true_point(rad, dmin, dmax)`: Places the earthquake randomly **between 500m and 10,000m depth**.

### **3️⃣ Calculating Seismic Travel Times**
- **Uses a constant seismic velocity (5000 m/s).**
- Computes **true travel times** to each station:
  ```python
  true_times = np.linalg.norm(stations - true_point, axis=1) / v
  ```
- The **first station to detect the signal is set to time = 0**.
- Other station times are **relative to the first station**.

### **4️⃣ Adding Realism: Time Stamping & Noise**
- The first receiving station is assigned a **random date & time**.
- Other stations get **delays based on their travel times**.
- Noise is introduced to simulate real-world sensor imperfections:
  ```python
  noise_std = 0.02  # 20 milliseconds standard deviation
  noisy_times = true_times + np.random.normal(0, noise_std, size=true_times.shape)
  ```

### **5️⃣ Estimating the Earthquake’s Location**
- **Least squares minimization** is used to find the best-fit location:
  ```python
  res_opt = least_squares(residuals_time, p0, args=(stations, measured_rel_times, v, ref_index))
  est_point = res_opt.x
  ```
- The **initial guess** is the **station centroid at -5000m depth**.

### **6️⃣ 3D Visualization**
- Displays **true and estimated earthquake locations**.
- **Stations are marked in blue**, the **true earthquake in green**, and the **estimate in red**.
- **Dashed lines** connect stations to the estimated earthquake.
- Each **line is annotated with the travel time**.

---

## 🛠 Customization

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `n` | Number of stations | `7` |
| `rad` | Maximum station distance (m) | `30000` |
| `dmin` | Minimum earthquake depth (m) | `500` |
| `dmax` | Maximum earthquake depth (m) | `10000` |
| `v` | Seismic wave speed (m/s) | `5000` |
| `noise_std` | Noise standard deviation (s) | `0.02` |

Example: To **increase station count & noise level**, modify:
```python
n = 10
noise_std = 0.05  # 50 milliseconds error
```

---

## 📈 Example 3D Visualization

The program generates a **3D interactive plot** showing:
✅ **Seismic stations (blue)**  
✅ **True earthquake location (green star)**  
✅ **Estimated location (red triangle)**  
✅ **Dashed lines between stations & estimated quake**  
✅ **Time labels on each line (in seconds)**  

---

## 📜 License
This project is **open-source** under **CC**.

---

## 💡 Future Improvements
- 🔄 **Variable wave speeds** (different layers of Earth).
- 🎛 **User input options** (manual earthquake input).
- 🔥 **Real earthquake data integration** from APIs.

---

## Need Help?
Feel free to **open an issue** or **contribute!** 🚀




---

## Need Help?
Feel free to **open an issue** or **contribute!** 🚀


