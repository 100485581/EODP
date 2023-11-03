#4.2.5. Pass/fail criteria
import pandas as pd

from common.io.writeToa import readToa
from common.io.readMat import readMat
from common.io.readArray import readArray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import globalConfig
from config.l1bConfig import l1bConfig

#Check for all bands that the differences with respect to the output TOA (ism_toa_) are <0.01% for at least 3-sigma of the points.

bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
Lau_toa_path = r"C:\LAU\EODP_TER\EODP-TS-ISM\OutputsLaura"
luss_toa_path = r"C:\LAU\EODP_TER\EODP-TS-ISM\output"

ism_toa_ = 'ism_toa_'

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, ism_toa_ + band + '.nc')

    # 2. Read your outputs
    Lau_toa = readToa(Lau_toa_path, ism_toa_ + band + '.nc')

    # 3. Compare
    difference = Lau_toa - luss_toa
    percentage = difference / Lau_toa * 100
    df = pd.DataFrame(percentage)
    percentage_df = df.fillna(0) # The division per zero gives some annoying NaN values
    boolean_comparison = np.array(percentage_df < 0.01)

    # Calculate the total number of values in each matrix
    total_values = boolean_comparison.size
    trues_matrix = np.full(boolean_comparison.shape, True)
    # Calculate the number of matching values (True values in the same positions)
    match_values = np.sum(boolean_comparison == trues_matrix)
    # Calculate the threshold for 99.7% (3sigma) matching values
    threshold = 0.997 * total_values
    # Apply threshold to the matching values
    Cond_3sigma = match_values >= threshold

    if Cond_3sigma == True:
        print("Differences with respect to the reference output TOA (", ism_toa_ + band,
            ") are INFERIOR to 0.01% for at least 3-sigma of the points.")
    else:
        print("Differences with respect to the reference output TOA (", ism_toa_ + band,
            ") are SUPERIOR to 0.01% for at least 3-sigma of the points.")



    # Check for all bands if there are any saturated pixels. Quantify the percentage of saturated
    # pixels per band.

    # Read final toa
    Lau_toa = readToa(Lau_toa_path, ism_toa_ + band + '.nc')

    saturated_values = np.sum(Lau_toa == 4095)
    percentage_saturated = saturated_values * 100 / Lau_toa.size
    print("The percentage of saturated values for", ism_toa_ + band,"is", "{:.2f}".format(percentage_saturated), "%.")
