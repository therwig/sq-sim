import ROOT
# Calculating the
f = ROOT.TFile('data/final_muons_noSkim.root', 'read')
t = f.Get('Events')

# t.Draw(">>elist", "pz>0.001 && fabs(x)<50 && fabs(y)<50")
# elist = ROOT.gDirectory.Get("elist")
# nExit = elist.GetN()
# print('Number of muons exiting the dump', nExit)

# Set the normalization
#   we already know this selection should give 0.81439 events per bucket
refSel = "fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40 && pz>20"
refNorm = 0.81439
refNum = t.GetEntries(refSel)
print('Reference:', refNum, 'entries correspond to ',refNorm,'events')

t.Draw(">>elist", "fabs(x)<50 && pz>5 && pdg==13")
#t.Draw(">>elist", "fabs(x)<50 && pz>5 && pdg==13 && fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40") #to test
elist = ROOT.gDirectory.Get("elist")
nAll5 = refNorm/refNum * elist.GetN()
print('Number of 5 GeV mu- exiting the dump', nAll5)

t.SetEventList(elist)
nRight5 = refNorm/refNum * t.GetEntries("x<-10 && fabs(x)<50 && pz>5 && pdg==13")
nWrong5 = refNorm/refNum * t.GetEntries("x>10 && fabs(x)<50 && pz>5 && pdg==13")

print("Num 5 GeV (10cm offset): all, right, wrong = ", nAll5, nRight5, nWrong5)

if False:
    nRight5_20cm = refNorm/refNum * t.GetEntries("x<-20 && fabs(x)<50 && pz>5 && pdg==13")
    nWrong5_20cm = refNorm/refNum * t.GetEntries("x>20 && fabs(x)<50 && pz>5 && pdg==13")
    print("Num 5 GeV (20cm offset): all, right, wrong = ", nAll5, nRight5_20cm, nWrong5_20cm)

# number of events per BX with a pair
npair5 = nRight5 * nWrong5
print(npair5)

'''
1.1432692794719879 * 0.00035232659189140034 = 0.00040280417 pairs per BX
From the other calculation (step4_2mu_analysis), we find
0.064016150 of pairs overlap in X (2cm)
0.11387252 of pairs overlap in Y (2cm)
0.0065108660 of pairs have dxy(mu1,mu2) < 2cm

This is now:
0.00040280417 * 0.0065108660 = 2.6226040e-06 per BX
Of these, 0.0033368317 of pairs have mass < 2 GeV.

So we expect 8.7511881e-09 of these background-like pairs with mass < 2 GeV.
If we also consider the +- in addition to -+ this is roughly 2x
8.7511881e-09 / 0.5 = 1.7502376e-08

######### 8.7511881e-09 / 0.45 = 1.9447085e-08 (this is probably not right)

'''


# Reference: 3656735 entries correspond to  0.81439 events
# Num 5 GeV: all, right, wrong =  1.1607813809723702 1.1432692794719879 0.00035232659189140034

# nStation = t.GetEntries("x>10 && pz>5 && pdg==13")
# nStation = t.GetEntries("fabs(x)<50 && pz>5 && pdg==13")
# nStation10 = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40 && pz>10")

# print('Number of muons entering the station', nStation)

# # restrict to consider only the interesting events
# t.SetEventList(elist)
# nStation = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40")
# print('Number of muons entering the station', nStation)
# nStation10 = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40 && pz>10")
# print('Number of muons entering the station 10 ', nStation10)
# nStation20 = t.GetEntries("fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40 && pz>20")
# print('Number of muons entering the station 20 ', nStation20)
# # print('Number of muons entering the station', nStation, nStation10, nStation20)
# n10 = t.GetEntries("pz>10")
# print('Number of exiting muons with pt>10 ', n10)
# n20 = t.GetEntries("pz>20")
# print('Number of exiting muons with pt>20 ', n20)

# nKnownTracker=1.9
# nAll10 = nKnownTracker * n10 / nStation
# nAll20 = nKnownTracker * n20 / nStation
# nSta10 = nKnownTracker * nStation10 / nStation
# nSta20 = nKnownTracker * nStation20 / nStation
# print("Expect to get an average of ", nAll10,"10 GeV muons exiting the dump")
# print("Expect to get an average of ", nAll20,"20 GeV muons exiting the dump")
# print("Expect to get an average of ", nSta10,"10 GeV muons entering the tracker station")
# print("Expect to get an average of ", nSta20,"20 GeV muons entering the tracker station")
