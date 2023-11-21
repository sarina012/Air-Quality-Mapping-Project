import csv

def text_to_csv(input_file, output_file, delimiter='\t'):
    # Open the text file for reading
    with open(input_file, 'r') as text_file:
        # Read lines from the text file
        lines = text_file.readlines()

    # Open the CSV file for writing
    with open(output_file, 'w', newline='') as csv_file:
        # Create a CSV writer with the specified delimiter
        csv_writer = csv.writer(csv_file, delimiter=delimiter)

        # Iterate through the lines in the text file
        for line in lines:
            # Split the line into values using the specified delimiter
            values = line.strip().split(delimiter)
            
            # Write the values to the CSV file
            csv_writer.writerow(values)

# Example usage
text_file_path = 'DylosLog.txt'
csv_file_path = 'output.csv'
text_to_csv(text_file_path, csv_file_path)
