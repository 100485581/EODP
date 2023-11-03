## 6.1.5. Pass/fail criteria

from common.io.writeToa import readToa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from config import globalConfig
from config.l1bConfig import l1bConfig

# Check for all bands that the differences with respect to the output TOA (l1b_toa_) are <0.01% for at
# least 3-sigma of the points.
bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
Lau_toa_path = r"C:\LAU\EODP_TER\EODP-TS-ISM\OutputsLaura"
luss_toa_path = r"C:\LAU\EODP_TER\EODP-TS-ISM\output"
l1b_toa = 'l1c_toa_'

#Check for all bands that the differences with respect to the output TOA are <0.01% for 3-sigma of the points.

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, l1b_toa + band + '.nc')

    # 2. Read your outputs (Laura's)
    Lau_toa = readToa(Lau_toa_path, l1b_toa + band + '.nc')

    # 3. Comparison
    difference = np.sort(Lau_toa) - np.sort(luss_toa)
    percentage = difference / Lau_toa * 100
    df = pd.DataFrame(percentage)
    percentage_df = df.fillna(0) # The division per zero gives some annoying NaN values
    boolean_comparison = np.array(percentage_df < 0.01)

    # Calculation of the total number of values for every matrix
    total_values = boolean_comparison.size
    trues_matrix = np.full(boolean_comparison.shape, True)
    # Calculate the number of matching values
    match_values = np.sum(boolean_comparison == trues_matrix)
    # Calculate the threshold for 99.7% matching values (Criteria followed 3sigma)
    threshold = 0.997 * total_values
    # Apply threshold to the matching values
    Cond_3sigma = match_values >= threshold

    if Cond_3sigma == True:
        print("The differences with respect to the output TOA (", l1b_toa + band,
            ") are <0.01% for at least 3-sigma of the points.")
    else:
        print("The differences with respect to the output TOA (", l1b_toa + band,
            ") are not all <0.01% for at least 3-sigma of the points.")


    a = 2