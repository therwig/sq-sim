'''
This file generates templates of muons from proton decay that may enter the 'mu+s->3mu' SR in SQ 
'''
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

class hists(HistHelper):
    def bookMu(self, tag):
        h.book(tag+'_x',   ';x [cm]',       40,-2,2)
        h.book(tag+'_xHi',   ';x [cm]',       50,-50,50)
        h.book(tag+'_xHi2',   ';x [cm]',       60,-150,150)
        h.book(tag+'_dxScatter', ';dx scatter [cm]',  60,-150,150)
        h.book(tag+'_y',   ';y [cm]',       40,-2,2)
        h.book(tag+'_yHi',   ';y [cm]',       40,-150,150)
        h.book2d(tag+'_xy',';x [cm];y [cm]',40,-2,2,40,-2,2)
        h.book2d(tag+'_xyHi',';x [cm];y [cm]',40,-50,50,40,-50,50)
        #h.book(tag+'_z',   ';z [cm]',       51,0,510)
        h.book(tag+'_px',  ';p_{x} [GeV]',  40,-2,2)
        h.book(tag+'_pxHi',  ';p_{x} [GeV]',  40,-10,10)
        h.book(tag+'_py',  ';p_{y} [GeV]',  40,-2,2)
        h.book(tag+'_pyHi',  ';p_{y} [GeV]',  40,-10,10)
        h.book(tag+'_pz',  ';p_{z} [GeV]',  40,0,40)
    def fillMu1(self, t, tag, cut, prep=''):
        pass
        # t.Draw(prep+'px>>'+tag+'_px',cut)
        # t.Draw(prep+'px>>'+tag+'_pxHi',cut)
        # t.Draw(prep+'py>>'+tag+'_py',cut)
        # t.Draw(prep+'py>>'+tag+'_pyHi',cut)
        # t.Draw(prep+'px>>'+tag+'_pz',cut)
    def fillMu2(self, t, tag, cut, prep=''):
        # t.Draw(prep+'x>>'+tag+'_x',cut)
        t.Draw(prep+'x>>'+tag+'_xHi',cut)
        t.Draw(prep+'x>>'+tag+'_xHi2',cut)
        # t.Draw(prep+'dxScatter>>'+tag+'_dxScatter',cut)
        # t.Draw(prep+'y>>'+tag+'_y',cut)
        # t.Draw(prep+'y>>'+tag+'_yHi',cut)
        # t.Draw(prep+'y:x>>'+tag+'_xy',cut)
        # t.Draw(prep+'y:x>>'+tag+'_xyHi',cut)
        # #t.Draw(prep+'z>>'+tag+'_z',cut)
        # t.Draw(prep+'px>>'+tag+'_px',cut)
        # t.Draw(prep+'px>>'+tag+'_pxHi',cut)
        # t.Draw(prep+'py>>'+tag+'_py',cut)
        # t.Draw(prep+'py>>'+tag+'_pyHi',cut)
        # t.Draw(prep+'px>>'+tag+'_pz',cut)
    def save(self, f):
        for hn in self.d:
            h = self.d[hn]
            h.SetDirectory(f)
            h.Write()

f = ROOT.TFile('data/final_muons_noSkim.root','read')
t = f.Get('Events')

h = hists()
tags = {
    'initial' : ('init_', ''),
    'initialP' : ('init_', 'pdg<0'),
    'initialM' : ('init_', 'pdg>0'),
    'final' : ('',  'pz>0.5  '),
    'finalP' : ('', 'pz>0.5 && pdg<0'),
    'finalM' : ('', 'pz>0.5 && pdg>0'),
    'final20' : ('',  'pz>0.5  '),
    'final20P' : ('', 'pz>0.5 && init_pz>20 && pdg<0'),
    'final20M' : ('', 'pz>0.5 && init_pz>20 && pdg>0'),
}

for tag in tags:
    h.bookMu(tag)
    prep, cut = tags[tag]
    if 'initial' in tag:
        h.fillMu1(t, tag, cut, prep)
    else:
        h.fillMu2(t, tag, cut, prep)

# t.Draw('init_px>>initial_px','')
# t.Draw('init_px>>initialP_px','pdg<0')
# t.Draw('init_px>>initialM_px','pdg>0')

labs = ['initial #mu+' ,'initial #mu-']
#plot('initial_x',   [h['initialP_x'],h['initialM_x']],labs=labs)
plot('initial_px',  [h['initialP_px'],h['initialM_px']],labs=labs)

#exit(0)
#plot('initial_xHi', [h['initialP_xHi'],h['initialM_xHi']],labs=labs)
#plot('initial_pxHi',[h['initialP_pxHi'],h['initialM_pxHi']],labs=labs)
#plot('final_x',   [h['finalP_x'],h['finalM_x']],labs=labs)

labs = ['all final #mu+','all final #mu-']
plot('final_x', [h['finalP_x'],h['finalM_x']],labs=labs)
plot('final_xHi', [h['finalP_xHi'],h['finalM_xHi']],labs=labs)
plot('final_xHi2', [h['finalP_xHi2'],h['finalM_xHi2']],labs=labs)
plot('final_xHi2_log', [h['finalP_xHi2'],h['finalM_xHi2']],labs=labs, logy=True, ymin=0.8)
plot('final_px',  [h['finalP_px'], h['finalM_px']],labs=labs)
plot('final_pxHi',[h['finalP_pxHi'],h['finalM_pxHi']],labs=labs)

labs = ['initial #mu','final #mu']
plot('pz',  [h['initial_pz'],h['final_pz']],labs=labs)

legtitle = 'final #mu, p_{z,initial}>20 GeV'
labs = ['final #mu+','final #mu-']
plot('final20_xHi', [h['final20P_xHi'],h['final20M_xHi']],legtitle=legtitle,labs=labs)
plot('final20_xHi2', [h['final20P_xHi2'],h['final20M_xHi2']],legtitle=legtitle,labs=labs)
plot('final20_xHi2_log', [h['final20P_xHi2'],h['final20M_xHi2']],legtitle=legtitle,labs=labs, logy=True, ymin=0.8)

labs = ['all final #mu','final #mu with p_{z,initial}>20 GeV']
plot('finalComp_xHi', [h['final_xHi'],h['final20_xHi']],labs=labs)
plot('finalComp_xHi2', [h['final_xHi2'],h['final20_xHi2']],labs=labs)
plot('finalComp_dxScatter', [h['final_dxScatter'],h['final20_dxScatter']],labs=labs)
plot('finalComp_dxScatter_log', [h['final_dxScatter'],h['final20_dxScatter']],labs=labs, logy=True, ymin=0.8)
# plot('comp_x',[h['finalP_px'],h['finalM_px']],labs=labs)

labs = ['all final #mu+','final #mu+ with p_{z,initial}>20 GeV','all final #mu-','final #mu- with p_{z,initial}>20 GeV']
colz=[ROOT.kGray, ROOT.kBlack, ROOT.kRed-9, ROOT.kRed]
#print('finalCompPM_xHi', [h['finalP_xHi'],h['final20P_xHi'],h['finalM_xHi'],h['final20M_xHi']], labs=labs)
plot('finalCompPM_xHi', [h['finalP_xHi'],h['final20P_xHi'],h['finalM_xHi'],h['final20M_xHi']],labs=labs, colz=colz)
plot('finalCompPM_xHi2', [h['finalP_xHi2'],h['final20P_xHi2'],h['finalM_xHi2'],h['final20M_xHi2']],labs=labs, colz=colz)


f.Close()

# fout = ROOT.TFile('inputs.root','recreate')
# h.save(fout)
# fout.Close()

# print('found {} muons, of which {} ({}-, {}+) pass pz > {} GeV'.format(len(real_pis_all), len(real_pis),
#                                                                        len(real_pims), len(real_pips),
#                                                                        high_pz_cut))
# muon_sim_fraction =  len(real_pis)/float(len(real_pis_all))
# print('muon_sim_fraction', muon_sim_fraction)
        
