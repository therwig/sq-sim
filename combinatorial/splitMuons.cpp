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

void split(){
  // unfortunately the splitting function was overwritten so I don't have a copy :(
  // must be re-written if we want to use it again. or combine the existing files in data/splitMuons/
  TString path = "data/pseudo120";
  TFile* f = new TFile(path+"/large_final_muons.root","read");
  TTree* t = (TTree*) f->Get("Events");
  float x, y, px, py, pz; // tie all outputs to these as well
  int pdg;
  t->SetBranchAddress("x",&x);
  t->SetBranchAddress("y",&y);
  t->SetBranchAddress("px",&px);
  t->SetBranchAddress("py",&py);
  t->SetBranchAddress("pz",&pz);
  t->SetBranchAddress("pdg",&pdg);

  constexpr int NBIN = 40;
  float x1, y1, px1, py1, pz1; 
  TFile* fP[NBIN];
  TTree* tP[NBIN];
  TFile* fM[NBIN];
  TTree* tM[NBIN];
  
  for(int ibin=0; ibin<NBIN; ibin++){
    fP[ibin] = new TFile(TString::Format(path+"/large_final_muons_bin%dP.root",ibin),"recreate");
    tP[ibin] = new TTree("Events","");
    tP[ibin]->Branch("x", &x1 ,"x" );
    tP[ibin]->Branch("y", &y1 ,"y" );
    tP[ibin]->Branch("px",&px1,"px");
    tP[ibin]->Branch("py",&py1,"py");
    tP[ibin]->Branch("pz",&pz1,"pz");
    tP[ibin]->SetDirectory(fP[ibin]);

    fM[ibin] = new TFile(TString::Format(path+"/large_final_muons_bin%dM.root",ibin),"recreate");
    tM[ibin] = new TTree("Events","");
    tM[ibin]->Branch("x", &x1 ,"x" );
    tM[ibin]->Branch("y", &y1 ,"y" );
    tM[ibin]->Branch("px",&px1,"px");
    tM[ibin]->Branch("py",&py1,"py");
    tM[ibin]->Branch("pz",&pz1,"pz");
    tM[ibin]->SetDirectory(fM[ibin]);
  }

  int b;
  for(long i=0; i < t->GetEntries(); i++){
    if( i%1000*1000==0) cout << i/(1000*1000) << "M events" << endl;
    // if (i>1000) break;
    t->GetEntry(i);
    b = x-10;
    if(b<0 || b >= NBIN) continue;
    x1 =x ;
    y1 =y ;
    px1=px;
    py1=py;
    pz1=pz;
    if(pdg<0){
      tP[b]->Fill();
    } else {
      tM[b]->Fill();
    }
  }
  
  for(int ibin=0; ibin<NBIN; ibin++){
    fP[ibin]->cd();
    tP[ibin]->Write();
    fP[ibin]->Close();
    fM[ibin]->cd();
    tM[ibin]->Write();
    fM[ibin]->Close();
  }
  f->Close();
}

void make_pairs(unsigned int ibin, bool debug=false){
  
  // TFile* f1 = new TFile(TString::Format("data/splitMuons/large_final_muons_bin%dP.root",ibin),"read");
  TString path = "data/pseudo120";
  TFile* f1 = new TFile(path+TString::Format("/large_final_muons_bin%dP.root",ibin),"read");
  TTree* t1 = (TTree*) f1->Get("Events");
  float xx1, yy1, px1, py1, pz1;
  // float px1, py1, pz1;
  int pdg1;
  t1->SetBranchAddress("x",&xx1);
  t1->SetBranchAddress("y",&yy1);
  t1->SetBranchAddress("px",&px1);
  t1->SetBranchAddress("py",&py1);
  t1->SetBranchAddress("pz",&pz1);
  // t1->SetBranchAddress("pdg",&pdg1);

  // TFile* f2 = new TFile(TString::Format("data/splitMuons/large_final_muons_bin%dM.root",ibin),"read");
  TFile* f2 = new TFile(path+TString::Format("/large_final_muons_bin%dM.root",ibin),"read");
  // TFile* f2 = new TFile(TString::Format("data/splitMuons/rgp_large_final_muons_bin%dM.root",ibin),"read");
  TTree* t2 = (TTree*) f2->Get("Events");
  float xx2, yy2, px2, py2, pz2;
  // float px2, py2, pz2;
  int pdg2;
  t2->SetBranchAddress("x",&xx2);
  t2->SetBranchAddress("y",&yy2);
  t2->SetBranchAddress("px",&px2);
  t2->SetBranchAddress("py",&py2);
  t2->SetBranchAddress("pz",&pz2);
  // t2->SetBranchAddress("pdg",&pdg2);

  // TFile* f  = new TFile(TString::Format("data/splitMuons/pairs_bin%d.root",ibin),"recreate");
  TFile* f = new TFile(path+TString::Format("/pairs_bin%d.root",ibin),"recreate");
  // TFile* f  = new TFile(TString::Format("data/splitMuons/rgp_pairs_bin%d.root",ibin),"recreate");
  TTree* t = new TTree("Events","");
  float m;
  t->Branch("m"  ,&m  ,"m"  );
  t->Branch("bin" ,&ibin ,"bin/I" );
  // t->Branch("x1" ,&xx1 ,"x1" );
  // t->Branch("x2" ,&xx2 ,"x2" );
  // t->Branch("y1" ,&yy1 ,"y1" );
  // t->Branch("y2" ,&yy2 ,"y2" );
  
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
  std::vector<float> xp1( n1 );
  std::vector<float> yp1( n1 );
  for(int i=0 ; i<n1; i++){
    t1->GetEntry(i);
    x1[i] = px1;
    y1[i] = py1;
    z1[i] = pz1;
    e1[i] = sqrt(px1*px1 + py1*py1 + pz1*pz1 + mmass*mmass);
    xp1[i] = xx1;
    yp1[i] = yy1;
  }
  if(debug) cout << "Loading " << n2 << " events into memory " << endl;
  std::vector<float> e2( n2 );
  std::vector<float> x2( n2 );
  std::vector<float> y2( n2 );
  std::vector<float> z2( n2 );
  std::vector<float> xp2( n2 );
  std::vector<float> yp2( n2 );
  for(int i=0 ; i<n2; i++){
    t2->GetEntry(i);
    x2[i] = px2;
    y2[i] = py2;
    z2[i] = pz2;
    e2[i] = sqrt(px2*px2 + py2*py2 + pz2*pz2 + mmass*mmass);
    xp2[i] = xx2;
    yp2[i] = yy2;
  }
  if(debug) cout << "Finished loading all events into memory " << endl;

  float m2;
  const long MAX=1e7;
  float reduceBy1=100;
  float reduceBy2=1;
  float reduceBy=1;
  if (n1>MAX) cout << "warning: truncating a large number of inputs early (n1=" << n1 << ", reduced: " << n1/reduceBy << ")" << endl;
  if (n2>MAX) cout << "warning: truncating a large number of inputs early (n2=" << n2 << ", reduced: " << n2/reduceBy << ")" << endl;
  cout << "Reduced:  (n1 = " << n1/(reduceBy1*reduceBy) << " and n2 = " << n2/(reduceBy2*reduceBy) << " and pairs is " << n1*n2/(reduceBy1*reduceBy2*reduceBy*reduceBy)/1e6 << "M)" << endl;
  for(int i=0 ; i<n1/(reduceBy*reduceBy1) && i<MAX; i++){
    for(int j=0 ; j<n2/(reduceBy*reduceBy2) && j<MAX; j++){
      m2 = pow(e1[i] + e2[j],2) - pow(x1[i] + x2[j],2) - pow(y1[i] + y2[j],2) - pow(z1[i] + z2[j],2);
      if (m2 > 9) continue;
      // if (m2 > 4) continue;
      // if (m2 > 100) continue;
      m = sqrt(m2);
      m = float(int(m*256)) / 256.; // compress
      // xx1=xp1[i];
      // yy1=yp1[i];
      // xx2=xp2[i];
      // yy2=yp2[i];
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
  // make_pairs(0, true);
  for(int i=0; i<40;i++){
    cout << "Running bin " << i << endl;
    make_pairs(i, true);
  }
  return 0;
}
