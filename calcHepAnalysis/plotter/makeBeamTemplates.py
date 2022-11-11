import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')

sys.path.insert(0,'/Users/therwig/work/commonRootTools')
from HistHelper import HistHelper
h = HistHelper()

f = ROOT.TFile('/Users/therwig/work/m3/combinatorial_pions/cpp/data/final_muons_noSkim.root')
t = f.Get('Events')

fo = ROOT.TFile('beamTemplates.root','recreate')
h.book('px',';px [GeV] ;',100,-5,5)
h.book('py',';py [GeV] ;',100,-5,5)
h.book('pz',';pz [GeV] ;',240,0,120)
h.book('x',';x [cm] ;',   100,-100,100)
h.book('y',';y [cm] ;',   100,-100,100)

h.book2d('2d_px',';px [GeV] ;',60,0,120, 100,-5,5)
h.book2d('2d_py',';py [GeV] ;',60,0,120, 100,-5,5)
h.book2d('2d_x',';x [cm] ;',   60,0,120, 100,-100,100)
h.book2d('2d_y',';y [cm] ;',   60,0,120, 100,-100,100)

cut='pz>0'
t.Draw('px>>px',cut)
t.Draw('py>>py',cut)
t.Draw('pz>>pz',cut)
t.Draw('x>>x',cut) 
t.Draw('y>>y',cut) 
t.Draw('px:pz>>2d_px',cut)
t.Draw('py:pz>>2d_py',cut)
t.Draw('x:pz>>2d_x',cut) 
t.Draw('y:pz>>2d_y',cut) 
fo.Write()
fo.Close()
f.Close()
