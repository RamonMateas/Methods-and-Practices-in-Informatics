import csv
import os
import time


# Read Write data

def read_data_from_csv(file_path, column_index):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = [row for row in reader if row]
    return header, data

def write_data_to_csv(header, data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


# Radix Sort Implementation

import math

def radix_sort(data, column_index):
    try:
        # Find the maximum number to figure out the number of digits
        max_num = max(abs(float(row[column_index])) for row in data)
        
        # Handle negative numbers by offsetting all numbers so that the minimum number starts from zero
        min_num = min(float(row[column_index]) for row in data)
        offset = -min_num if min_num < 0 else 0

        # Calculate the number of digits in the largest number
        max_digits = math.floor(math.log10(max_num)) + 1 if max_num > 0 else 1

        exp = 1
        for _ in range(max_digits):
            helper_counting_sort(data, exp, column_index, offset)
            exp *= 10
    except OverflowError as e:
        
        print(f"OverflowError occurred in radix_sort at exp={exp}, max_num={max_num}")
        raise e 

def helper_counting_sort(data, exp, column_index, offset):
    n = len(data)
    output = [None] * n  
    count = [0] * 10     
    
    
    for i in range(n):
        index = int((float(data[i][column_index]) + offset) / exp) % 10
        count[index] += 1

    # Change count[i] so it contains the actual position of this digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    
    i = n - 1
    while i >= 0:
        index = int((float(data[i][column_index]) + offset) / exp) % 10
        output[count[index] - 1] = data[i]
        count[index] -= 1
        i -= 1

    
    for i in range(n):
        data[i] = output[i]





# TimSort Implementation

MIN_MERGE = 32

def calc_min_run(n):
    
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort(arr, left, right, column_index):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and float(arr[j][column_index]) > float(temp[column_index]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

def merge(arr, l, m, r, column_index):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(len1):
        left.append(arr[l + i])
    for i in range(len2):
        right.append(arr[m + 1 + i])

    i = j = 0
    k = l

    while i < len1 and j < len2:
        if float(left[i][column_index]) <= float(right[j][column_index]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = right[j]
        j += 1
        k += 1

def timsort(arr, column_index):
    n = len(arr)
    min_run = calc_min_run(n)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end, column_index)

    size = min_run
    while size < n:
        for left in range(0, n, size * 2):
            mid = min(n - 1, left + size - 1)
            right = min(n - 1, left + 2 * size - 1)
            if mid < right:
                merge(arr, left, mid, right, column_index)
        size *= 2


# ShellSort Implementation

def shell_sort(arr, column_index):
    n = len(arr)
    # Generate Sedgewick's increment sequence
    gaps = []
    i = 0
    while True:
        if i % 2 == 0:
            gap = 9 * (2 ** i - 2 ** (i // 2)) + 1
        else:
            gap = 8 * 2 ** i - 6 * 2 ** ((i + 1) // 2) + 1
        if gap > n:
            break
        gaps.append(gap)
        i += 1
    gaps.reverse()  # Reverse to start with the largest gap

    # Perform a gap insertion sort for each gap size in the Sedgewick sequence
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Shift earlier gap-sorted elements up until the correct location for a[i] is found
            while j >= gap and float(arr[j - gap][column_index]) > float(temp[column_index]):
                arr[j] = arr[j - gap]
                j -= gap
            # Put temp (the original a[i]) in its correct location
            arr[j] = temp


# CountingSort Implementation

def counting_sort(arr, column_index):
    
    max_value = float(max(arr, key=lambda x: float(x[column_index]))[column_index])
    min_value = float(min(arr, key=lambda x: float(x[column_index]))[column_index])
    range_of_elements = int(max_value - min_value + 1)

    count = [0] * range_of_elements
    output = [0] * len(arr)

    # Count each occurrence
    for i in range(len(arr)):
        index = int(float(arr[i][column_index]) - min_value) 
        count[index] += 1

    for i in range(1, range_of_elements):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        index = int(float(arr[i][column_index]) - min_value)
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    for i in range(len(arr)):
        arr[i] = output[i]


# Benchmark Implementation

def benchmark_sorting_algorithms(files_info):
    results = {}
    for filename, column_index in files_info:
        header, data = read_data_from_csv(filename, column_index)
        algorithms = [radix_sort, shell_sort, counting_sort, timsort]
        results[filename] = {}
        for algorithm in algorithms:
            start_time = time.time()
            algorithm(data.copy(), column_index) 
            elapsed_time = time.time() - start_time
            results[filename][algorithm.__name__] = elapsed_time
    return results


# Benchmarking

# Format: ("input path",column_index)
files_info = [
    ("D:/Info/1st Year/2nd Semester/Methods and Practices/Datasets/Uniform_Data.csv", 0),
    ("D:/Info/1st Year/2nd Semester/Methods and Practices/Datasets/Reversed_Data.csv", 0),
    ("D:/Info/1st Year/2nd Semester/Methods and Practices/Datasets/Adult_Data_Duplicates.csv", 10),
    ("D:/Info/1st Year/2nd Semester/Methods and Practices/Datasets/Bank_Data_Partially_Sorted.csv", 5),
    ("D:/Info/1st Year/2nd Semester/Methods and Practices/Datasets/Wine_Data_Limited_Range.csv", 10),
    ("D:/Info/1st Year/2nd Semester/Methods and Practices/Datasets/Flight_Data_Large.csv", 14),
]


results = benchmark_sorting_algorithms(files_info)

for file, timings in results.items():
    print(f"Timings for {file}:")
    for sort_name, timing in timings.items():
        print(f"{sort_name}: {timing:.6f} seconds")
