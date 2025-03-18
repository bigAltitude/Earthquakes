# -*- coding: utf-8 -*-
# Program: Earthquake Triangulator (Timestamped)
# Date: 2025-02-01
# Author: S Perkins
# Company: Geo Consulting Limited
# Work: Geo-Science Engineering

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
from scipy.optimize import least_squares

def gen_station_positions(n, rad):
    """Generate n stations within a circle with a small vertical wiggle."""
    stations = []
    for i in range(n):
        r = np.sqrt(np.random.rand()) * rad
        theta = np.random.rand() * 2 * np.pi
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.random.uniform(-500, 500)  # slight variation in elevation
        stations.append([x, y, z])
    return np.array(stations)

def gen_true_point(rad, dmin, dmax):
    """Randomly place a true earthquake point under the stations.
    The depth is between dmin and dmax (in meters, negative)."""
    r = np.sqrt(np.random.rand()) * rad
    theta = np.random.rand() * 2 * np.pi
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = -np.random.uniform(dmin, dmax)
    return np.array([x, y, z])

def residuals_time(p, stations, rel_times, v, ref_index):
    """For candidate point p, compute the predicted travel times
    to each station, subtract the reference station travel time,
    and return the differences with measured relative times."""
    t_pred = np.linalg.norm(stations - p, axis=1) / v
    t_rel_pred = t_pred - t_pred[ref_index]
    return t_rel_pred - rel_times

def generate_random_datetime():
    """Generate a random date and time for the first station's timestamp."""
    year = np.random.randint(2000, 2030)  # Random year between 2000 and 2030
    month = np.random.randint(1, 13)  # Random month
    day = np.random.randint(1, 29)  # Keep it simple to avoid month length issues
    hour = np.random.randint(0, 24)
    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)
    
    return datetime(year, month, day, hour, minute, second)

def main():
    print("# -*- coding: utf-8 -*-")
    print("# Program: Earthquake Triangulator (Timestamped)")
    print("# Date: " + datetime.now().strftime("%Y-%m-%d"))
    print("# Author: S Perkins")
    print("# Company: Geo Consulting Limited")
    print("# Work: Geo-Science Engineering")
    print("Let's timestamp some earthquake arrivals!\n")
    
    np.random.seed()  # True randomness
    
    n = 7          # Number of stations
    rad = 30000    # 30 km radius for station placement
    dmin = 500     # Minimum depth (m)
    dmax = 10000   # Maximum depth (m)
    v = 5000       # Wave speed (m/s)
    
    # Generate station positions and a true earthquake point.
    stations = gen_station_positions(n, rad)
    true_point = gen_true_point(rad, dmin, dmax)
    
    # Compute the "true" travel times (in seconds) for each station.
    true_times = np.linalg.norm(stations - true_point, axis=1) / v
    # The station with the minimum travel time receives the signal at t=0.
    ref_index = np.argmin(true_times)
    
    # measured_rel_times = true_times - true_times[ref_index]

    noise_std = 0.01  # Standard deviation of noise in seconds (adjust as needed)
    noisy_times = true_times + np.random.normal(0, noise_std, size=true_times.shape)
    measured_rel_times = noisy_times - noisy_times[ref_index]
    
    
    # Assign a random absolute timestamp to the first receiving station.
    base_time = generate_random_datetime()
    station_times = [base_time + timedelta(seconds=t) for t in measured_rel_times]
    
    print(f"First station to receive earthquake signal: Station {ref_index + 1}")
    print("Station Arrival Times:")
    for i, t in enumerate(station_times):
        print(f"  Station {i + 1}: {t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")  # Millisecond precision

    # Initial guess: use the centroid for (x,y) and -5000 m for depth.
    centroid = np.mean(stations, axis=0)
    p0 = np.array([centroid[0], centroid[1], -5000])
    
    # Solve for the earthquake location using least squares.
    res_opt = least_squares(residuals_time, p0, 
                            args=(stations, measured_rel_times, v, ref_index))
    est_point = res_opt.x
    
    print("\nTrue Earthquake Location: ", true_point)
    print("Estimated Location:       ", est_point)
    error = np.linalg.norm(true_point - est_point)
    print("Error (m):               ", error)
    
    # Plotting the result.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot stations, true point, and estimated point.
    ax.scatter(stations[:,0], stations[:,1], stations[:,2],
               c='blue', label='Stations')
    ax.scatter(true_point[0], true_point[1], true_point[2],
               c='green', marker='*', s=150, label='True Earthquake')
    ax.scatter(est_point[0], est_point[1], est_point[2],
               c='red', marker='^', s=150, label='Estimated Earthquake')
    
    # Draw lines from each station to the estimated point.
    for i, s in enumerate(stations):
        line_x = [s[0], est_point[0]]
        line_y = [s[1], est_point[1]]
        line_z = [s[2], est_point[2]]
        ax.plot(line_x, line_y, line_z, c='gray', ls='--', lw=1)
        # Calculate travel time from estimated point to station.
        t_est = np.linalg.norm(s - est_point) / v
        # Annotate the midpoint of the line with the travel time in seconds.
        mid_x = (s[0] + est_point[0]) / 2
        mid_y = (s[1] + est_point[1]) / 2
        mid_z = (s[2] + est_point[2]) / 2
        ax.text(mid_x, mid_y, mid_z, f"{t_est:.3f}s",
                size=8, color='purple')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Earthquake Triangulation (Timestamped)')
    ax.legend()
    
    # Ensure the z-axis always shows down to -10000 m.
    ax.set_zlim(-10000, 100)
    
    plt.show()

if __name__ == '__main__':
    main()
