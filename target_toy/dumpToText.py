import ROOT

def dumpToTxt(fname, h, lims=None):
    f = open(fname+'.txt','w')
    for i in range(1,h.GetNbinsX()+1):
        x = h.GetBinCenter(i)
        y = h.GetBinContent(i)
        if lims and (x<lims[0] or x>lims[1]): continue
        f.write('{} {}\n'.format(x,y))
    f.close()
def dumpToTxtG(fname, g):
    f = open(fname+'.txt','w')
    for i in range(g.GetN()):
        x = g.GetX()[i]
        y = g.GetY()[i]
        f.write('{} {}\n'.format(x,y))
    f.close()

f = ROOT.TFile.Open('histdump.root')
x0s = ['1','5','10','20','50','100']

for x0 in x0s:
    h = f.Get('h_'+x0)
    dumpToTxt('plots/txt/thickness_mass_'+x0, h, lims=(0,2))
    g = f.Get(x0)
    dumpToTxtG('plots/txt/thickness_srb_'+x0, g)

f.Close()
