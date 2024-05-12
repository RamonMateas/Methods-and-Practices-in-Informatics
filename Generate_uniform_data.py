import random

def generate_uniform_data(n, lower_bound, upper_bound):
    """
    Generates 'n' uniformly distributed numbers between 'lower_bound' and 'upper_bound'.
    
    Args:
    n (int): Number of elements to generate.
    lower_bound (int): Lower bound of the range.
    upper_bound (int): Upper bound of the range.
    
    Returns:
    list: A list containing 'n' uniformly distributed numbers.
    """
    return [random.randint(lower_bound, upper_bound) for _ in range(n)]

# Example usage: Generate 10,000 numbers uniformly distributed between 0 and 100000
uniform_data = generate_uniform_data(10000, 0, 100000)

# Optionally, you can save this data to a file if you need to use it across different sessions or platforms
with open('uniform_data.txt', 'w') as f:
    for number in uniform_data:
        f.write(f"{number}\n")
