import ROOT
from HistHelper import HistHelper
h = HistHelper()

f = ROOT.TFile('final_muons.root','read')
t = f.Get('Events')

fo = ROOT.TFile('templates.root','recreate')
h.book('pos_x','',200,-100,100)
h.book('neg_x','',200,-100,100)

t.Draw('x>>neg_x','pz>0.5 && pdg==13')
t.Draw('x>>pos_x','pz>0.5 && pdg==-13')

fo.Write()
fo.Close()
