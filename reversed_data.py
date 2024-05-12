import random

# Generate a list of 10,000 random numbers
data = [random.randint(0, 100000) for _ in range(10000)]

# Sort the data in ascending order
data_sorted = sorted(data)

# Reverse the sorted data
data_reversed = data_sorted[::-1]

# Write the reversed data to a file
with open('reversed_data.txt', 'w') as f:
    for number in data_reversed:
        f.write(f"{number}\n")
