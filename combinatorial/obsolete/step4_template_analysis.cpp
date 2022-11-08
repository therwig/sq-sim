#include <iostream>
#include <Math/Vector4D.h>
#include "TRandom3.h"
#include "TF1.h"
#include "TH1.h"
#include "TFile.h"
#include "TTree.h"
using std::cout;
using std::endl;

#include "constants.h"

#define SKIM

#ifdef SKIM
constexpr int NTRIALS=100*1000*1000;
#elif
constexpr int NTRIALS=10*1000*1000;
#endif

void step4_analysis(){
  // Inputs
  TFile* ifi = new TFile("templates.root","read");
  TH1D* hpos = (TH1D*) ifi->Get("pos_x");
  TH1D* hneg = (TH1D*) ifi->Get("neg_x");

  // Outputs
  TFile* f = new TFile("final_events_xdiff.root","recreate");
  TTree* t = new TTree("Events","");
  float xpos1, xpos2, xneg, xdiff, vx;
  t->Branch("xpos1"  ,&xpos1  ,"xpos1/F" );
  t->Branch("xpos2"  ,&xpos2  ,"xpos2/F" );
  t->Branch("xneg"   ,&xneg   ,"xneg/F"  );
  t->Branch("xdiff"  ,&xdiff  ,"xdiff/F"  );
  t->Branch("vx"  ,&vx  ,"vx/F");

  // Utilities
  TRandom* r = new TRandom3(2022);
  
  for(int itrial=0; itrial<NTRIALS; itrial++){
    xpos1 = hpos->GetRandom(r);
    xpos2 = hpos->GetRandom(r);
    xneg = hneg->GetRandom(r);
    xdiff = std::max(std::max(xpos1, xpos2), xneg) - std::min(std::min(xpos1, xpos2), xneg);
#ifdef SKIM
    if (xdiff>20) continue;
#endif
    vx = (xpos1+xpos2+xneg)/3.;
    t->Fill();
  }
  t->Write();
  f->Close();
  ifi->Close();
  
}

int main(){
  step4_analysis();
  return 0;
}

