# Note : The api_url mentioned below is the fake url. We have to parse it with tthe actual url

import requests
import math

# 1. Fetching Data from an API
def data_stream_from_api(api_url):
    response = requests.get(api_url)  # Fetch data from the API
    data = response.json()  # Parse JSON data
    return data['data']  # Extract the 'data' field from the response

# 2. Anomaly Detection Using Simple Moving Average (SMA)
# Assuming the constant window_size of 50 and threshold value as 3
def detect_anomaly(data_stream, window_size=50, threshold=3):
    window = []
    anomalies = []
    
    for idx in range(len(data_stream)):
        data = data_stream[idx]
        
        if len(window) == window_size: 
            mean = sum(window) / window_size
            variance = sum((x - mean) ** 2 for x in window) / window_size
            std_dev = math.sqrt(variance)
            
            if std_dev > 0:
                z_score = (data - mean) / std_dev
                if abs(z_score) > threshold:
                    anomalies.append((idx, data))
        
        if len(window) < window_size:
            window.append(data)
        else:
            window.pop(0)
            window.append(data)
    
    return anomalies

# 3. Simple ASCII Visualization 
# Data Points are represented by * while any anomaly is marked with X so that it stands out.
def visualize_data(data_stream, anomalies):
    max_value = max(data_stream)
    min_value = min(data_stream)
    height = 20

    def scale_data(data):
        return int((data - min_value) / (max_value - min_value) * height)

    for idx, data in enumerate(data_stream):
        scaled_value = scale_data(data)
        line = [' '] * (height + 1)
        line[scaled_value] = '*'
        
        if idx in [a[0] for a in anomalies]:
            line[scaled_value] = 'X'
        
        print(''.join(line[::-1]))

# 4. Main flow starts
if __name__ == "__main__":
    api_url = 'https://example.com/data'  # Replace with actual API URL
    data_stream = data_stream_from_api(api_url)  # Fetch data from API
    anomalies = detect_anomaly(data_stream)  # Detect anomalies
    visualize_data(data_stream, anomalies)  # Visualize data
