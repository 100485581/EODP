
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\LAU\auxiliary'
indir = r"C:\LAU\EODP_TER_2023_working\EODP-TS-L1B\input"
outdir = r"C:\LAU\EODP_TER_2023_working\EODP-TS-L1B\myoutputs"

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
