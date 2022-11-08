import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')
# import numpy as np
# r = ROOT.TRandom3(2022)
# from constants import *
# from particle import part
# from rand import get_eloss, smear_angle, getScatterAngle1d
from HistHelper import HistHelper
from plotUtils import *

f = ROOT.TFile('data/final_muons_muminus_xge10_skim_20k.root','read')
t = f.Get('Events')

h = HistHelper()
h.book('init_px',';p_{x}[GeV];entries',30,-2,4)
h.book('x_all',';x[cm];entries',40,10,50)
h.book('dxScatter',';dx from scattering [cm];entries',60,-50,250)
h.book('dxBeam',';dx from p_{x}(beam) [cm];entries',60,-40,120)
h.book('dxBfield',';dx from B field [cm];entries',40,-400,0)
h.book('x_hiScatter',';x[cm];entries',40,10,50)
h.book('x_loScatter',';x[cm];entries',40,10,50)

t.Draw('dxScatter>>dxScatter','')
t.Draw('dxBeam>>dxBeam','')
t.Draw('dxBfield>>dxBfield','')

t.Draw('init_px>>init_px','')
t.Draw('x>>x_all','')
t.Draw('x>>x_hiScatter','dxScatter>10')
t.Draw('x>>x_loScatter','dxScatter<10')

pdir='plots/skim/'
plot('compX_scatter', [h['x_all'],h['x_hiScatter'],h['x_loScatter']],labs=['all','dx(scatter)>10cm','dx(scatter)<10cm'], pdir=pdir)
plot('init_px', [h['init_px']],labs='none', pdir=pdir, dopt='hist')
plot('x', [h['x_all']],labs='none', pdir=pdir, dopt='hist')

for n in ['dxScatter','dxBeam','dxBfield']:
    plot(n, [h[n]],labs='none', pdir=pdir, dopt='hist')
    
