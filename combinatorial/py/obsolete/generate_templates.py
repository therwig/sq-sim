'''
This file generates templates of muons from proton decay that may enter the 'mu+s->3mu' SR in SQ 
'''
import ROOT
import numpy as np
r = ROOT.TRandom3(2022)
from constants import *
from particle import part
from rand import get_eloss, smear_angle, getScatterAngle1d
from HistHelper import HistHelper
from plotUtils import *

    
class hists(HistHelper):
    def bookMu(self, tag):
        h.book(tag+'_x',   ';x [cm]',       40,-2,2)
        h.book(tag+'_xHi',   ';x [cm]',       50,-50,50)
        h.book(tag+'_xHi2',   ';x [cm]',       60,-150,150)
        h.book(tag+'_y',   ';y [cm]',       40,-2,2)
        h.book(tag+'_yHi',   ';y [cm]',       40,-150,150)
        h.book2d(tag+'_xy',';x [cm];y [cm]',40,-2,2,40,-2,2)
        h.book2d(tag+'_xyHi',';x [cm];y [cm]',40,-50,50,40,-50,50)
        h.book(tag+'_z',   ';z [cm]',       51,0,510)
        h.book(tag+'_px',  ';p_{x} [GeV]',  40,-2,2)
        h.book(tag+'_pxHi',  ';p_{x} [GeV]',  40,-10,10)
        h.book(tag+'_py',  ';p_{y} [GeV]',  40,-2,2)
        h.book(tag+'_pyHi',  ';p_{y} [GeV]',  40,-10,10)
        h.book(tag+'_pz',  ';p_{z} [GeV]',  40,0,40)
    def fillMu(self, tag,mu):
        h.fill(tag+'_x', mu.x())
        h.fill(tag+'_xHi', mu.x())
        h.fill(tag+'_xHi2', mu.x())
        h.fill(tag+'_y', mu.y())
        h.fill(tag+'_yHi', mu.y())
        h.fill(tag+'_xy',mu.x(),mu.y())
        h.fill(tag+'_xyHi',mu.x(),mu.y())
        h.fill(tag+'_z', mu.z())
        h.fill(tag+'_px',mu.px())
        h.fill(tag+'_pxHi',mu.px())
        h.fill(tag+'_py',mu.py())
        h.fill(tag+'_pyHi',mu.py())
        h.fill(tag+'_pz',mu.pz())
    def save(self, f):
        for hn in self.d:
            h = self.d[hn]
            h.SetDirectory(f)
            h.Write()
h = hists()
tags = ['initial','initialP','initialM',
        'final','finalP','finalM',
        'final20', 'final20P','final20M']
for tag in tags:
    h.bookMu(tag)

nTryPerEvt=1
with open('genmuons_protons.csv','r') as f:
    for il, l in enumerate(f):
        if il==0: continue
        # if il==20000: break
        if il and il%(100000)==0: print('processing event',il)
        # initial momenta and position
        px,py,pz,pdgId = [float(p) for p in l.split(',')[:4]]
        # if pz<20: continue
        px, py = 0, 0
        pz_initial = pz
        for iTry in range(nTryPerEvt):
            # x,y=99,99
            # while abs(x)>2*cm : x = r.Gaus(0,beam_sigma_xy)
            # while abs(y)>2*cm : y = r.Gaus(0,beam_sigma_xy)
            x, y = 0, 0
            z = r.Exp(fe_nucl_int)
            mu = part(x=x,y=y,z=z,px=px,py=py,pz=pz,pdgId=pdgId)
            h.fillMu('initial',mu)
            h.fillMu('initialP',mu) if mu.pdgId > 0 else h.fillMu('initialM',mu)
            ### Propagate
            ###
            nSteps=1
            dzStep = (dump_len-z)/nSteps
            xs=[x]
            for iStep in range(nSteps):
                # energy loss (de/dx)
                eloss = get_eloss(r, dz=dzStep)
                mu.rescale(mu.p()-eloss)
                if not mu.p()>0: continue

                # rotate beam in field. half now + half later to propogate in x according to the midpoint
                mu.BendX(dp=fmag_dp/nSteps/2.)

                # scatter and propagate position
                if mu.pz():
                    # jackson and pdg appear to diagree on 1/2 vs 1/sqrt(3) ?
                    # dAngle = getScatterAngle1d(mu,dzStep/fe_rad_len)
                    new_x = dzStep * mu.px()/mu.pz() + dzStep * getScatterAngle1d(mu,dzStep/fe_rad_len)
                    new_y = dzStep * mu.py()/mu.pz() + dzStep * getScatterAngle1d(mu,dzStep/fe_rad_len)
                    mu.pos.SetX( new_x )
                    mu.pos.SetY( new_y )
                    xs.append(new_x)
                mu.pos.SetZ( z + dzStep*(iStep+1) )
                
                # second half of beam rotation
                mu.BendX(dp=fmag_dp/nSteps/2.)
                
                # scatter
                # dtheta_x = smear_angle(r, mu.e(), dzStep/fe_rad_len )
                # dtheta_y = smear_angle(r, mu.e(), dzStep/fe_rad_len )
                # dtheta_x = r.Gaus(0, mu.smear_theta_pdg(dzStep/fe_rad_len) )
                # dtheta_y = r.Gaus(0, mu.smear_theta_pdg(dzStep/fe_rad_len) )
                # mu.add_theta_x(dtheta_x)
                # mu.add_theta_y(dtheta_y)

                # print ( dzStep/fe_rad_len, mu.smear_theta_pdg(dzStep/fe_rad_len), )
            #print( ['{:.3f} '.format(x) for x in xs] )
                
                # dx_orig = dzStep * mu.px()/mu.pz()
                # dx =  r.Gaus(0, mu.smear_theta_pdg(dzStep/fe_rad_len) )
                # dx = dx * dzStep # dx/dz = tan(t0) ~ sin(t0) ~ t0
                # if 0:
                #     print ('initial pz',pz_initial, mu.p())
                #     print ('dz orig', dx_orig, dx , dzStep , mu.px(), mu.pz())
                
                
                # dpx = (41.2+6.36*np.log(e/MeV))*MeV
                # print( mu.smear_theta_pdg(dzStep/fe_rad_len) )
                
                # if mu.pz():
                #     mu.pos.SetX( mu.x() + dzStep * mu.px()/mu.pz() )
                #     mu.pos.SetY( mu.y() + dzStep * mu.py()/mu.pz() )
                # mu.pos.SetZ( z + dzStep*(iStep+1) )
                
            if mu.pz() > min_pair_mu_p:
                h.fillMu('final',mu)
                h.fillMu('finalP',mu) if mu.pdgId > 0 else h.fillMu('finalM',mu)
                if pz_initial > 20:
                    h.fillMu('final20',mu) 
                    h.fillMu('final20P',mu) if mu.pdgId > 0 else h.fillMu('final20M',mu)
               
        # # do dedx first to terminate stopped muons early
        # eloss = get_eloss(r, dz=dump_len-z)
        # if eloss > mu.p():
        #     continue
        # # rotate beam in field
        # mu.BendX(dp=fmag_dp)
        # # scatter
        # dtheta_x = smear_angle(r, mu.e(), dump_len/fe_rad_len)
        # dtheta_y = smear_angle(r, mu.e(), dump_len/fe_rad_len)
        # mu.add_theta_x(dtheta_x)
        # mu.add_theta_y(dtheta_y)
        # # propagate
        # mu.pos.SetX( mu.x() + (dump_len-mu.z())*mu.px()/mu.pz() )
        # mu.pos.SetY( mu.y() + (dump_len-mu.z())*mu.py()/mu.pz() )
        # mu.pos.SetZ( dump_len )
        # # energy loss
        # mu.rescale(mu.p()-eloss)
        
        # h.fillMu('final',mu)
        # h.fillMu('finalP',mu) if mu.pdgId > 0 else h.fillMu('finalM',mu)

labs = ['initial #mu+' ,'initial #mu-']
plot('initial_x',   [h['initialP_x'],h['initialM_x']],labs=labs)
plot('initial_px',  [h['initialP_px'],h['initialM_px']],labs=labs)
#plot('initial_xHi', [h['initialP_xHi'],h['initialM_xHi']],labs=labs)
#plot('initial_pxHi',[h['initialP_pxHi'],h['initialM_pxHi']],labs=labs)
#plot('final_x',   [h['finalP_x'],h['finalM_x']],labs=labs)

labs = ['final #mu+','final #mu-']
plot('final_x', [h['finalP_x'],h['finalM_x']],labs=labs)
plot('final_xHi', [h['finalP_xHi'],h['finalM_xHi']],labs=labs)
plot('final_xHi2', [h['finalP_xHi2'],h['finalM_xHi2']],labs=labs)
plot('final_px',  [h['finalP_px'], h['finalM_px']],labs=labs)
plot('final_pxHi',[h['finalP_pxHi'],h['finalM_pxHi']],labs=labs)

labs = ['initial #mu','final #mu']
plot('pz',  [h['initial_pz'],h['final_pz']],labs=labs)

legtitle = 'final #mu, p_{z,initial}>20 GeV'
labs = ['final #mu+','final #mu-']
plot('final20_xHi', [h['final20P_xHi'],h['final20M_xHi']],legtitle=legtitle,labs=labs)
plot('final20_xHi2', [h['final20P_xHi2'],h['final20M_xHi2']],legtitle=legtitle,labs=labs)

labs = ['all final #mu','final #mu with p_{z,initial}>20 GeV']
plot('finalComp_xHi', [h['final_xHi'],h['final20_xHi']],labs=labs)
plot('finalComp_xHi2', [h['final_xHi2'],h['final20_xHi2']],labs=labs)
# plot('comp_x',[h['finalP_px'],h['finalM_px']],labs=labs)
        
fout = ROOT.TFile('inputs.root','recreate')
h.save(fout)
fout.Close()

# print('found {} muons, of which {} ({}-, {}+) pass pz > {} GeV'.format(len(real_pis_all), len(real_pis),
#                                                                        len(real_pims), len(real_pips),
#                                                                        high_pz_cut))
# muon_sim_fraction =  len(real_pis)/float(len(real_pis_all))
# print('muon_sim_fraction', muon_sim_fraction)
        
