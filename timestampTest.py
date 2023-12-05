from datetime import datetime, timedelta

# Specify the file path
file_path = "DylosLog.txt"

# Initialize variables for averaging
current_hour = None
current_minute = None
records_in_interval = []
averages = []

# Open the file and iterate through the lines
with open(file_path, 'r') as file:
    for line in file:
        if 'Date/Time' in line:
            continue  # Skip lines with 'Date/Time' text

        if line.strip() and ',' in line:
            # Extract timestamp and convert to datetime object
            timestamp_str = line.split(',')[0].strip()

            try:
                timestamp = datetime.strptime(timestamp_str, "%m/%d/%y %H:%M")
            except ValueError:
                print(f"Skipping invalid timestamp: {timestamp_str}")
                continue

            # Check if the hour and minute are the same as the current interval
            if current_hour is not None and current_minute is not None and \
                    timestamp.hour == current_hour and timestamp.minute // 2 == current_minute // 2:
                records_in_interval.append(float(line.split(',')[1].strip()))  # Assuming PM2.5 is in the second column

            else:
                # Calculate average for the previous interval, if any
                if records_in_interval:
                    avg_value = sum(records_in_interval) / len(records_in_interval)
                    averages.append((timestamp.replace(minute=current_minute), avg_value))

                # Start a new interval
                current_hour = timestamp.hour
                current_minute = timestamp.minute // 2
                records_in_interval = [float(line.split(',')[1].strip())]  # Assuming PM2.5 is in the second column

# Print the averages
for timestamp, avg_value in averages:
    print(f"{timestamp.strftime('%m/%d/%y %H:%M')}, Average PM2.5: {avg_value:.2f} µg/m³")
