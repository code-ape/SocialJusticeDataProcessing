import json

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

import settings
import tools

def main():
    process_fac_staff_data()

def process_fac_staff_data():
    data = load_fac_staff_data()


def load_fac_staff_data():
    data = None
    with open(settings.fac_staff_clean_path, "r") as f:
        data = json.loads(f.read())
    return data



def test():
    # Generate fake data
    x = np.random.normal(size=1000)
    y = x * 3 + np.random.normal(size=1000)

    # Calculate the point density
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=100, edgecolor='')


    plt.show()


if __name__ == "__main__":
    print("Starting run_stats.py")
    main()
    print("Ending run_stats.py")
