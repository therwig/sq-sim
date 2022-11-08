import ROOT
import numpy as np
from constants import *

# take numbers for a 20 GeV muon on ECal
landau_mpv_ref = (280.316+22.425*np.log(20e3))/1e3
landau_wid_ref = (24.419+5.228*np.log(20e3))/1e3
landau_rescale = mu_dedx_dump/landau_mpv_ref # rescale 500 MeV mean loss in ECal to 7 GeV in FMag
# landau_x = np.arange(0, 100./landau_rescale, 0.01) # 100 GeV max loss
# landau_y = landau(landau_x, mpv=landau_mpv_ref, eta=landau_wid_ref)
# landau_x = landau_rescale*landau_x
# landau_y = landau_rescale*landau_y

def get_eloss(rand, dz=dump_len):
    return dz/dump_len * rand.Landau(landau_mpv_ref, landau_wid_ref)*landau_rescale

# def rand_landau(rand):
#     return np.random.choice(landau_x, p=landau_y / landau_y.sum())

def smear_angle(rand, e, x0):
    # calculated RMS(py)/e for 40 x0
    if e <=0: return 0
    dpx = (41.2+6.36*np.log(e/MeV))*MeV
    theta_rms = np.arcsin(dpx/e) * np.sqrt(x0/40)
    # print( theta_rms)
    return rand.Gaus(0,theta_rms)

# from Jackson
scatterFunc = ROOT.TF1("scatterFunc","1/sqrt(TMath::Pi())*exp(-x*x) + (fabs(x)>2)*1/(8*log(204*pow(26,1/3))*fabs(x*x*x))",-20,20);
def getScatterAngle1d(part, dist_x0):
    beta = part.p4.Beta()
    t0 = 13.6*MeV / (beta * part.p()) * np.sqrt(dist_x0) * (1 + 0.038 * np.log(dist_x0  / (beta*beta)))
    # jackson and pdg appear to diagree on 1/2 vs 1/sqrt(3)?
    return t0/2. * scatterFunc.GetRandom(-20,20)
    
def smear_theta_pdg_new(self, r, x0, z):
        z1 = r.Gaus(0,1)
        z2 = r.Gaus(0,1)
        yplane = z1 * z * t0 / np.sqrt(12) + z2 * z * t0 / 2
        tplane = z2 * t0
        Phiplane = np.arctan(yplane / z) if z>0 else 0
        return Phiplane * np.sin(tplane), Phiplane * np.cos(tplane)


# def smear_angle_pdg(rand, e, x0):
#     # calculated RMS(py)/e for 40 x0
#     if e <=0: return 0
#     dpx = (41.2+6.36*np.log(e/MeV))*MeV
#     theta_rms = np.arcsin(dpx/e) * np.sqrt(x0/40)
#     return rand.Gaus(0,theta_rms)
