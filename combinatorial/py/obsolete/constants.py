#units
mm = 0.1
cm = mm * 10
m = mm * 1000
GeV = 1
MeV = 0.001 * GeV

# constants
fe_nucl_int = 16.77 * cm
fe_rad_len = 1.757 * cm

# geometry
dump_len = 5 * m
mu_dedx_dump = 7 * GeV
mu_dedx_x0 = mu_dedx_dump * (fe_rad_len/dump_len)
fmag_dp = 2.9 * GeV

# beam
beam_sigma_xy = 0.4 * cm
beam_sigma_pxy = 0.4 * GeV
protons_per_spill = 28000 # @ 53 MHz
mu_per_spill = 1167787 / 1e9 * protons_per_spill # from cristina:  about 30 (up to 60?)

# selection requirements
MAX_Dump_XY = 0.5 * m
pair_dxy = 1 * cm
min_pair_mu_p = 0.5 * GeV

#simulation
n_spills = int(1e5)
nPOT = n_spills * protons_per_spill
