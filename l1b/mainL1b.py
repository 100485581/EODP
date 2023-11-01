
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\LAU\EODP\auxiliary'
indir = r"C:\LAU\EODP_TER\EODP-TS-E2E\OutputsLaura"
outdir = r"C:\LAU\EODP_TER\EODP-TS-E2E\OutputsLaura_L1b"

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
