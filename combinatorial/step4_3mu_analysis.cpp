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
  TFile* ifi1 = new TFile("data/final_muons_noSkim.root","read");
  // TFile* ifi1 = new TFile("data/pseudo/final_muons_noSkim.root","read");
  // TFile* ifi1 = new TFile("data/pseudo120/final_muons_muplus_0x50_pz500_skim.root","read");
  // Access mu+ values
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
  // TFile* ifi2 = new TFile("data/final_muons_muminus_xge0_skim_20k.root","read");
  // TFile* ifi2 = new TFile("data/pseudo/final_muons_muminus_xge0_skim.root","read");
  // TFile* ifi2 = new TFile("data/pseudo120/final_muons_muminus_xge0_skim_1e11.root","read");
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
  ROOT::Math::PxPyPzMVector pos1;
  ROOT::Math::PxPyPzMVector pos2;
  ROOT::Math::PxPyPzMVector neg;

  
  // Preselect events to consider
  //it1->Draw(">>elist","pdg==13 && x>-5 && pz>0.5");
  int all_muplus = it1->GetEntries("pdg==-13");
  it1->Draw(">>elist","pdg==-13 && x>0 && x<50 && pz>0.5");
  TEventList *elist1 = (TEventList*) ((TEventList*) gDirectory->Get("elist"))->Clone("elist1");
  it1->SetEventList(elist1);

  // it2->Draw(">>elist","pdg==-13 && pz>0.5");
  int all_muminus = it2->GetEntries("pdg==13");
  it2->Draw(">>elist","pdg==13 && x>0 && x<50 && pz>0.5");
  TEventList *elist2 = (TEventList*) gDirectory->Get("elist");
  it2->SetEventList(elist2);

  // numerology
  //
  cout << "Trees contain " << it1->GetEntries() << " and " << it2->GetEntries() << " entries." << endl;
  cout << "  including " << all_muplus << " mu+ and " << all_muminus << " m-." << endl;
  cout << "Elists select " << elist1->GetN() << " and " << elist2->GetN() << " entries." << endl;
  cout << "Skim factors are " << t1_skim_factor << " and " << t2_skim_factor << " entries." << endl;
  // helper constants
  const float pos_frac =  0.55; // float(all_muplus) / it1->GetEntries();
  const float neg_frac =  0.45; // (1 - pos_frac);
  const float avgNpos = mu_per_spill * pos_frac;
  const float avgNneg = mu_per_spill * neg_frac;
  const float pos_mc_factor = t1_skim_factor * elist1->GetN() / all_muplus;
  const float neg_mc_factor = t2_skim_factor * elist2->GetN() / all_muminus;
  
  // estimate stats to find good background pairs
  TFile* fhist = new TFile("hist_mot_calc.root","recreate");
  TH1F* h_nMu = new TH1F("h_nMu","",60,-0.5,59.5);
  TH1F* h_nMuP = new TH1F("h_nMuP","",40,-0.5,39.5);
  TH1F* h_nMuM = new TH1F("h_nMuM","",40,-0.5,39.5);
  TH1F* h_nMuP_mc = new TH1F("h_nMuP_mc","",20,-0.5,19.5); // with mc factor
  TH1F* h_nMuP_mc_pairs = new TH1F("h_nMuP_mc_pairs","",50,-0.5,49.5); // truncate at 10Choose2
  int n_mu_plus_cap = 10; // keeps 95% of events

  // run a quick pair simulation
  TRandom* r = new TRandom3(2022);
  for(int i=0;i<100*1000;i++){
    // before any MC selection
    int nP = r->Poisson(avgNpos);
    int nM = r->Poisson(avgNneg);
    h_nMu->Fill(nP+nM);
    h_nMuP->Fill(nP);
    h_nMuM->Fill(nM);
    
    // after applying the MC selection factor (e.g. 'central' muons with pz>0.5 GeV)
    int nP_mc = r->Poisson(avgNneg * pos_mc_factor);
    h_nMuP_mc->Fill(nP_mc);
    h_nMuP_mc_pairs->Fill( nP_mc > n_mu_plus_cap ? 0 : TMath::Binomial(nP_mc,2) );
  }
  float mup_pairs_per_bucket = h_nMuP_mc_pairs->GetMean(); // / ntrials;
  // cout << mup_pairs_per_bucket << endl;
  fhist->Write();
  fhist->Close();

  cout << "The number of mu- per bucket in the fiducial region is " << avgNneg * neg_mc_factor << endl;
  cout << "The number of mu+ pairs per bucket in the fiducial region is " << mup_pairs_per_bucket << endl;
  cout << "The number of buckets that one MC event with 3 ficucial muons corresponds to is " << 1./(avgNneg * neg_mc_factor * mup_pairs_per_bucket) << endl;

  float fsim_signal_mu_10GeV = 0.057299957; // from step2 file
  float mean_sig_mu  = mu_per_spill * fsim_signal_mu_10GeV;

  cout << "///////////////////////////////////////////////////////////////////" << endl;
  cout << "The average number of 10 GeV muons (final pz) per bucket is " << mean_sig_mu << endl;
  cout << "Thus, to simulate background corresponding to..." << endl;
  cout << "  10^12 MoT requires "<< 1e12 * (avgNneg * neg_mc_factor * mup_pairs_per_bucket / mean_sig_mu) <<" MC events" << endl;
  cout << "  10^13 MoT requires "<< 1e13 * (avgNneg * neg_mc_factor * mup_pairs_per_bucket / mean_sig_mu) <<" MC events" << endl;
  cout << "  10^14 MoT requires "<< 1e14 * (avgNneg * neg_mc_factor * mup_pairs_per_bucket / mean_sig_mu) <<" MC events" << endl;
  cout << "///////////////////////////////////////////////////////////////////" << endl;

  //exit(0);

  
  // float muP_per_bucket = mu_per_spill * elist1->GetN() / float(it1->GetEntries());
  // float muM_per_bucket = mu_per_spill * elist2->GetN() / float(it2->GetEntries());
  // cout << "  Average mu- per bucket passing cuts: " << muP_per_bucket << endl;
  // cout << "  Average mu+ per bucket passing cuts: " << muM_per_bucket << endl;
  // cout << "  Sim factor: " << muP_per_bucket*muM_per_bucket*muM_per_bucket << endl;
  // cout << "  Triplets considered: " << (elist1->GetN()) * NTRIALS_PER_EVENT << endl;
  // cout << "  Effective same size: " << (elist1->GetN()) * float(NTRIALS_PER_EVENT) / (muP_per_bucket*muM_per_bucket*muM_per_bucket) << endl;

  // exit(0);
  
    // Outputs
  TFile* f = new TFile(TString::Format("final_events%s.root",suffix),"recreate");
  TTree* t = new TTree("Events","");
  float xP1, yP1, pxP1, pyP1, pzP1;
  float xP2, yP2, pxP2, pyP2, pzP2;
  float xN, yN, pxN, pyN, pzN;
  t->Branch("xP1"  ,&xP1  ,"xP1/F"  );
  t->Branch("yP1"  ,&yP1  ,"yP1/F"  );
  t->Branch("pxP1" ,&pxP1 ,"pxP1/F" );
  t->Branch("pyP1" ,&pyP1 ,"pyP1/F" );
  t->Branch("pzP1" ,&pzP1 ,"pzP1/F" );
  t->Branch("xP2"  ,&xP2  ,"xP2/F"  );
  t->Branch("yP2"  ,&yP2  ,"yP2/F"  );
  t->Branch("pxP2" ,&pxP2 ,"pxP2/F" );
  t->Branch("pyP2" ,&pyP2 ,"pyP2/F" );
  t->Branch("pzP2" ,&pzP2 ,"pzP2/F" );
  t->Branch("xN"  ,&xN  ,"xN/F"  );
  t->Branch("yN"  ,&yN  ,"yN/F"  );
  t->Branch("pxN" ,&pxN ,"pxN/F" );
  t->Branch("pyN" ,&pyN ,"pyN/F" );
  t->Branch("pzN" ,&pzN ,"pzN/F" );

  float xdiff, vx, m1n, m2n;
  t->Branch("xdiff"  ,&xdiff  ,"xdiff/F"  );
  t->Branch("vx"  ,&vx  ,"vx/F");
  t->Branch("m1n"  ,&m1n  ,"m1n/F");
  t->Branch("m2n"  ,&m2n  ,"m2n/F");

  int i1=0, interval=0; // these run over the lists
  // int i1 = offset1 % ;
  // int i2 = 0;
  // int interval=0; // these run over the lists

  if(maxEvt<0) maxEvt = elist1->GetN();
  std::cout << "Min and max: " << minEvt << " " << maxEvt << endl;
  
  
  // Loop over mu-
  for(int i2=minEvt ; i2<maxEvt; i2++){
    if ( ((i2-minEvt) % (100*1000)) == 0 ) cout << i2-minEvt << endl;
    it2->GetEntry( elist2->GetEntry(i2) );
    xN   = x2;
    yN   = y2;
    pxN  = px2;
    pyN  = py2;
    pzN  = pz2;

    // Loop over mu+
    for(int itrial=0; itrial<NTRIALS_PER_EVENT; itrial++){
      // first mu+
      it1->GetEntry( elist1->GetEntry(i1) );
      xP1   = x1;
      yP1   = y1;
      pxP1  = px1;
      pyP1  = py1;
      pzP1  = pz1;
      i1++;
      // i1 += 1+interval;
      if (i1 >= elist1->GetN()){
        i1 = (i1 % elist1->GetN());
        interval++;
      }
      it1->GetEntry( elist1->GetEntry(i1) );
      if (interval>1000) interval=0;

      // second mu+
      xP2   = x1;
      yP2   = y1;
      pxP2  = px1;
      pyP2  = py1;
      pzP2  = pz1;
      
      i1 += 1+interval; // this is a bit wasteful but :/
      if (i1 >= elist1->GetN()){
        i1 = (i1 % elist1->GetN());
        interval++;
      }
      if (interval>1000) interval=0;

      xdiff = std::max(std::max(xP1, xP2), xN) - std::min(std::min(xP1, xP2), xN);
      vx = (xP1+xP2+xN)/3.;

      if (xdiff>10) continue;
      // if (xdiff>3) continue; // extreme skim
      
      if (xdiff<20){
        if (pzP1>pzP2){
          pos1.SetCoordinates(pxP1,pyP1,pzP1,mmass);
          pos2.SetCoordinates(pxP2,pyP2,pzP2,mmass);
        } else {
          pos2.SetCoordinates(pxP1,pyP1,pzP1,mmass);
          pos1.SetCoordinates(pxP2,pyP2,pzP2,mmass);
        }
        neg.SetCoordinates(pxN,pyN,pzN,mmass);
        m1n = (pos1+neg).M();
        m2n = (pos2+neg).M();
      } else {
        m1n = 10;
        m2n = 10;
      }
      // if (std::min(m1n,m2n) > 2) continue; // extreme skim
      t->Fill();
    }
    // if (pdg1==13 && x1>-1 && pz1>0.5) ct++;
    // ct++;
    // if( i1<100){
    //   cout << pdg1 << " " << x1 << std::endl;
    // }
  }

  // for(int i2=0; i2<elist1->GetN(); i2++){
  //   it2->GetEntry( elist1->GetEntry(i2) );
  //   ct2++;
  // }
  
  // cout << ct << " " << ct2 << endl;

  cout << interval << endl;
  
  t->Write();
  f->Close();
  ifi1->Close();
  ifi2->Close();
  
  //   pdg=ipdg; // doesn't change
  //   for(int itrial=0; itrial<NTRIALS_PER_EVENT; itrial++){
  //     x = r->Gaus(0, beam_sigma_xy);
  //     y = r->Gaus(0, beam_sigma_xy);
  //     z = r->Exp(fe_nucl_int);

  //     px = ipx;
  //     py = ipy; 
  //     pz = ipz; 
  //     e = sqrt(px*px + py*py + pz*pz + mmass*mmass);
  //     eloss = (1.-z/dump_len) * r->Landau(landau_mpv_ref, landau_wid_ref)*landau_rescale;
  //     if( e <= eloss ){
  //       pz=0;
  //     } else {
  //       // assess half of energy loss
  //       rescale = sqrt(1. - eloss/e);
  //       px = px * rescale;
  //       py = py * rescale; 
  //       pz = pz * rescale;
  //       // half of B field bending
  //       pz = sqrt( std::max(1*MeV*MeV, pz*pz - half_fmag_dp*half_fmag_dp - 2*half_fmag_dp*px) ); // do first; uses pre-bend px
  //       px += (pdg<0 ? half_fmag_dp : -half_fmag_dp);

  //       // calc the random scattering angle
  //       dzStep = dump_len-z;
  //       p = sqrt(px*px + py*py + pz*pz);
  //       beta = p*p + mmass*mmass; // gamma2
  //       beta = sqrt(1 - 1./beta);
  //       dist_x0 = dzStep / fe_rad_len;
  //       t0 = 13.6*MeV / (beta * p) * sqrt(dist_x0) * (1 + 0.038 * log(dist_x0  / (beta*beta)));
  //       // propagate and scatter
  //       dx = dzStep * t0/2 * scatterFunc->GetRandom(-20,20);
  //       x += dzStep * px/pz + dx;
  //       y += dzStep * py/pz + dzStep * t0/2 * scatterFunc->GetRandom(-20,20);

  //       // finish bending and energy loss
  //       pz = sqrt( std::max(1*MeV*MeV, pz*pz - half_fmag_dp*half_fmag_dp - 2*half_fmag_dp*px) ); // do first; uses pre-bend px
  //       px += (pdg<0 ? half_fmag_dp : -half_fmag_dp);
  //       px = px * rescale;
  //       py = py * rescale; 
  //       pz = pz * rescale;
  //     }
      
  //     t->Fill();
  //   }
  // }
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

B
