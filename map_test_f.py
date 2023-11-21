import pandas as pd
import folium

def map():


    # Load the CSV data into a DataFrame
    data = pd.read_excel('output.xlsx',engine='openpyxl')

    # Initialize a map centered around a location (this example uses the latitude and longitude of the first measurement)
    m = folium.Map(location=[data.iloc[0]['Latitude'], data.iloc[0]['Longitude']], zoom_start=13)

    # Add air quality measurements to the map
    for index, row in data.iterrows():
        color = 'green'  # Default color

        # Change the marker color based on air quality (this is a simple example)
        if row['Air Quality Measurement'] > 10:  # Adjust this threshold as needed
            color = 'red'
        elif row['Air Quality Measurement'] > 20:
            color = 'orange'
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=f"Air Quality: {row['Air Quality Measurement']}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Save the map to an HTML file
    m.save('air_quality_map.html')