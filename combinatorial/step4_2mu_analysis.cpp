#include <iostream>
#include <Math/Vector4D.h>
#include "TRandom3.h"
#include "TF1.h"
#include "TH1.h"
#include "TFile.h"
#include "TTree.h"
// #include "TEntryList.h"
#include "TEventList.h"
using std::cout;
using std::endl;

#include "constants.h"

//constexpr int NTRIALS_PER_EVENT=5000;
//constexpr int NTRIALS_PER_EVENT=2; // 1863331 events in 3.2 min (xdiff<20)
//constexpr int NTRIALS_PER_EVENT=10; // 18581988 events in 33.5 min (xdiff<20)
// xdiff<20 is 0.23822961 of all events

// bugfix
// constexpr int NTRIALS_PER_EVENT=1000; // 1000 * 1573586/4 events in 3.2 min (xdiff<20)
// constexpr int NTRIALS_PER_EVENT=15000;
//25min

constexpr int NTRIALS_PER_EVENT=2;

void step2_initial_to_final(const char* suffix="", int minEvt=0, int maxEvt=-1){
  // Inputs
  // Access mu+ values
  TFile* ifi1 = new TFile("data/final_muons_noSkim.root","read");
  TTree* it1 = (TTree*) ifi1->Get("Events");
  float x1, y1, px1, py1, pz1;
  int pdg1;
  it1->SetBranchAddress("x",&x1);
  it1->SetBranchAddress("y",&y1);
  it1->SetBranchAddress("px",&px1);
  it1->SetBranchAddress("py",&py1);
  it1->SetBranchAddress("pz",&pz1);
  it1->SetBranchAddress("pdg",&pdg1);
  float t1_skim_factor = 1.;

  // Access mu- values
  TFile* ifi2 = new TFile("data/final_muons_noSkim.root","read");
  TTree* it2 = (TTree*) ifi2->Get("Events");
  float x2, y2, px2, py2, pz2;
  int pdg2;
  it2->SetBranchAddress("x",&x2);
  it2->SetBranchAddress("y",&y2);
  it2->SetBranchAddress("px",&px2);
  it2->SetBranchAddress("py",&py2);
  it2->SetBranchAddress("pz",&pz2);
  it2->SetBranchAddress("pdg",&pdg2);
  float t2_skim_factor = 4.07e-5;
  
  // helpers
  ROOT::Math::PxPyPzMVector pos;
  ROOT::Math::PxPyPzMVector neg;

  
  // Preselect events to consider
  // it1->Draw(">>elist","pdg==-13 && x>10 && x<50 && pz>5");
  // it1->Draw(">>elist","x>10 && x<50 && pz>5 && pdg==-13 && fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40");  
  it1->Draw(">>elist","fabs(y)<50 && x>10 && x<50 && pz>5 && pdg==-13");
  TEventList *elist1 = (TEventList*) ((TEventList*) gDirectory->Get("elist"))->Clone("elist1");
  it1->SetEventList(elist1);

  // it2->Draw(">>elist","x>10 && x<50 && pz>5 && pdg==13 && fabs(x+(px/pz)*0.9)<40 && fabs(y+(py/pz)*0.9)<40");
  it2->Draw(">>elist","fabs(y)<50 && x>10 && x<50 && pz>5 && pdg==13");
  TEventList *elist2 = (TEventList*) gDirectory->Get("elist");
  it2->SetEventList(elist2);

  cout << "found " << elist1->GetN() << " and " << elist2->GetN() << " events" << endl;
  
  // Outputs
  TFile* f = new TFile(TString::Format("final_events%s.root",suffix),"recreate");
  TTree* t = new TTree("Events","");
  // float x1, y1, px1, py1, pz1;
  // float x2, y2, px2, py2, pz2, m;
  float m;
  t->Branch("x1"  ,&x1  ,"x1/F"  );
  t->Branch("y1"  ,&y1  ,"y1/F"  );
  t->Branch("px1" ,&px1 ,"px1/F" );
  t->Branch("py1" ,&py1 ,"py1/F" );
  t->Branch("pz1" ,&pz1 ,"pz1/F" );
  t->Branch("x2"  ,&x2  ,"x2/F"  );
  t->Branch("y2"  ,&y2  ,"y2/F"  );
  t->Branch("px2" ,&px2 ,"px2/F" );
  t->Branch("py2" ,&py2 ,"py2/F" );
  t->Branch("pz2" ,&pz2 ,"pz2/F" );
  // float xdiff, vx, m1n, m2n;
  // t->Branch("xdiff"  ,&xdiff  ,"xdiff/F"  );
  // t->Branch("vx"  ,&vx  ,"vx/F");
  // t->Branch("m1n"  ,&m1n  ,"m1n/F");
  t->Branch("m"  ,&m  ,"m/F");
  
  const long n1 = elist1->GetN();
  const long n2 = elist2->GetN();
  const long MAX=1e5;
  
  // load smaller set into memory
  std::vector<float> xx( n2 );
  std::vector<float> yy( n2 );
  std::vector<float> vx( n2 );
  std::vector<float> vy( n2 );
  std::vector<float> vz( n2 );
  std::vector<float> ve( n2 );
  for(int j=0 ; j<n2; j++){
    it2->GetEntry( elist2->GetEntry(j) );
    xx[j]=x2;
    yy[j]=y2;
    vx[j]=px2;
    vy[j]=py2;
    vz[j]=pz2;
    ve[j]=sqrt(px2*px2 + py2*py2 + pz2*pz2 + mmass*mmass);
  }
  
  for(int i=0 ; i<n1 && i<MAX; i++){
    if (i%1000==0) cout << i << endl;
    it1->GetEntry( elist1->GetEntry(i) );
    float e1 = sqrt(px1*px1 + py1*py1 + pz1*pz1 + mmass*mmass);
    for(int j=0 ; j<n2 && j<MAX; j++){
      m = sqrt(pow(e1 + ve[j],2) - pow(px1 + vx[j],2) - pow(py1 + vy[j],2) - pow(pz1 + vz[j],2));
      x2 =xx[j];
      y2 =yy[j];
      px2=vx[j];
      py2=vy[j];
      pz2=vz[j];
      t->Fill();
    }
  }
  
  t->Write();
  f->Close();
  ifi1->Close();
  ifi2->Close();
}

int main(int argc, char *argv[]){
  if (argc>3){
    cout << "Setting min max events : " << atoi(argv[2]) << " " << atoi(argv[3]) << endl;
    step2_initial_to_final( argv[1], atoi(argv[2]), atoi(argv[3]) );
  } else if (argc>1){
    step2_initial_to_final( argv[1] );
  } else {
    step2_initial_to_final();
  }
  return 0;
}

// int main(){
//   step2_initial_to_final();
//   return 0;
// }


