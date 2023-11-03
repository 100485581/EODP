#4. EODP Pass/fail Check
import pandas as pd

from common.io.writeToa import readToa
from common.io.readMat import readMat
from common.io.readArray import readArray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import globalConfig
from config.l1bConfig import l1bConfig

#Assignment: Check for all bands that the differences with respect to the output TOA (ism_toa_isrf) are <0.01% for at least 3-sigma of the points.

bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
Lau_toa_path = r"C:\LAU\EODP_TER\EODP-TS-ISM\OutputsLaura"
Luss_toa_path = r"C:\LAU\EODP_TER\EODP-TS-ISM\output"

ism_toa_isrf = 'ism_toa_isrf_'
ism_toa_optical = 'ism_toa_optical_'
Hdiff = 'Hdiff_'
Hdefoc = 'Hdefoc_'
Hwfe = 'Hwfe_'
Hdet = 'Hdet_'
Hsmear = 'Hsmear_'
Hmotion = 'Hmotion_'
Hsys = 'Hsys_'
fnAct = 'fnAct_'
fnAlt = 'fnAlt_'

for band in bands:

#Outputs Comparison
    # 1. Read LUSS
    luss_toa = readToa(Luss_toa_path, ism_toa_isrf + band + '.nc')

    # 2. Read your outputs (Laura's)
    Lau_toa = readToa(Lau_toa_path, ism_toa_isrf + band + '.nc')

    # 3. Comparison
    difference = Lau_toa - luss_toa
    percentage = difference / Lau_toa * 100 #porcentual difference
    df = pd.DataFrame(percentage)
    percentage_df = df.fillna(0)
    boolean_comparison = np.array(percentage_df < 0.01)

    # Calculation of the total number of values for every matrix
    total_values = boolean_comparison.size
    trues_matrix = np.full(boolean_comparison.shape, True)
    # Calculate the number of matching values
    match_values = np.sum(boolean_comparison == trues_matrix)
    # Calculate the thresholds for 99.7% matching values (Criteria followed 3sigma)
    threshold = 0.997 * total_values
    # Apply thresholds to the matching values
    Cond_3sigma = match_values >= threshold

    if Cond_3sigma == True:
        print("Differences with respect to the reference output TOA (", ism_toa_isrf + band,
            ") are INFERIOR to 0.01% for at least 3-sigma of the points.")
    else:
        print("Differences with respect to the reference output TOA (", ism_toa_isrf + band,
            ") are SUPERIOR to 0.01% for at least 3-sigma of the points.")

    # Check for all bands that the differences with respect to the output TOA (ism_toa_optical) are <0.01%
    # for at least 3-sigma of the points.

    # 1. Read LUSS
    luss_toa = readToa(Luss_toa_path, ism_toa_optical + band + '.nc')

    # 2. Read your outputs
    Lau_toa = readToa(Lau_toa_path, ism_toa_optical + band + '.nc')

    # 3. Compare
    difference = Lau_toa - luss_toa
    percentage = difference / Lau_toa * 100
    df = pd.DataFrame(percentage)
    percentage_df = df.fillna(0)  # The division per zero gives some annoying NaN values
    boolean_comparison = np.array(percentage_df < 0.01)

    # Calculate the total number of values in each matrix
    total_values = boolean_comparison.size
    trues_matrix = np.full(boolean_comparison.shape, True)
    # Calculate the number of matching values (True values in the same positions)
    match_values = np.sum(boolean_comparison == trues_matrix)
    # Calculate the limit for 99.7% (3sigma) matching values
    threshold = 0.997 * total_values
    # Apply limits to the matching values
    Cond_3sigma = match_values >= threshold

    if Cond_3sigma == True:
        print("Differences with respect to the reference output TOA (", ism_toa_optical + band,
                  ") are INFERIOR to 0.01% for at least 3-sigma of the points.")
    else:
        print("Differences with respect to the reference output TOA (", ism_toa_optical + band,
                  ")  are SUPERIOR to 0.01% for at least 3-sigma of the points.")

    


    # Plot for all bands the System MTF across and along track (for the central pixels). Report the MTF at
    # the Nyquist frequency. Explain whether this is a decent or mediocre value and why

    # Read your outputs
    Lau_Hdiff = readMat(Lau_toa_path, Hdiff + band + '.nc')
    Lau_Hdefoc = readMat(Lau_toa_path, Hdefoc + band + '.nc')
    Lau_Hwfe = readMat(Lau_toa_path, Hwfe + band + '.nc')
    Lau_Hdet = readMat(Lau_toa_path, Hdet + band + '.nc')
    Lau_Hsmear = readMat(Lau_toa_path, Hsmear + band + '.nc')
    Lau_Hmotion = readMat(Lau_toa_path, Hmotion + band + '.nc')
    Lau_Hsys = readMat(Lau_toa_path, Hsys + band + '.nc')
    Lau_fnAct = readArray(Lau_toa_path, fnAct + band + '.nc')
    Lau_fnAlt = readArray(Lau_toa_path, fnAlt + band + '.nc')

    #fnAct: 1D normalised frequencies 2D ACT (f/(1/w))
    lines_ALT = Lau_Hdiff.shape[0]
    ACT_central_line = int(lines_ALT / 2)
    lines_ACT = Lau_Hdiff.shape[1]
    ALT_central_line = int(lines_ACT / 2)


    # ACT
    plt.plot(Lau_fnAct[75:150], Lau_Hdiff[ACT_central_line, 75:150])
    plt.plot(Lau_fnAct[75:150], Lau_Hdefoc[ACT_central_line, 75:150])
    plt.plot(Lau_fnAct[75:150], Lau_Hwfe[ACT_central_line, 75:150])
    plt.plot(Lau_fnAct[75:150], Lau_Hdet[ACT_central_line, 75:150])
    plt.plot(Lau_fnAct[75:150], Lau_Hsmear[ACT_central_line, 75:150])
    plt.plot(Lau_fnAct[75:150], Lau_Hmotion[ACT_central_line, 75:150])
    plt.plot(Lau_fnAct[75:150], Lau_Hsys[ACT_central_line, 75:150], color='black', linewidth=2.5)
    plt.plot(np.full(2, 0.5), np.linspace(0, 1, 2), linestyle='--', color='black')
    plt.xlabel('Spatial Frequency [-]')
    plt.ylabel('MTF')
    plt.title("System MTF, slice ACT for " + band + " for ALT central pixels")
    plt.legend(['Diffraction MTF', 'Defocus MTF', 'WFE Aberration MTF', 'Detector MTF', 'Smearing MTF', 'Motion blur MTF', 'System MTF','f Nyquist'])
    plt.xlim(-0.025, 0.525)
    plt.ylim(-0.025, 1.025)
    plt.savefig("ism_plot_MTF_ACT_" + band + ".png")
    plt.show()


    # ALT
    plt.plot(Lau_fnAlt[50:100], Lau_Hdiff[50:100, ALT_central_line])
    plt.plot(Lau_fnAlt[50:100], Lau_Hdefoc[50:100, ALT_central_line])
    plt.plot(Lau_fnAlt[50:100], Lau_Hwfe[50:100, ALT_central_line])
    plt.plot(Lau_fnAlt[50:100], Lau_Hdet[50:100, ALT_central_line])
    plt.plot(Lau_fnAlt[50:100], Lau_Hsmear[50:100, ALT_central_line])
    plt.plot(Lau_fnAlt[50:100], Lau_Hmotion[50:100, ALT_central_line])
    plt.plot(Lau_fnAlt[50:100], Lau_Hsys[50:100, ALT_central_line], color='black', linewidth=2.5)
    plt.plot(np.full(2, 0.5), np.linspace(0, 1, 2), linestyle='--', color='black')
    plt.xlabel('Spatial frequencies [-]')
    plt.ylabel('MTF')
    plt.title("System MTF, slice ALT for " + band + "for ACT central pixels")
    plt.legend(
        ['Diffraction MTF', 'Defocus MTF', 'WFE Aberration MTF', 'Detector MTF', 'Smearing MTF', 'Motion blur MTF',
         'System MTF', 'f Nyquist'])
    plt.xlim(-0.025, 0.525)
    plt.ylim(-0.025, 1.025)
    plt.savefig("ism_plot_MTF_ALT_" + band + ".png")
    plt.show()

    a = 2



