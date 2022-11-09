import ROOT
# Calculating the
f = ROOT.TFile('data/final_muons_noSkim.root', 'read')
t = f.Get('Events')

t.Draw(">>elist", "pz>0.001 && fabs(x)<50 && fabs(y)<50")
elist = ROOT.gDirectory.Get("elist")
nExit = elist.GetN()
print('Number of muons exiting the dump', nExit)

# restrict to consider only the interesting events
t.SetEventList(elist)
nStation = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40")
print('Number of muons entering the station', nStation)
nStation10 = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40 && pz>10")
print('Number of muons entering the station 10 ', nStation10)
nStation20 = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40 && pz>20")
print('Number of muons entering the station 20 ', nStation20)
# print('Number of muons entering the station', nStation, nStation10, nStation20)
n10 = t.GetEntries("pz>10")
print('Number of exiting muons with pt>10 ', n10)
n20 = t.GetEntries("pz>20")
print('Number of exiting muons with pt>20 ', n20)

nKnownTracker=1.9
nAll10 = nKnownTracker * n10 / nStation
nAll20 = nKnownTracker * n20 / nStation
nSta10 = nKnownTracker * nStation10 / nStation
nSta20 = nKnownTracker * nStation20 / nStation
print("Expect to get an average of ", nAll10,"10 GeV muons exiting the dump")
print("Expect to get an average of ", nAll20,"20 GeV muons exiting the dump")
print("Expect to get an average of ", nSta10,"10 GeV muons entering the tracker station")
print("Expect to get an average of ", nSta20,"20 GeV muons entering the tracker station")
