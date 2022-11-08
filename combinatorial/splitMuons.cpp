#include <iostream>
#include <Math/Vector4D.h>
#include "TRandom3.h"
#include "TF1.h"
#include "TH1.h"
#include "TFile.h"
#include "TTree.h"
#include "TEventList.h"
#include <vector>
using std::cout;
using std::endl;

#include "constants.h"

// void split(){
// unfortunately the splitting function was overwritten so I don't have a copy :(
// must be re-written if we want to use it again. or combine the existing files in data/splitMuons/
  
//   TFile* f1 = new TFile(TString::Format("data/splitMuons/large_final_muons_bin%dP.root",ibin),"read");
//   TTree* t1 = (TTree*) f1->Get("Events");
//   float x1, y1, px1, py1, pz1;
//   int pdg1;
//   // t1->SetBranchAddress("x",&x1);
//   // t1->SetBranchAddress("y",&y1);
//   t1->SetBranchAddress("px",&px1);
//   t1->SetBranchAddress("py",&py1);
//   t1->SetBranchAddress("pz",&pz1);
//   // t1->SetBranchAddress("pdg",&pdg1);

//   TFile* f2 = new TFile(TString::Format("data/splitMuons/large_final_muons_bin%dM.root",ibin),"read");
//   TTree* t2 = (TTree*) f2->Get("Events");
//   float x2, y2, px2, py2, pz2;
//   int pdg2;
//   // t2->SetBranchAddress("x",&x2);
//   // t2->SetBranchAddress("y",&y2);
//   t2->SetBranchAddress("px",&px2);
//   t2->SetBranchAddress("py",&py2);
//   t2->SetBranchAddress("pz",&pz2);
//   // t2->SetBranchAddress("pdg",&pdg2);

//   TFile* f  = new TFile(TString::Format("data/splitMuons/pairs_bin%d.root",ibin),"recreate");
//   t = new TTree("Events","");
//   float m;
//   t->Branch("x"  ,&m  ,"x"  );
//   t->Branch("pz1" ,&pz1 ,"pz1" );
//   t->Branch("pz2" ,&pz2 ,"pz2" );

//   const int n1 = t1->GetEntries();
//   const int n2 = n2;
//   cout << "Expect to process " << (n1 * n2)/1e6 << "M pairs" << endl;
//   cout << "Loading " << n1 << " events into memory " << endl;
//   std::vector e1( n1 );
//   std::vector x1( n1 );
//   std::vector y1( n1 );
//   std::vector z1( n1 );
//   for(int i=0 ; i<n1; i++){
//     it->GetEntry(i);
//     x1[i] = px1;
//     y1[i] = py1;
//     z1[i] = pz1;
//     e1[i] = sqrt(px1*px1 + py1*py1 + pz1*pz1 + mmass*mmass);
//   }
//   cout << "Loading " << n2 << " events into memory " << endl;
//   std::vector e2( n2 );
//   std::vector x2( n2 );
//   std::vector y2( n2 );
//   std::vector z2( n2 );
//   for(int i=0 ; i<n2; i++){
//     it->GetEntry(i);
//     x2[i] = px2;
//     y2[i] = py2;
//     z2[i] = pz2;
//     e2[i] = sqrt(px2*px2 + py2*py2 + pz2*pz2 + mmass*mmass);
//   }
//   cout << "Finished loading all events into memory " << endl;

//   float m2;
//   const int MAX=1000;
//   for(int i=0 ; i<n1 && i<MAX; i++){
//     for(int j=0 ; j<n2 && j<MAX; j++){
//       m2 = pow(e1[i] + e2[j],2) - pow(x1[i] + x2[j],2) - pow(y1[i] + y2[j],2) - pow(z1[i] + z2[j],2);
//       if (m2 > 9) continue;
//       m=sqrt(m2);
//       t->Fill();
//     }
//   }
//   t->Write();
//   f->Close();
//   f1->Close();
//   f2->Close();

// }

void make_pairs(unsigned int ibin, bool debug=false){
  
  // TFile* f1 = new TFile(TString::Format("data/splitMuons/large_final_muons_bin%dP.root",ibin),"read");
  TFile* f1 = new TFile(TString::Format("data/splitMuons/rgp_large_final_muons_bin%dP.root",ibin),"read");
  TTree* t1 = (TTree*) f1->Get("Events");
  // float x1, y1, px1, py1, pz1;
  float px1, py1, pz1;
  int pdg1;
  // t1->SetBranchAddress("x",&x1);
  // t1->SetBranchAddress("y",&y1);
  t1->SetBranchAddress("px",&px1);
  t1->SetBranchAddress("py",&py1);
  t1->SetBranchAddress("pz",&pz1);
  // t1->SetBranchAddress("pdg",&pdg1);

  // TFile* f2 = new TFile(TString::Format("data/splitMuons/large_final_muons_bin%dM.root",ibin),"read");
  TFile* f2 = new TFile(TString::Format("data/splitMuons/rgp_large_final_muons_bin%dM.root",ibin),"read");
  TTree* t2 = (TTree*) f2->Get("Events");
  // float x2, y2, px2, py2, pz2;
  float px2, py2, pz2;
  int pdg2;
  // t2->SetBranchAddress("x",&x2);
  // t2->SetBranchAddress("y",&y2);
  t2->SetBranchAddress("px",&px2);
  t2->SetBranchAddress("py",&py2);
  t2->SetBranchAddress("pz",&pz2);
  // t2->SetBranchAddress("pdg",&pdg2);

  // TFile* f  = new TFile(TString::Format("data/splitMuons/pairs_bin%d.root",ibin),"recreate");
  TFile* f  = new TFile(TString::Format("data/splitMuons/rgp_pairs_bin%d.root",ibin),"recreate");
  TTree* t = new TTree("Events","");
  float m;
  t->Branch("m"  ,&m  ,"m"  );
  t->Branch("bin" ,&ibin ,"bin/I" );
  // t->Branch("pz1" ,&pz1 ,"pz1" );
  // t->Branch("pz2" ,&pz2 ,"pz2" );

  const long n1 = t1->GetEntries();
  const long n2 = t2->GetEntries();
  cout << "Expect to process " << (n1 * n2)/1e6 << "M pairs" << endl;
  if(debug) cout << "Loading " << n1 << " events into memory " << endl;
  std::vector<float> e1( n1 );
  std::vector<float> x1( n1 );
  std::vector<float> y1( n1 );
  std::vector<float> z1( n1 );
  for(int i=0 ; i<n1; i++){
    t1->GetEntry(i);
    x1[i] = px1;
    y1[i] = py1;
    z1[i] = pz1;
    e1[i] = sqrt(px1*px1 + py1*py1 + pz1*pz1 + mmass*mmass);
  }
  if(debug) cout << "Loading " << n2 << " events into memory " << endl;
  std::vector<float> e2( n2 );
  std::vector<float> x2( n2 );
  std::vector<float> y2( n2 );
  std::vector<float> z2( n2 );
  for(int i=0 ; i<n2; i++){
    t2->GetEntry(i);
    x2[i] = px2;
    y2[i] = py2;
    z2[i] = pz2;
    e2[i] = sqrt(px2*px2 + py2*py2 + pz2*pz2 + mmass*mmass);
  }
  if(debug) cout << "Finished loading all events into memory " << endl;

  float m2;
  const long MAX=1e7;
  if (n1>MAX) cout << "warning: truncating a large number of inputs early (n1=" << n1 << ")" << endl;
  if (n2>MAX) cout << "warning: truncating a large number of inputs early (n2=" << n2 << ")" << endl;
  for(int i=0 ; i<n1 && i<MAX; i++){
    for(int j=0 ; j<n2 && j<MAX; j++){
      m2 = pow(e1[i] + e2[j],2) - pow(x1[i] + x2[j],2) - pow(y1[i] + y2[j],2) - pow(z1[i] + z2[j],2);
      // if (m2 > 9) continue;
      if (m2 > 4) continue;
      m=sqrt(m2);
      t->Fill();
    }
  }
  t->Write();
  f->Close();
  f1->Close();
  f2->Close();
  
}

int main(int argc, char *argv[]){
  // split();
  // make_pairs(20);
  for(int i=6; i<10;i++){
    cout << "Running bin " << i << endl;
    make_pairs(i, false);
  }
  return 0;
}
