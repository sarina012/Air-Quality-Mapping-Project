import pandas as pd
import datetime
import folium

def parse_date_time(date_time_str):
    return datetime.datetime.strptime(date_time_str, '%m/%d/%y %H:%M')

def calculate_averages(air_quality_data):
    pm25_avg = air_quality_data['PM2.5'].mean()
    pm10_avg = air_quality_data['PM10'].mean()
    return pm25_avg, pm10_avg

def process_air_quality_data(air_quality_file, coordinates_file):
    air_quality_data = []

    with open(air_quality_file, 'r') as file:
        for line in file:
            if ',' in line and 'Date/Time' not in line:
                date_time, pm25, pm10 = line.strip().split(',')
                air_quality_data.append({'Date/Time': parse_date_time(date_time), 'PM2.5': float(pm25), 'PM10': float(pm10)})

    air_quality_df = pd.DataFrame(air_quality_data)
    coord_data = pd.read_excel(coordinates_file, engine='openpyxl')

    if len(coord_data) < 14:
        print("There are not enough coordinate points. Please ensure there are at least 14 coordinate points.")
        return

    first_coord = coord_data.iloc[0]
    m = folium.Map(location=[first_coord['Latitude'], first_coord['Longitude']], zoom_start=13)

    prev_time = None
    batch_data = []
    batch_index = 0  # Keep track of which batch we are on

    for index, row in air_quality_df.iterrows():
        time_diff = (row['Date/Time'] - prev_time).total_seconds() / 60 if prev_time else 0

        if time_diff > 2 or index == 0:  # Move to the next location every 2 minutes or at the start.
            if batch_data:
                avg_pm25, avg_pm10 = calculate_averages(pd.DataFrame(batch_data))
                coord = coord_data.iloc[batch_index % len(coord_data)]  # Loop over if index exceeds
                folium.Marker(
                    location=[coord['Latitude'], coord['Longitude']],
                    tooltip=f"Batch {batch_index}: PM2.5 = {avg_pm25:.2f}, PM10 = {avg_pm10:.2f}",
                    icon=folium.Icon(color='blue')
                ).add_to(m)
                batch_data = []  # Clear batch data for the next batch.
                batch_index += 1  # Increment batch index.

        if time_diff > 30:  # If gap is more than 30 minutes, reset the batch index.
            batch_index = 0

        batch_data.append(row)
        prev_time = row['Date/Time']

    # Process the final batch
    if batch_data:
        avg_pm25, avg_pm10 = calculate_averages(pd.DataFrame(batch_data))
        coord = coord_data.iloc[batch_index % len(coord_data)]  # Ensure we don't exceed the coordinates count.
        folium.Marker(
            location=[coord['Latitude'], coord['Longitude']],
            tooltip=f"Final Batch: PM2.5 = {avg_pm25:.2f}, PM10 = {avg_pm10:.2f}",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    m.save('air_quality_map.html')  # Save the map in a writable directory

# Example usage
process_air_quality_data('DylosLog.txt', 'coordinates.xlsx')
