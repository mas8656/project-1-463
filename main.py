import pandas as pd
import numpy as np

def detect_anomalies(data):
    anomalies = []
    threshold = 2  # Example threshold for anomaly detection
    for i in range(len(data) - 1):
        distance = np.abs(data['Price'][i + 1] - data['Price'][i])
        if distance > threshold:
            anomalies.append(((i + 1, data['Price'][i + 1]), (i, data['Price'][i])))
    return anomalies

def main():
    # Read the CSV file
    try:
        data = pd.read_csv('../data/stock_prices.csv', header=0)
        print("Data from CSV:", data)

        # Sort data by date if needed (assuming 'Date' is the column name)
        data = data.sort_values(by='Date')

        # Calculate the period of maximum gain
        max_gain = 0
        period = (0, 0)
        for i in range(len(data) - 1):
            gain = data['Price'][i + 1] - data['Price'][i]
            if gain > max_gain:
                max_gain = gain
                period = (i, i + 1)

        # Detect anomalies
        anomalies = detect_anomalies(data)

        # Calculate anomaly distance (if relevant)
        if anomalies:
            anomaly_distance = np.abs(anomalies[0][0][1] - anomalies[0][1][1])
        else:
            anomaly_distance = 0

        # Print the formatted report
        print("Financial Analysis Report:")
        print(f"Period of Maximum Gain: {period}")
        print(f"Maximum Gain: {max_gain}")
        print(f"Anomaly Detected: {anomalies}")
        print(f"Anomaly Distance: {anomaly_distance}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
