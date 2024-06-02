import numpy as np

def generate_distinct_colors(n):
    np.random.seed(0)
    colors = np.random.rand(n, 3)
    return colors