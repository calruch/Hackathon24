## Author: Calvin Ruch - 4/13/24

#!usr/bin/env python3
class log:
    def __init__(self, input_data):
        self.input_data = input_data
        
    def print_log(self):
        import re

        # Split into lines
        entries = self.input_data.strip().split('\n')

        # Prepare to write to a file
        filename = 'weatherLog.txt'

        # Open the file, clearing existing data
        with open(filename, 'w') as file:
            for entry in entries:
                # Extract the components of each entry
                match = re.match(r"(\d+) ([\w\s]+) (\w{2}) (.+)", entry)
                if match:
                    index = match.group(1)
                    city = match.group(2)
                    state = match.group(3)
                    description = match.group(4)

                    # Write formatted output to the file
                    file.write(f"{index} {city}, {state}\n")
                    file.write(f"{description}\n")
                    file.write("\n")

        print(f"Weather data has been successfully written to {filename}.")
    