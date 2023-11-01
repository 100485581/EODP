
# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\LAU\EODP\auxiliary'
indir = r"C:\LAU\EODP_TER\EODP-TS-E2E\sgm_out" # small scene
outdir = r"C:\LAU\EODP_TER\EODP-TS-E2E\OutputsLaura"

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()
