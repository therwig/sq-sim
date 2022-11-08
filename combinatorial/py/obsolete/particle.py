import ROOT
import numpy as np
from constants import *

class part:
    def __init__(self, px=0,py=0,pz=0,x=0,y=0,z=0,m=105*MeV,pdgId=0):
        self.p4 = ROOT.Math.PxPyPzMVector()
        self.p4.SetCoordinates(px,py,pz,m)
        self.pos = ROOT.TVector3(x,y,z)
        self.pdgId=pdgId
    def pt(self): return self.p4.pt()
    def p(self): return self.p4.P()
    def e(self): return self.p4.e()
    def px(self): return self.p4.Px()
    def py(self): return self.p4.Py()
    def pz(self): return self.p4.Pz()
    def x(self): return self.pos.x()
    def y(self): return self.pos.y()
    def z(self): return self.pos.z()
    def dxy(self, p2): return (self.pos - p2.pos).Pt() #np.hypot(self.x-p2.x,self.y-p2.y)
    def rescale(self, pnew): 
        if pnew<=0:
            self.p4.SetCoordinates(0,0,0,0)
            self.pos.SetXYZ(0,0,0)
            return
        ptot = self.p()
        self.p4.SetPx( self.p4.Px() * pnew / ptot)
        self.p4.SetPy( self.p4.Py() * pnew / ptot)
        self.p4.SetPz( self.p4.Pz() * pnew / ptot)
        return
    def add_theta_x(self, delta_t):
        x, z = self.pos.x(),self.pos.z()
        p2 = np.hypot(x,z)
        t = np.arctan(x / z) if z>0 else 0
        t += delta_t
        self.pos.SetX( p2 * np.sin(t) )
        self.pos.SetZ( p2 * np.cos(t) )
    def add_theta_y(self, delta_t):
        y, z = self.pos.y(),self.pos.z()
        p2 = np.hypot(y,z)
        t = np.arctan(y / z) if z>0 else 0
        t += delta_t
        self.pos.SetY( p2 * np.sin(t) )
        self.pos.SetZ( p2 * np.cos(t) )
    def smear_theta_pdg(self, x0):
        beta = self.p4.Beta()
        return 13.6*MeV / (beta * self.p()) * np.sqrt(x0) * (1 + 0.038 * np.log(x0  / (beta*beta)))
    def smear_theta_pdg_new(self, r, x0, z):
        beta = self.p4.Beta()
        t0 = 13.6*MeV / (beta * self.p()) * np.sqrt(x0) * (1 + 0.038 * np.log(x0  / (beta*beta)))
        z1 = r.Gaus(0,1)
        z2 = r.Gaus(0,1)
        yplane = z1 * z * t0 / np.sqrt(12) + z2 * z * t0 / 2
        tplane = z2 * t0
        Phiplane = np.arctan(yplane / z) if z>0 else 0
        return Phiplane * np.sin(tplane), Phiplane * np.cos(tplane)
    def BendX(self,dp=0):
        px = self.p4.Px()
        pz = self.p4.Pz()
        px2 = px - dp * np.sign(self.pdgId) 
        pz2 = np.sqrt(max(1*MeV*MeV,pz*pz+px*px-px2*px2))
        self.p4.SetPx(px2)
        self.p4.SetPz(pz2)
    def __repr__(self): 
        return "Part (x,y,z)=({:.2f},{:.2f},{:.2f}) cm, ".format(self.pos.x()*cm,self.pos.y()*cm,self.pos.z()*cm) + \
                "(px,py,pz)=({:.2f},{:.2f},{:.2f}) GeV".format(self.p4.Px()*GeV,self.p4.Py()*GeV,self.p4.Pz()*GeV)
def mass(a,b):
    return (a.p4+b.p4).M()
