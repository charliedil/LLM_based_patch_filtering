import pandas as pd

# Define the number of smaller CSV files you want
n = 5

input_file = "msr_train.csv"
# Read the large CSV file
df = pd.read_csv(input_file)

# Calculate the chunk size
chunk_size = len(df) // n

# Split and save the chunks to separate CSV files
for i in range(n):
    start_row = i * chunk_size
    # Ensure the last chunk includes all remaining rows
    end_row = None if i == n - 1 else (i + 1) * chunk_size
    chunk = df[start_row:end_row]
    chunk.to_csv(f'{input_file.split(".")[0]}_{i + 1}.csv', index=False)
