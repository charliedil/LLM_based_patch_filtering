def split_csv_in_half(input_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
        headers = lines[0]  # Store the column headers
        total_lines = len(lines) - 1  # Exclude the header line
        half_lines = total_lines // 2

        # Split lines into two halves
        first_half = [headers] + lines[1:half_lines + 1]
        second_half = [headers] + lines[half_lines + 1:]

        # Write the first half to a new file
        with open('first_half.csv', 'w') as first_file:
            first_file.writelines(first_half)

        # Write the second half to a new file
        with open('second_half.csv', 'w') as second_file:
            second_file.writelines(second_half)

# Usage example:
split_csv_in_half('thing.csv')#CHECK BEFORE USING FOR DOWNSTREAM TASK
