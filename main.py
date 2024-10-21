import pandas as pd
import numpy as np

# Sample stock price data (embedded in the script)
stock_data = [
    {"Date": "2024-01-01", "Price": 100},
    {"Date": "2024-01-02", "Price": 105},
    {"Date": "2024-01-03", "Price": 102},
    {"Date": "2024-01-04", "Price": 110},
    {"Date": "2024-01-05", "Price": 109},
    {"Date": "2024-01-06", "Price": 101},
    {"Date": "2024-01-07", "Price": 99},
    {"Date": "2024-01-08", "Price": 103}
]

# Merge Sort Function (Assuming sorting by 'Date' is needed)
def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, key)
        merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i][key] < R[j][key]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

# Function to find the maximum subarray gain (Kadane's Algorithm)
def max_subarray(prices):
    max_gain = 0
    current_gain = 0
    start = end = 0
    temp_start = 0

    for i in range(1, len(prices)):
        gain = prices[i] - prices[i - 1]
        if current_gain + gain > 0:
            current_gain += gain
            if current_gain > max_gain:
                max_gain = current_gain
                start = temp_start
                end = i
        else:
            current_gain = 0
            temp_start = i

    return max_gain, start, end

# Anomaly detection using a simple distance-based approach
def detect_anomalies(data, threshold=2):
    anomalies = []
    for i in range(len(data) - 1):
        distance = np.abs(data['Price'].iloc[i + 1] - data['Price'].iloc[i])
        if distance > threshold:
            anomalies.append(((i + 1, data['Price'].iloc[i + 1]), (i, data['Price'].iloc[i])))
    return anomalies

# Report generation with formatted output for anomalies
def generate_report(period, max_gain, anomalies, anomaly_distance):
    print("\nFinancial Analysis Report:")
    print(f"Period of Maximum Gain: {period}")
    print(f"Maximum Gain: {max_gain}")
    if anomalies:
        formatted_anomalies = ', '.join([f"(({a[0][0]}, {a[0][1]}), ({a[1][0]}, {a[1][1]}))" for a in anomalies])
        print(f"Anomaly Detected: {formatted_anomalies}")
        print(f"Anomaly Distance: {anomaly_distance:.13f}")
    else:
        print("Anomaly Detected: None")
        print("Anomaly Distance: N/A")

# Main function to execute the analysis
def main():
    try:
        # Convert embedded data to a DataFrame
        data = pd.DataFrame(stock_data)
        print("Data from CSV:", data)

        # Convert DataFrame to list of dicts for merge sort
        data_list = data.to_dict('records')
        sorted_data = merge_sort(data_list, 'Date')

        # Convert sorted data back to DataFrame
        sorted_df = pd.DataFrame(sorted_data)

        # Extract prices from sorted data for max subarray analysis
        prices = sorted_df['Price'].tolist()
        max_gain, start, end = max_subarray(prices)
        period = (start, end)

        # Detect anomalies
        anomalies = detect_anomalies(sorted_df)
        anomaly_distance = 0
        if anomalies:
            # Calculate the distance of the first detected anomaly
            anomaly_distance = np.abs(anomalies[0][0][1] - anomalies[0][1][1])

        # Generate the report with updated formatting
        generate_report(period, max_gain, anomalies, anomaly_distance)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
