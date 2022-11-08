from ROOT import *
import os

os.system('mkdir -p data')
fout = TFile.Open('data/initial_muons.root','recreate')

t = TTree("Events","")
t.ReadFile("genmuons_protons.csv","px/F:py/F:pz/F:pdg/I",",")
t.Write()

fout.Close()
