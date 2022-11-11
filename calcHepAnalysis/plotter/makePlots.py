import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')

import numpy as np
from array import array
sys.path.insert(0,'/Users/therwig/work/commonRootTools')
from collections import OrderedDict
from HistHelper import HistHelper
from plotUtils import *

#FAST=True
FAST=0

dataDir = 'data/20GeVBeam'
eBeam=20
MoT=1e15
# lumi = 1e-36 * 7.874 * 6.022e23 / 55.845 * 10 * 1e13 # for 1e13 MoT, 10cm target, in 1/pb
lumi = 1e-36 * 7.874 * 6.022e23 / 55.845 * 10 * MoT # for 1e15 MoT, 10cm target, in 1/pb
MoT=5e13
lumi = 1e-36 * 7.874 * 6.022e23 / 55.845 * 100 * MoT # for 5e13 MoT, 1m target, in 1/pb
nBkgd = 3.187970E+05 * lumi

nSig={}
nSig[1000]=6.634621E+05
nSig[2000]=1.009877E+04
nSig[220]=5.343163E+07
nSig[3000]=3.045280E+02
nSig[300]=2.842917E+07
nSig[4000]=1.762285E+01
nSig[400]=1.449005E+07
nSig[500]=7.971065E+06
nSig[600]=4.608885E+06
nSig[700]=2.753382E+06
nSig[800]=1.686569E+06
nSig[900]=1.050958E+06
gSref=1e-3
for x in nSig: nSig[x] = nSig[x] * lumi * gSref * gSref

ROOT.gROOT.ProcessLine(".L plotter/helpers.C+")
ROOT.load_f5()

fout = ROOT.TFile('hist.root','recreate')
mSs=[220,300,400,500,600,700,800,1000,2000,3000,4000]
h = HistHelper()

weights={}
weights['']='1'
weights['w_']='f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'
weights['w2_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.3) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'
weights['w3_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.3) * (min({smr}m1z,{smr}Mz)>5)'
# weights['w3_']='(min({smr}m1z,{smr}Mz)>5)'
# weights['w3_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.4) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'
# weights['w4_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.5) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'
# weights['w3_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.3) * (hypot({smr}m1x,{smr}m1y)/{eBeam}>0.01) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'
# weights['w4_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.3) * (hypot({smr}m1x,{smr}m1y)/{eBeam}>0.015) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'
# weights['w_']='f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'.format(eBeam=eBeam, smr=smr)
# weights['w2_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.3) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'.format(eBeam=eBeam, smr=smr)
# weights['w3_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.4) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'.format(eBeam=eBeam, smr=smr)
# weights['w4_']='(ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p > 0.5) * f5(5./(min({smr}m1z,{smr}Mz)/{eBeam}))'.format(eBeam=eBeam, smr=smr)
wns = weights.keys()

for mS in mSs+['b']:
    for smr in ['','s_']:
        for wn in wns: # ['','w_','w2_']:
            pfx=smr+wn
            h.book(str(mS)+'_'+pfx+'ptm1_frac',';p_{T}(#mu^{-}_{1})/p(Beam) ;',40,0,.10)
            h.book(str(mS)+'_'+pfx+'ptm2_frac',';p_{T}(#mu^{-}_{2})/p(Beam) ;',40,0,.10)
            h.book(str(mS)+'_'+pfx+'ptM_frac',';p_{T}(#mu^{+})/p(Beam) ;',40,0,.10)
            h.book(str(mS)+'_'+pfx+'pm1_frac',';p(#mu^{-}_{1})/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'pm2_frac',';p(#mu^{-}_{2})/p(Beam) ;',20,0,0.5)
            h.book(str(mS)+'_'+pfx+'pM_frac',';p(#mu^{+})/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'pzm1_frac',';p_{z}(#mu^{-}_{1})/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'pzm2_frac',';p_{z}(#mu^{-}_{2})/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'pzM_frac',';p_{z}(#mu^{+})/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'minpm_frac',';min(p(#mu^{-}_{1}),p(#mu^{-}_{2}))/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'maxpm_frac',';max(p(#mu^{-}_{1}),p(#mu^{-}_{2}))/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'minpzm_frac',';min(p_{z}(#mu^{-}_{1}),p(#mu^{-}_{2}))/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'maxpzm_frac',';max(p_{z}(#mu^{-}_{1}),p(#mu^{-}_{2}))/p(Beam) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'mass1lo',';m(#mu^{-}_{1},#mu^{+}) [GeV];',64,0,3.2)
            h.book(str(mS)+'_'+pfx+'pair1_m1frac',';p(#mu^{+})/p(#mu^{-}_{1},#mu^{+}) [GeV];',40,0,1)
            h.book(str(mS)+'_'+pfx+'pair1_Mfrac',';p(#mu^{+})/p(#mu^{-}_{1},#mu^{+}) [GeV];',40,0,1)
            h.book(str(mS)+'_'+pfx+'mass1',';m(#mu^{-}_{1},#mu^{+}) [GeV];',100,0,5)
            h.book(str(mS)+'_'+pfx+'mass2',';m(#mu^{-}_{2},#mu^{+}) [GeV];',100,0,5)
            h.book(str(mS)+'_'+pfx+'pairp1_frac',';p(#mu^{-}_{1},#mu^{+}) ;',20,0,1)
            h.book(str(mS)+'_'+pfx+'pairp2_frac',';p(#mu^{-}_{2},#mu^{+}) ;',20,0,1)
            # h.book(str(mS)+'_'+pfx+'dot1',';#mu^{-}_{1}.#mu^{+} [GeV2];',100,0,5)
            # h.book(str(mS)+'_'+pfx+'dot2',';#mu^{-}_{2}.#mu^{+} [GeV2];',100,0,5)
            # h.book(str(mS)+'_'+pfx+'dotRat1',';#mu^{-}_{1}.#mu^{+}/m(#mu^{-}_{1},#mu^{+}) ;',100,0.55,0.72)
            # h.book(str(mS)+'_'+pfx+'dotRat2',';#mu^{-}_{2}.#mu^{+}/m(#mu^{-}_{2},#mu^{+}) ;',100,0.55,0.72)
            h.book(str(mS)+'_'+pfx+'dr1',';dR(#mu^{-}_{1},#mu^{+});',100,0,8)
            h.book(str(mS)+'_'+pfx+'dr2',';dR(#mu^{-}_{2},#mu^{+});',100,0,8)
            h.book(str(mS)+'_'+pfx+'drr1',';d#theta(#mu^{-}_{1},#mu^{+});',50,0,0.5)
            h.book(str(mS)+'_'+pfx+'drr2',';d#theta(#mu^{-}_{2},#mu^{+});',50,0,0.5)
            h.book(str(mS)+'_'+pfx+'pair1z1fracP',';max(p(#mu^{-}_{1}),p(#mu^{+}))/p(#mu^{-}_{1}+#mu^{+});',40,0.5,1)
            h.book(str(mS)+'_'+pfx+'pair2z1fracP',';max(p(#mu^{-}_{2}),p(#mu^{+}))/p(#mu^{-}_{2}+#mu^{+});',40,0.5,1)
            h.book(str(mS)+'_'+pfx+'pair1z1fracPz',';max(p_{Z}(#mu^{-}_{1}),p_{Z}(#mu^{+}))/p_{Z}(#mu^{-}_{1}+#mu^{+});',40,0.5,1)
            h.book(str(mS)+'_'+pfx+'pair2z1fracPz',';max(p_{Z}(#mu^{-}_{2}),p_{Z}(#mu^{+}))/p_{Z}(#mu^{-}_{2}+#mu^{+});',40,0.5,1)
            # h.book(str(mS)+'_'+pfx+'test','test',100,0.55,0.72)
            h.book(str(mS)+'_'+pfx+'test',';m(#mu^{-}_{1},#mu^{+}) [GeV];',100,0,5)
            # h.book(str(mS)+'_minp_x_beam',';min(p) [GeV] ;',120,0,60)
            # h.book(str(mS)+'_minp_x_beam_cumul',';min(p) [GeV] ;',120,0,60)
            
            # bins = np.exp(np.linspace(np.log(0.200), np.log(1.2), 50))
            bins = np.exp(np.linspace(np.log(0.200), np.log(1.2), 100))
            bins = np.exp(np.linspace(np.log(0.200), np.log(1.2), 80))
            h.bookBins(str(mS)+'_'+pfx+'mass1lx',';m(#mu^{-}_{1},#mu^{+}) [GeV];',bins)
            # bins = np.exp(np.linspace(np.log(0.200), np.log(1.2), 400))
            # bins = np.exp(np.linspace(np.log(0.200), np.log(6), 150))
            # h.bookBins(str(mS)+'_'+pfx+'mass1lx2',';m(#mu^{-}_{1},#mu^{+}) [GeV];',bins)
            # h.book(str(mS)+'_'+pfx+'mass1lx2',';m(#mu^{-}_{1},#mu^{+}) [GeV];',40,0,6)
            bins = np.exp(np.linspace(np.log(0.200), np.log(1.5), 90))
            h.bookBins(str(mS)+'_'+pfx+'mass1lx2',';m(#mu^{-}_{1},#mu^{+}) [GeV];',bins)
            bins = np.exp(np.linspace(np.log(0.200), np.log(6), 400))
            # bins = np.exp(np.linspace(np.log(0.200), np.log(1.2), 80))
            h.bookBins(str(mS)+'_'+pfx+'mass1lx3',';m(#mu^{-}_{1},#mu^{+}) [GeV];',bins)

#
# Load the beam profile distributions
fh = ROOT.TFile('beamTemplates.root','read')
hpz = fh.Get('pz')
fout.cd()
hpzc = hpz.Clone('cumul_pz_beam')
tot = hpz.Integral(1,hpz.GetNbinsX()+1)
for i in range(1,hpz.GetNbinsX()+1):
    hpzc.SetBinContent(i, hpz.Integral(i,hpz.GetNbinsX()+1) / tot)
    hpzc.SetBinError(i, 0)
plot('pz',[hpzc],
     labs='none',
     logy=1,ymin=1e-8,
     ytitle='Muon fraction',xtitle='p_{z} [GeV]',dopt='hist',legstyle='l')

nEntries={}
            
for mS in mSs+['b']:
    if mS == 'b':
        f = ROOT.TFile.Open(dataDir+'/../20GeVBeamBg.root','r')
        t = f.Get('Events')
        t.AddFriend('Friends',dataDir+'/../20GeVBeamBg_Friend.root')
    else:
        f = ROOT.TFile.Open(dataDir+'/mS{}MeV20_decayed.root'.format(mS),'r')
        t = f.Get('Events')
        t.AddFriend('Friends',dataDir+'/mS{}MeV20_decayed_Friend.root'.format(mS))
    fout.cd()
    nEntries[mS]=t.GetEntries()
    for smr in ['','s_']:
        # for wn, w in [('','1'),('w_','5/f5(min({smr}m1z,{smr}Mz))')]:
        for wn in weights:
            w = weights[wn].format(eBeam=eBeam, smr=smr)
            # print (wn, w)
        # for wn, w in [('','1'),('w_','f5(5./(min('+smr+'m1z,'+smr+'Mz)/'+str(eBeam)+'))')]:
            # w is fraction of events that would pass a pz>5 GeV cut on both muons
            # this is the minimum beam fraction of mu+ and mu-
            pfx=smr+wn
            if not FAST:
                t.Draw("hypot({smr}m1x,{smr}m1y)/{eBeam}>>{mS}_{pfx}ptm1_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("hypot({smr}m2x,{smr}m2y)/{eBeam}>>{mS}_{pfx}ptm2_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("hypot({smr}Mx,{smr}My)/{eBeam}>>{mS}_{pfx}ptM_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}m1x,{smr}m1y,{smr}m1z)/{eBeam}>>{mS}_{pfx}pm1_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}m2x,{smr}m2y,{smr}m2z)/{eBeam}>>{mS}_{pfx}pm2_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}Mx,{smr}My,{smr}Mz)/{eBeam}>>{mS}_{pfx}pM_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}m1z/{eBeam}>>{mS}_{pfx}pzm1_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}m2z/{eBeam}>>{mS}_{pfx}pzm2_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}Mz/{eBeam}>>{mS}_{pfx}pzM_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("min(ptot({smr}m1x,{smr}m1y,{smr}m1z),ptot({smr}m2x,{smr}m2y,{smr}m2z))/{eBeam}>>{mS}_{pfx}minpm_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("max(ptot({smr}m1x,{smr}m1y,{smr}m1z),ptot({smr}m2x,{smr}m2y,{smr}m2z))/{eBeam}>>{mS}_{pfx}maxpm_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("min({smr}m1z,{smr}m2z)/{eBeam}>>{mS}_{pfx}minpzm_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("max({smr}m1z,{smr}m2z)/{eBeam}>>{mS}_{pfx}maxpzm_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}pair1x,{smr}pair1y,{smr}pair1z)/{eBeam}>>{mS}_{pfx}pairp1_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}pair2x,{smr}pair2y,{smr}pair2z)/{eBeam}>>{mS}_{pfx}pairp2_frac".format(eBeam=eBeam, mS=mS, smr=smr, pfx=pfx),w)
                # t.Draw("sqrt({smr}dot1)>>{mS}_{pfx}dot1".format(mS=mS, smr=smr, pfx=pfx),w)
                # t.Draw("sqrt({smr}dot2)>>{mS}_{pfx}dot2".format(mS=mS, smr=smr, pfx=pfx),w)
                # t.Draw("sqrt({smr}dot1)/{smr}mass1>>{mS}_{pfx}dotRat1".format(mS=mS, smr=smr, pfx=pfx),w)
                # t.Draw("sqrt({smr}dot2)/{smr}mass2>>{mS}_{pfx}dotRat2".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}mass2>>{mS}_{pfx}mass2".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}dr1>>{mS}_{pfx}dr1".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}dr2>>{mS}_{pfx}dr2".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}drr1>>{mS}_{pfx}drr1".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}drr2>>{mS}_{pfx}drr2".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}pair1z1fracP>>{mS}_{pfx}pair1z1fracP".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}pair2z1fracP>>{mS}_{pfx}pair2z1fracP".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}pair1z1fracPz>>{mS}_{pfx}pair1z1fracPz".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("{smr}pair2z1fracPz>>{mS}_{pfx}pair2z1fracPz".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}m1x,{smr}m1y,{smr}m1z)/{smr}pair1p>>{mS}_{pfx}pair1_m1frac".format(mS=mS, smr=smr, pfx=pfx),w)
                t.Draw("ptot({smr}Mx,{smr}My,{smr}Mz)/{smr}pair1p>>{mS}_{pfx}pair1_Mfrac".format(mS=mS, smr=smr, pfx=pfx),w)
            # ALWAYS DRAW MASSES
            t.Draw("{smr}mass1>>{mS}_{pfx}mass1lo".format(mS=mS, smr=smr, pfx=pfx),w)
            t.Draw("{smr}mass1>>{mS}_{pfx}mass1lx".format(mS=mS, smr=smr, pfx=pfx),w)
            # print("ATTN","{smr}mass1>>{mS}_{pfx}mass1lx".format(mS=mS, smr=smr, pfx=pfx),w)
            t.Draw("{smr}mass1>>{mS}_{pfx}mass1lx2".format(mS=mS, smr=smr, pfx=pfx),w)
            t.Draw("{smr}mass1>>{mS}_{pfx}mass1lx3".format(mS=mS, smr=smr, pfx=pfx),w)
            t.Draw("{smr}mass1>>{mS}_{pfx}mass1".format(mS=mS, smr=smr, pfx=pfx),w)
            # t.Draw("sqrt(0.5-(.105/{smr}mass1)*(.105/{smr}mass1))>>{mS}_{pfx}test".format(mS=mS, smr=smr, pfx=pfx),w)
            # w='1'
            # t.Draw("{smr}mass1>>{mS}_{smr}test".format(mS=mS, smr=smr),w)
    
    # t.Draw("sqrt(m2x*m2x+m2y*m2y+m2z*m2z+0.105*0.105)/{}>>{}_pm2_frac".format(eBeam, mS))
    # t.Draw("min(sqrt(m1x*m1x+m1y*m1y+m1z*m1z+0.105*0.105),sqrt(m2x*m2x+m2y*m2y+m2z*m2z+0.105*0.105))/{}>>{}_minp_frac".format(eBeam, mS))
    f.Close()

legsty=['f']+['l' for x in mSs]
allTags=['b']+[str(x) for x in mSs]
allLabs=['Bkg']+[str(mS)+' MeV' for mS in mSs]
pnames=['pm1_frac', 'pm2_frac', 'pM_frac',
        'ptm1_frac', 'ptm2_frac', 'ptM_frac',
        'pzm1_frac', 'pzm2_frac', 'pzM_frac',
        'minpm_frac', 'maxpm_frac', 'minpzm_frac', 'maxpzm_frac',
        'mass1', 'mass2', 'mass1lx', 'mass1lx2','mass1lx3', 'pair1_Mfrac','pair1_m1frac',
        'dr1','dr2','drr1','drr2',
        'pairp1_frac', 'pairp2_frac', #'dotRat1', 'dotRat2',
        'pair1z1fracP', 'pair2z1fracP','pair1z1fracPz', 'pair2z1fracPz', 'test',
        ]
## YIELDS
# at this point, the weight is number of passing events
norms=[1./nEntries['b']]+[1./nEntries[x] for x in mSs]
norms=[nBkgd/nEntries['b']]+[nSig[x]/nEntries[x] for x in mSs]
gs={}
for smrName, smrPfx in [('yields_smr','s_'),
                        #('yields5_smr','s_w_'),
                        # ('yields_pz5_frac0p3_smr','s_w2_'),
                        ('yields_pz5_frac0p3_SQ_smr','s_w2_'),
                        ('yields_pz5_frac0p3_20_smr','s_w3_'),
                        # ('yields5frac0p4_smr','s_w3_'),
                        # ('yields5frac0p5_smr','s_w4_'),
                        # ('yields5frac0p3Pt1_smr','s_w3_'),
                        # ('yields5frac0p3Pt15_smr','s_w4_'),
                        ]:
    allLabs=['Bkg']+[str(mS)+' MeV' for mS in mSs]
    for pname in pnames:
        plot(smrName+'_'+pname,[h[t+'_'+smrPfx+pname] for t in allTags],
             labs=allLabs, rescale=norms, fcolz=[18], toptext=smrName,
             ytitle='events', dopt='hist',legstyle=legsty)
    for pname in ['mass1lx', 'mass1lx2','mass1lx3']:
        for t in allTags: h[t+'_'+smrPfx+pname].GetXaxis().SetMoreLogLabels()
        plot(smrName+'_'+pname+'_logx',[h[t+'_'+smrPfx+pname] for t in allTags],
             labs=allLabs, logx=1, fcolz=[18], toptext=smrName,
             ytitle='events', dopt='hist',legstyle=legsty)
        plot(smrName+'_'+pname+'_logxy',[h[t+'_'+smrPfx+pname] for t in allTags],
             labs=allLabs, logx=1, logy=1, ymin=0.8, fcolz=[18], toptext=smrName,
             ytitle='events', dopt='hist',legstyle=legsty)
    for pname in ['mass1lx', 'mass1lx2','mass1lx3']:
        toptext=smrName+', gS='+str(gSref)+', MoT='+str(MoT)
        toptext='{}: gS={}, MoT={:.1e}'.format(smrName, gSref, MoT)
        sb = [h[t+'_'+smrPfx+pname].Clone(t+'_'+smrPfx+pname+'sb') for t in allTags]
        for x in sb[1:]: x.Divide(sb[0])
        sb[0].Divide(sb[0])
        plot(smrName+'_'+pname+'_logx_sb',sb,
             labs=allLabs, logx=1, fcolz=[18], toptext=toptext,
             ytitle='S/B', ymax=2, dopt='hist',legstyle=legsty)
        plot(smrName+'_'+pname+'_logxy_sb',sb,
             labs=allLabs, logx=1, logy=1, ymin=0.001, ymax=5, fcolz=[18], toptext=toptext,
             ytitle='S/B', dopt='hist',legstyle=legsty)
        srb = [h[t+'_'+smrPfx+pname].Clone(t+'_'+smrPfx+pname+'srb') for t in allTags]
        for x in srb[1:]:
        # for x in srb[1:]+[srb[0]]:
            for ibin in range(1,srb[0].GetNbinsX()+1):
                _s = x.GetBinContent(ibin)
                _b = srb[0].GetBinContent(ibin)
                x.SetBinContent(ibin, _s/np.sqrt(_b if _b else 1.))
        for ibin in range(1,srb[0].GetNbinsX()+1):
            _b = srb[0].GetBinContent(ibin)
            srb[0].SetBinContent(ibin, 1./np.sqrt(_b if _b else 1.))
        allLabs=['1/sqrt(B)']+[str(mS)+' MeV/Sqrt(B)' for mS in mSs]
        plot(smrName+'_'+pname+'_logx_srb',srb,
             labs=allLabs, logx=1, fcolz=[18], toptext=toptext,
             ytitle='S/sqrt(B)', ymax=100, dopt='hist',legstyle=legsty)
        plot(smrName+'_'+pname+'_logxy_srb',srb,
             labs=allLabs, logx=1, logy=1, ymin=0.001, ymax=1000, fcolz=[18], toptext=toptext,
             ytitle='S/sqrt(B)', dopt='hist',legstyle=legsty)
        # compute coupling reach
        # if pname == 'mass1lx':
        if True: #pname == 'mass1lx':
            srbTarget=2
            xvals, yvals = [],[]
            for _srb in srb[1:]:
                mS = int(_srb.GetName().split('_')[0])
                refReach = _srb.GetMaximum()
                maxReach = (np.sqrt(srbTarget/refReach) * gSref if refReach else 1.)
                print (mS, gSref, maxReach)
                xvals.append(mS)
                yvals.append(maxReach)
            # print(len(xvals),xvals, yvals)
            g = ROOT.TGraph(len(xvals),array('d',xvals), array('d',yvals))
            g.SetName(smrName+'_'+pname+'_reach')
            if 'yields_pz5' in g.GetName() and 'lx2' in g.GetName():
                gs[g.GetName()] = g
            # if 'lx2' in g.GetName():
            #     gs[g.GetName()] = g
# print( gs)

# ([70.24103610412794, 196.16143792435946, 462.1391138727753, 1000, 3246.1130182667275, 5964.4195055310365, 11853.964884161176] , [0.0006612646932204835, 0.0009938458643623858, 0.0015888115417895718, 0.002769231412412844, 0.006990432096802956, 0.011596933412770474, 0.020975668833025943])

# ([70.24103610412794, 200.0489902606505, 1000, 3420.5103516713175, 6451.476072880001, 11853.964884161176] , [0.00039859898918456527, 0.0005990732017020341, 0.001648762787759438, 0.004319055054118019, 0.007344322559292381, 0.012488628456704353])

gLo = ROOT.TGraph(6,array('d',[70.24103610412794, 200.0489902606505, 1000.0, 3420.5103516713175, 6451.476072880001, 11853.964884161176]),array('d',[0.00039859898918456527,0.0005990732017020341,0.001648762787759438,0.004319055054118019,0.007344322559292381,0.012488628456704353]))
gLo.SetName('g-2 lower')
gHi = ROOT.TGraph(7,array('d',[70.24103610412794, 196.16143792435946, 462.1391138727753, 1000.0, 3246.1130182667275, 5964.4195055310365, 11853.964884161176]),array('d',[0.0006612646932204835,0.0009938458643623858,0.0015888115417895718,0.002769231412412844,0.006990432096802956,0.011596933412770474,0.020975668833025943]))
gHi.SetName('g-2 upper')
gLo.SetLineColor(8)
gHi.SetLineColor(8)
gs['g2 lo'] = gLo
gs['g2 hi'] = gHi

plotGraphs('reach', [gs[x] for x in gs],
           xtitle='mS [MeV]', ytitle='gS',
           legcoors=(0.7,0.6,0.88,0.9),
           xlims=None, ymin=0, ymax=None, legcols=1,
           logy=True, logx=True, colz=None, styz=None, dopt='AL*')

## SHAPES
for smrName, smrPfx in [('comp',''),('comp_smr','s_'),('comp5','w_'),('comp5_smr','s_w_'),('comp5frac0p3_smr','s_w2_')]:#,('comp5frac0p3Pt1_smr','s_w3_')]:
    for pname in pnames:
        plot(smrName+'_'+pname,[h[t+'_'+smrPfx+pname] for t in allTags],
             labs=allLabs, rescale='norm', fcolz=[18],
             ytitle='event fraction', dopt='hist',legstyle=legsty)
        
# Fewer signals for the paper
pdir='plots/paper/'
mSs=[220,500,1000,3000]
legsty=['f']+['l' for x in mSs]
allTags=['b']+[str(x) for x in mSs]
allLabs=['Background']+[str(mS)+' MeV' for mS in mSs]
pnames=['drr1','mass1lo','pair1_Mfrac','pair1_m1frac',
        'pm1_frac','pm2_frac', 'pM_frac', 'ptm1_frac','ptm2_frac', 'ptM_frac', # rel to beam
        'pair1z1fracP' # rel to S(mm)
        ]
for smrName, smrPfx in[ ('comp',''),  ('comp5','w_'), ('comp5_smr','s_w_')]:
    for pname in pnames:
        plot(smrName+'_'+pname,[h[t+'_'+smrPfx+pname] for t in allTags],
             labs=allLabs, rescale='norm', fcolz=[18], pdir=pdir,
             ytitle='event fraction', dopt='hist',legstyle=legsty)
        for t in allTags:
            dumpToTxt(pdir+'/txt/'+smrName+'_'+pname+'_'+t, h[t+'_'+smrPfx+pname])

# plot('p1Frac_comp',[h[str(mS)+'_pm1_frac'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],
#      rescale='norm',
#      ytitle='event fraction',xtitle='p_{#mu+}/p_{Beam}',dopt='hist',legstyle='l')
# plot('minFrac_comp',[h[str(mS)+'_minp_frac'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],
#      rescale='norm',
#      ytitle='event fraction',xtitle='min(p_{#mu+},p_{#mu-})/p_{Beam}',dopt='hist',legstyle='l')

# fh = ROOT.TFile('beamTemplates.root','read')
# hpz = fh.Get('pz')
# fout.cd()
# hpzc = hpz.Clone('cumul_pz_beam')
# #hpzc.SetDirectory(fout)

# #tot = hpz.Integral()
# tot = hpz.Integral(1,hpz.GetNbinsX()+1)
# print('tot',tot)
# for i in range(1,hpz.GetNbinsX()+1):
#     print('{} : {}/{} = {}'.format(i, hpz.Integral(i,hpz.GetNbinsX()+1), tot, hpz.Integral(i,hpz.GetNbinsX()+1)/tot))
#     hpzc.SetBinContent(i, hpz.Integral(i,hpz.GetNbinsX()+1) / tot)
#     hpzc.SetBinError(i, 0)

# for mS in mSs:
#     hfrac = h[str(mS)+'_minp_frac']
#     hmin = h[str(mS)+'_minp_x_beam']
#     for i in range(1,hpz.GetNbinsX()+1):
#         for j in range(1,hfrac.GetNbinsX()+1):
#             ax = hpz.GetBinCenter(i)
#             ay = hpz.GetBinContent(i)
#             bx = hfrac.GetBinCenter(j)
#             by = hfrac.GetBinContent(j)
#             hmin.Fill(ax*bx, ay*by)
#     hc = h[str(mS)+'_minp_x_beam_cumul']
#     tot = hmin.Integral()
#     for i in range(1,hmin.GetNbinsX()+1):
#         hc.SetBinContent(i, hmin.Integral(i,hmin.GetNbinsX()+1) / tot)
    

    
# plot('minp_comp',[h[str(mS)+'_minp_x_beam'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],
#      ytitle='events',xtitle='min(p_{#mu+},p_{#mu-})',dopt='hist',legstyle='l')
# plot('minp_comp_log',[h[str(mS)+'_minp_x_beam'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],
#      ytitle='events',xtitle='min(p_{#mu+},p_{#mu-})',dopt='hist',legstyle='l',
#      logy=1,ymin=0.8)

# plot('minp_comp_cumul',[h[str(mS)+'_minp_x_beam_cumul'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],
#      ytitle='Fraction of events with min(p)>X',xtitle='min(p_{#mu+},p_{#mu-})',dopt='hist',legstyle='l')
# plot('minp_comp_cumul_log',[h[str(mS)+'_minp_x_beam_cumul'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],
#      ytitle='Fraction of events with min(p)>X',xtitle='min(p_{#mu+},p_{#mu-})',dopt='hist',legstyle='l',
#      logy=1,ymin=1e-8)
# plot('minp_comp_cumul_zoom_log',[h[str(mS)+'_minp_x_beam_cumul'] for mS in mSs],
#      labs=[str(mS)+' MeV' for mS in mSs],xlims=(0,20),
#      ytitle='Fraction of events with min(p)>X',xtitle='min(p_{#mu+},p_{#mu-})',dopt='hist',legstyle='l',
#      logy=1,ymin=1e-3)

for g in gs: gs[g].Write()
fout.Write()
fout.Close()
