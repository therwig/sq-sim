import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')

from HistHelper import HistHelper
from plotUtils import *

# f = ROOT.TFile('data/final_events_noSkim.root','read')
f = ROOT.TFile('data/pseudo120/final_events_noSkim.root','read')
t = f.Get('Events')

h = HistHelper()
h.book('xdiff',';max_{#mu}(x) - min_{#mu}(x) [cm];entries',50,0,50)
# h.book('x_all',';x[cm];entries',40,10,50)
# h.book('dxScatter',';dx from scattering [cm];entries',60,-50,250)
# h.book('dxBeam',';dx from p_{x}(beam) [cm];entries',60,-40,120)
# h.book('dxBfield',';dx from B field [cm];entries',40,-400,0)
# h.book('x_hiScatter',';x[cm];entries',40,10,50)
# h.book('x_loScatter',';x[cm];entries',40,10,50)

t.Draw('xdiff>>xdiff','')

pdir='plots/events/pseudo120/'
for n in ['xdiff']:
    plot('noskim_'+n, [h[n]],labs='none', pdir=pdir, dopt='hist')

f.Close()

############

# f = ROOT.TFile('data/final_events_xdiff20.root','read')
f = ROOT.TFile('data/pseudo120/final_events_xdiff3.root','read')
#f = ROOT.TFile('data/pseudo60/final_events_skim.root','read')
t = f.Get('Events')

# h.book('minpz_xd3',';min_{#mu}(p_{z}) [GeV];entries',50,0,50)
h.book('vx',';vertex x [cm];entries',50,0,50)
h.book('minmass',';min m(#mu+#mu-) [GeV];entries',40,0,8)
h.book('minmass_lo',';min m(#mu+#mu-) [GeV];entries',40,0,2)
h.book('maxmass',';max m(#mu+#mu-) [GeV];entries',40,0,8)
h.book('maxmass_lo',';max m(#mu+#mu-) [GeV];entries',40,0,2)

t.Draw('vx>>vx','xdiff<3')
t.Draw('min(m1n,m2n)>>minmass','xdiff<3')
t.Draw('min(m1n,m2n)>>minmass_lo','xdiff<3')
t.Draw('max(m1n,m2n)>>maxmass','xdiff<3')
t.Draw('max(m1n,m2n)>>maxmass_lo','xdiff<3')

for n in ['vx','minmass','minmass_lo']:
    plot('xdiff3_'+n, [h[n]],labs='none', pdir=pdir, dopt='hist')
    plot('xdiff3_'+n+'_log', [h[n]],labs='none', pdir=pdir, dopt='hist', logy=True, ymin=0.8)

plot('xdiff3_masses', [h['minmass'],h['maxmass']],labs=['min m(#mu#mu)','max m(#mu#mu)'], xtitle='m(#mu#mu) [GeV]',
     pdir=pdir, dopt='')
plot('xdiff3_masses_log', [h['minmass'],h['maxmass']],labs=['min m(#mu#mu)','max m(#mu#mu)'], xtitle='m(#mu#mu) [GeV]',
     pdir=pdir, dopt='', logy=True, ymin=0.8)

f.Close()
