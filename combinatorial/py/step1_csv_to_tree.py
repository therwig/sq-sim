from ROOT import *

fout = TFile.Open('initial_muons.root','recreate')

t = TTree("Events","")
t.ReadFile("genmuons_protons.csv","px/F:py/F:pz/F:pdg/I",",")
t.Write()

fout.Close()
