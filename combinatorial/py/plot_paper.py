import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')

from HistHelper import HistHelper
from plotUtils import *
pdir='plots/paper/'

h = HistHelper()

make_pz_comp = True
make_dx_comp = True
make_mass = True

def dumpToTxt(fname, h):
    f = open(fname+'.txt','w')
    for i in range(1,h.GetNbinsX()+1):
        x = h.GetBinCenter(i)
        y = h.GetBinContent(i)
        f.write('{} {}\n'.format(x,y))
    f.close()

if make_pz_comp:
    f = ROOT.TFile('data/final_muons_noSkim.root','read')
    t = f.Get('Events')
    
    h.book('init_pz',';muon p_{Z} [GeV];a.u.',40,0,40)
    h.book('final_pz',';muon p_{Z} [GeV];a.u.',40,0,40)
    t.Draw("pz>>final_pz","pz>0") #,"Entry$<10000")
    t.Draw("init_pz>>init_pz") #,"Entry$<10000")
    
    h['final_pz10'] = h['final_pz'].Clone('final_pz10')
    for i in range(0,h['final_pz10'].GetNbinsX()+2):
        if h['final_pz10'].GetXaxis().GetBinCenter(i) < 10:
            h['final_pz10'].SetBinContent(i,0)
            h['final_pz10'].SetBinError(i,0)
    
    h['final_pz10'].SetFillColor(ROOT.kRed-10)
    
    hs=[h['init_pz'],h['final_pz'],h['final_pz10']]
    # for h in hs:
    #     print(h.Integral())
    
    norm=h['init_pz'].Integral()
    h['final_pz10'].Scale( norm / h['final_pz'].Integral())
    h['final_pz'].Scale( norm / h['final_pz'].Integral())
    
    plot('pz_comparison', hs,
         labs=['Muons before traversing dump','Muons after traversing dump', 'After dump, p_{z}>10 GeV'],
         colz = [ROOT.kBlack, ROOT.kRed, ROOT.kRed],
         pdir=pdir, rescale=1./norm, legcoors=(0.55,0.6,0.88,0.85), #xlims=(0,35),
         ytitle='d#sigma/dp_{z}', dopt='hist', legstyle='f')
    
    plot('pz_comparison_log', hs,
         labs=['Muons before traversing dump','Muons after traversing dump', 'After dump, p_{z}>10 GeV'],
         colz = [ROOT.kBlack, ROOT.kRed, ROOT.kRed],
         pdir=pdir, legcoors=(0.55,0.6,0.88,0.85),
         ytitle='d#sigma/dp_{z}', logy=1, dopt='hist', legstyle='f', ymin=2e-4)
    
    dumpToTxt(pdir+'/txt/pz_beforeDump', hs[0])
    dumpToTxt(pdir+'/txt/pz_afterDump', hs[1])
    dumpToTxt(pdir+'/txt/pz_afterDump10GeV', hs[2])
    
    f.Close()
    
####
if make_dx_comp:

    f = ROOT.TFile('data/final_muons_noSkim.root','read')
    # f = ROOT.TFile('data/pseudo60/final_muons_noSkim.root','read')
    t = f.Get('Events')
    
    h.book('dx_pos',';muon x_{end of dump} [cm];a.u.',50,-50,50)
    h.book('dx_pos10',';muon x_{end of dump} [cm];a.u.',50,-50,50)
    h.book('dx_neg',';muon x_{end of dump} [cm];a.u.',50,-50,50)
    h.book('dx_neg10',';muon x_{end of dump} [cm];a.u.',50,-50,50)
    
    t.Draw("x>>dx_pos","pz>0 && pdg==-13")
    t.Draw("x>>dx_pos10","pz>10 && pdg==-13")
    t.Draw("x>>dx_neg","pz>0 && pdg==13")
    t.Draw("x>>dx_neg10","pz>10 && pdg==13")
    nall = h['dx_pos'].Integral() + h['dx_neg'].Integral()
    hs = [h['dx_pos'], h['dx_pos10'], h['dx_neg'], h['dx_neg10']]
    # for h in hs: h.Scale(h.Integral()/nall)
    
    plot('dx_comparison', hs,
         labs = ['all final #mu+','final #mu+ with p_{z}>10 GeV','all final #mu-','final #mu- with p_{z}>10 GeV'],
         colz=[ROOT.kGray, ROOT.kBlack, ROOT.kRed-9, ROOT.kRed],
         pdir=pdir, rescale=1./nall, legcoors=(0.15,0.63,0.48,0.88), #xlims=(0,35),
         ytitle='d#sigma/dx', dopt='', legstyle='l')
    plot('dx_comparison_log', hs,
         labs = ['all final #mu+','final #mu+ with p_{z}>10 GeV','all final #mu-','final #mu- with p_{z}>10 GeV'],
         colz=[ROOT.kGray, ROOT.kBlack, ROOT.kRed-9, ROOT.kRed],
         pdir=pdir, rescale=1., legcoors=(0.15,0.33,0.48,0.58), #xlims=(0,35),
         ytitle='d#sigma/dx', dopt='', legstyle='l', logy=1, ymin=2e-6)

    dumpToTxt(pdir+'/txt/dx_positive', hs[0])
    dumpToTxt(pdir+'/txt/dx_positive10GeV', hs[1])
    dumpToTxt(pdir+'/txt/dx_negative', hs[2])
    dumpToTxt(pdir+'/txt/dx_negative10GeV', hs[3])
    
    f.Close()

if make_mass:

    f = ROOT.TFile('data/pseudo120/final_events_xdiff3.root','read')
    t = f.Get('Events')
    
    h.book('m',';minimum m_{#mu^{+}#mu^{-}} [GeV];Events',100,0,10)    
    h0=h['m']
    h0.Sumw2()
    t.Draw("min(m1n,m2n)>>m","(xN>10 && xP1>10 && xP2>10)")

    f1 = ROOT.TF1( "f1", "[0]*pow(x,[1])", 1.4, 3)
    f1.SetLineColor(ROOT.kBlue)
    f1.SetLineStyle(2)
    f2 = ROOT.TF1( "f1", "[0]*pow(x,[1])", 1e-3, 3.5)
    h0.Fit(f1,'R')
    f2.SetParameter(0, f1.GetParameter(0))
    f2.SetParameter(1, f1.GetParameter(1))
    f2.SetLineColor(ROOT.kBlue)
    f2.SetLineStyle(2)
    
    c = ROOT.TCanvas()
    c.SetLogy()

    # leg = ROOT.TLegend(0.7,0.6,0.88,0.9)
    leg = ROOT.TLegend(0.4,0.2,0.8,0.4)
    leg.SetTextFont(42)
    leg.SetNColumns(1)
    leg.SetHeader("2.1 #times 10^{14} MoT Equivalent")

    h0.SetLineWidth(2)
    h0.SetLineColor(ROOT.kBlack)
    h0.SetMarkerColor(ROOT.kBlack)
    h0.Draw()
    f2.Draw('same')
    leg.AddEntry(h0,'Coincident #mu background','ple')
    leg.AddEntry(f2,'Fit (power law)','l')
    
    leg.SetFillStyle(0) 
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.Draw()
    
    h0.Draw('axis same')
    save(c, 'mass', pdir=pdir, exts=['.pdf','.eps','.png'])

    dumpToTxt(pdir+'/txt/min_mass', h0)

    f.Close()

