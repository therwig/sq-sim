#include <TFile.h>
#include <TH1.h>
#include <cmath>

void helpers(){}
float ptot(float x, float y, float z, float m=0.105){
  return sqrt(x*x + y*y + z*z + m*m);
}

TH1* hpzc;

void load_f5(){
  TFile *fh = new TFile("beamTemplates.root","read");
  auto hpz = (TH1*) fh->Get("pz");
  hpzc = (TH1*) hpz->Clone("cumul_pz_beam");
  float tot = hpz->Integral(1, hpz->GetNbinsX()+1);
 
  for (int i=1; i<=hpzc->GetNbinsX()+1; i++){
    hpzc->SetBinContent(i, hpz->Integral(i,hpz->GetNbinsX()+1) / tot);
    hpzc->SetBinError(i, 0);
  }
}

float f5(float frac){
  return hpzc->GetBinContent( hpzc->GetBin(frac) );
}
