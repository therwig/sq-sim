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

eBeam=20
MoT=5e13
lumi = 1e-36 * 7.874 * 6.022e23 / 55.845 * 100 * MoT # for 5e13 MoT, 1m target, in 1/pb
nBkgd = 3.187970E+05 * lumi
print("With this setup, we expect to have",nBkgd,"background events in total.")

nSig={}
nSig[1000]=6.634621E+05 
nSig[2000]=1.009877E+04
nSig[220]=5.343163E+07 #* 0.2 # scale down to DRAW!
nSig[3000]=3.045280E+02
nSig[300]=2.842917E+07
nSig[4000]=1.762285E+01
nSig[400]=1.449005E+07
nSig[500]=7.971065E+06 
nSig[600]=4.608885E+06
nSig[700]=2.753382E+06 
nSig[800]=1.686569E+06
nSig[900]=1.050958E+06
for m in nSig: nSig[m] = nSig[m] * m/220 * m/220
gSref=1e-2
for x in nSig: nSig[x] = nSig[x] * lumi * gSref * gSref
print("With this setup, we expect to have",nSig[220],"signal events with 220 MeV mass.")
print("With this setup, we expect to have",nSig[500],"signal events with 500 MeV mass.")
print("With this setup, we expect to have",nSig[1000],"signal events with 1 GeV mass.")

ROOT.gROOT.ProcessLine(".L plotter/helpers.C+")
ROOT.load_f5()

fout = ROOT.TFile('hist.root','recreate')
mSs=[220,300,400,500,600,700,800,1000,2000,3000,4000]
mSs=[220,300,400,500,700,1000]
h = HistHelper()

weights={}
weights['']='(massBest-mass1)<1e-8'
weights['pz5_']='{smr}m1z>5 && {smr}Mz>5 && (massBest-mass1)<1e-8'
wns = weights.keys()

for mS in mSs+['b']:
    for smr in ['','s_']:
        for wn in wns: # ['','w_','w2_']:
            pfx=smr+wn            
            bins = np.exp(np.linspace(np.log(0.200), np.log(1.2), 60))
            # bins = np.exp(np.linspace(np.log(0.200), np.log(2.2), 160))
            h.bookBins(str(mS)+'_'+pfx+'mass',';m(#mu^{-}_{1},#mu^{+}) [GeV];',bins)

nEntries={}
dataDir = 'data/'
for mS in mSs+['b']:
    if mS == 'b':
        f = ROOT.TFile.Open(dataDir+'/20GeVBeamBg.root','r')
        t = f.Get('Events')
        t.AddFriend('Friends',dataDir+'/20GeVBeamBg_Friend.root')
    else:
        f = ROOT.TFile.Open(dataDir+'/20GeVBeam/mS{}MeV20_decayed.root'.format(mS),'r')
        t = f.Get('Events')
        t.AddFriend('Friends',dataDir+'/20GeVBeam/mS{}MeV20_decayed_Friend.root'.format(mS))
    fout.cd()
    nEntries[mS]=t.GetEntries()
    for smr in ['','s_']:
        for wn in weights:
            w = weights[wn].format(eBeam=eBeam, smr=smr)
            pfx=smr+wn
            # t.Draw("{smr}massBest>>{mS}_{pfx}mass".format(mS=mS, smr=smr, pfx=pfx),w)
            t.Draw("{smr}massBest>>{mS}_{pfx}mass".format(mS=mS, smr=smr, pfx=pfx),w)
    
    f.Close()

legsty=['f']+['l' for x in mSs]
allTags=['b']+[str(x) for x in mSs]
allLabs=['Bkg']+[str(mS)+' MeV' for mS in mSs]

## YIELDS
# at this point, the weight is number of passing events
norms=[1./nEntries['b']]+[1./nEntries[x] for x in mSs]
norms=[nBkgd/nEntries['b']]+[nSig[x]/nEntries[x] for x in mSs]
gs={}
for smrName, smrPfx in [('yields_smr','s_'),
                        ('yields_pz5_smr','s_pz5_'),
                        # ('yields_pz5_frac0p3_smr','s_w2_'),
                        # ('yields_pz5_frac0p3_SQ_smr','s_w2_'),
                        # ('yields_pz5_frac0p3_20_smr','s_w3_'),
                        # ('yields5frac0p4_smr','s_w3_'),
                        # ('yields5frac0p5_smr','s_w4_'),
                        # ('yields5frac0p3Pt1_smr','s_w3_'),
                        # ('yields5frac0p3Pt15_smr','s_w4_'),
                        ]:
    allLabs=['Bkg']+[str(mS)+' MeV' for mS in mSs]
    pname = 'mass'
    plot(smrName+'_'+pname,[h[t+'_'+smrPfx+pname] for t in allTags],
         labs=allLabs, rescale=norms, fcolz=[18], toptext=smrName,
         ytitle='events', dopt='hist',legstyle=legsty)
    #continue
    for t in allTags: h[t+'_'+smrPfx+pname].GetXaxis().SetMoreLogLabels()
    plot(smrName+'_'+pname+'_logx',[h[t+'_'+smrPfx+pname] for t in allTags],
         labs=allLabs, logx=1, fcolz=[18], toptext=smrName,
         ytitle='events', dopt='hist',legstyle=legsty)
    plot(smrName+'_'+pname+'_logxy',[h[t+'_'+smrPfx+pname] for t in allTags],
         labs=allLabs, logx=1, logy=1, ymin=0.8, fcolz=[18], toptext=smrName,
         ytitle='events', dopt='hist',legstyle=legsty)
    plot(smrName+'_'+pname+'_logxy_bsub',[h[t+'_'+smrPfx+pname] for t in allTags],
         labs=allLabs, logx=1, logy=1, ymin=0.8, fcolz=[18], toptext=smrName,
         ytitle='events', dopt='hist',legstyle=legsty, bsub=True)
    #
    for t in allTags[1:]:
        h[t+'_'+smrPfx+pname+'_plusb'] = h[t+'_'+smrPfx+pname].Clone(t+'_'+smrPfx+pname+'_plusb')
        # print(t+'_'+smrPfx+pname+'_plusb',  h[t+'_'+smrPfx+pname+'_plusb'].Integral() )
        h[t+'_'+smrPfx+pname+'_plusb'].Add( h['b_'+smrPfx+pname] )
        dumpToTxt('plots/txt/'+t+'_'+smrPfx+pname+'_plusb',h[t+'_'+smrPfx+pname+'_plusb'])
    dumpToTxt('plots/txt/b_'+smrPfx+pname,h['b_'+smrPfx+pname])
    # plusb = [h[t+'_'+smrPfx+pname].Clone(t+'_'+smrPfx+pname+'_bbb') for t in allTags]
    # plusb = [h[t+'_'+smrPfx+pname].Clone(t+'_'+smrPfx+pname+'_bbb') for t in allTags]
    # for h in plusb[1:]:
    #     h.Add(plusb[0])
    plot(smrName+'_'+pname+'_logx_sum', [h['b_'+smrPfx+pname]]+[h[t+'_'+smrPfx+pname+'_plusb'] for t in allTags[1:]] , redrawBkg=1,
         labs=allLabs, logx=1, fcolz=[18], toptext='', ymax=2.2e6,
         ytitle='events', dopt='hist',legstyle=legsty)
    
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

# gLo = ROOT.TGraph(6,array('d',[70.24103610412794, 200.0489902606505, 1000.0, 3420.5103516713175, 6451.476072880001, 11853.964884161176]),array('d',[0.00039859898918456527,0.0005990732017020341,0.001648762787759438,0.004319055054118019,0.007344322559292381,0.012488628456704353]))
# gLo.SetName('g-2 lower')
# gHi = ROOT.TGraph(7,array('d',[70.24103610412794, 196.16143792435946, 462.1391138727753, 1000.0, 3246.1130182667275, 5964.4195055310365, 11853.964884161176]),array('d',[0.0006612646932204835,0.0009938458643623858,0.0015888115417895718,0.002769231412412844,0.006990432096802956,0.011596933412770474,0.020975668833025943]))
# gHi.SetName('g-2 upper')
# gLo.SetLineColor(8)
# gHi.SetLineColor(8)
# gs['g2 lo'] = gLo
# gs['g2 hi'] = gHi

# plotGraphs('reach', [gs[x] for x in gs],
#            xtitle='mS [MeV]', ytitle='gS',
#            legcoors=(0.7,0.6,0.88,0.9),
#            xlims=None, ymin=0, ymax=None, legcols=1,
#            logy=True, logx=True, colz=None, styz=None, dopt='AL*')

# ## SHAPES
# for smrName, smrPfx in [('comp',''),('comp_smr','s_'),('comp5','w_'),('comp5_smr','s_w_'),('comp5frac0p3_smr','s_w2_')]:#,('comp5frac0p3Pt1_smr','s_w3_')]:
#     for pname in pnames:
#         plot(smrName+'_'+pname,[h[t+'_'+smrPfx+pname] for t in allTags],
#              labs=allLabs, rescale='norm', fcolz=[18],
#              ytitle='event fraction', dopt='hist',legstyle=legsty)
        
# # Fewer signals for the paper
# pdir='plots/paper/'
# mSs=[220,500,1000,3000]
# legsty=['f']+['l' for x in mSs]
# allTags=['b']+[str(x) for x in mSs]
# allLabs=['Background']+[str(mS)+' MeV' for mS in mSs]
# pnames=['drr1','mass1lo','pair1_Mfrac','pair1_m1frac',
#         'pm1_frac','pm2_frac', 'pM_frac', 'ptm1_frac','ptm2_frac', 'ptM_frac', # rel to beam
#         'pair1z1fracP' # rel to S(mm)
#         ]
# for smrName, smrPfx in[ ('comp',''),  ('comp5','w_'), ('comp5_smr','s_w_')]:
#     for pname in pnames:
#         plot(smrName+'_'+pname,[h[t+'_'+smrPfx+pname] for t in allTags],
#              labs=allLabs, rescale='norm', fcolz=[18], pdir=pdir,
#              ytitle='event fraction', dopt='hist',legstyle=legsty)
#         for t in allTags:
#             dumpToTxt(pdir+'/txt/'+smrName+'_'+pname+'_'+t, h[t+'_'+smrPfx+pname])

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
