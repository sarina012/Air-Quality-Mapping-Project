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

    if coord_data.empty:
        print("The coordinates data is empty. Please check your Excel file.")
        return

    first_coord = coord_data.iloc[0]
    m = folium.Map(location=[first_coord['Latitude'], first_coord['Longitude']], zoom_start=13)

    prev_time = None
    batch_data = []
    batch_index = 0

    for index, row in air_quality_df.iterrows():
        if prev_time and (row['Date/Time'] - prev_time).total_seconds() > 120:
            # Time gap detected, process the current batch
            if batch_data:
                avg_pm25, avg_pm10 = calculate_averages(pd.DataFrame(batch_data))
                coord = coord_data.iloc[batch_index % len(coord_data)]
                folium.Marker(
                    location=[coord['Latitude'], coord['Longitude']],
                    tooltip=f"Batch {batch_index}: PM2.5 = {avg_pm25:.2f}, PM10 = {avg_pm10:.2f}",
                    icon=folium.Icon(color='blue')
                ).add_to(m)
                batch_data = []  # Start new batch
                batch_index += 1

            # If the gap is greater than 1 hour, reset the batch index
            if (row['Date/Time'] - prev_time).total_seconds() > 3600:
                batch_index = 0

        batch_data.append(row)
        prev_time = row['Date/Time']

    if batch_data:
        avg_pm25, avg_pm10 = calculate_averages(pd.DataFrame(batch_data))
        coord = coord_data.iloc[batch_index % len(coord_data)]
        folium.Marker(
            location=[coord['Latitude'], coord['Longitude']],
            tooltip=f"Final Batch: PM2.5 = {avg_pm25:.2f}, PM10 = {avg_pm10:.2f}",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    m.save('air_quality_map.html')

# Example usage
process_air_quality_data('DylosLog.txt', 'coordinates.xlsx')
