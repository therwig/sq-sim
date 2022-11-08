// units
float mm = 0.1;
float cm = mm * 10;
float m = mm * 1000;
float GeV = 1;
float MeV = 0.001 * GeV;

// constants
float fe_nucl_int = 16.77 * cm;
float fe_rad_len = 1.757 * cm;
float mmass = 0.105 * GeV;

// geometry
float dump_len = 5 * m;
float mu_dedx_dump = 7 * GeV;
float mu_dedx_x0 = mu_dedx_dump * (fe_rad_len/dump_len);
float fmag_dp = 2.9 * GeV;
float half_fmag_dp = fmag_dp/2.;

// beam
float beam_sigma_xy = 0.4 * cm;
float beam_sigma_pxy = 0.333 * GeV;
int protons_per_spill = 28000; // @ 53 MHz
float mu_per_spill = 1167787 / 1e9 * protons_per_spill; // from cristina:  about 30 (up to 60?)

// selection requirements
float MAX_Dump_XY = 0.5 * m;
float pair_dxy = 1 * cm;
float min_pair_mu_p = 0.5 * GeV;

//simulation 
int n_spills = int(1e5);
int nPOT = n_spills * protons_per_spill;


// ranom uil
float landau_mpv_ref = (280.316+22.425*log(20e3))/1e3;
float landau_wid_ref = (24.419+5.228*log(20e3))/1e3;
float landau_rescale = mu_dedx_dump/landau_mpv_ref;
