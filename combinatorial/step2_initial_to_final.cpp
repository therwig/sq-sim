#include <iostream>
#include <Math/Vector4D.h>
#include "TRandom3.h"
#include "TString.h"
#include "TF1.h"
#include "TFile.h"
#include "TTree.h"
using std::cout;
using std::endl;

#include "constants.h"

//constexpr int NTRIALS_PER_EVENT=200*100;
constexpr bool DO_ELOSS=1;
constexpr bool DO_BEAMPXY=1;
constexpr bool DO_BFIELD=1;
constexpr bool DO_SCATTER=1;

constexpr bool DO_MUMINUS_SKIM=0;
constexpr float MUMINUS_SKIM_MINPZ=0.5;
constexpr float MUMINUS_SKIM_MINX=0;
constexpr float MUMINUS_SKIM_MAXX=50;

constexpr bool DO_MUPLUS_SKIM=1;
constexpr float MUPLUS_SKIM_MINPZ=0.5;
constexpr float MUPLUS_SKIM_MINX=0;
constexpr float MUPLUS_SKIM_MAXX=50;

constexpr bool DO_RANDOM_INPUTS=1;
// constexpr int DUMMY_NEVENT = 200 * 1e6; // noskim 5.5min
// constexpr int DUMMY_NEVENT = 2000 * 1e6; // mu- skim(x>0). 7min
// constexpr int DUMMY_NEVENT = 2000 * 1e6; // mu+ skim(0<x<50, pz>0.5). 10.m
constexpr int DUMMY_NEVENT = 500 * 1e6; // mu+ skim(0<x<50, pz>0.5). 10.m
// constexpr long DUMMY_NEVENT = 10000 * 1e6; // mu- skim. ~27.5 min
//constexpr long DUMMY_NEVENT = 1000 * 1e6; // mu- skim. ~27.5 min
constexpr int NTRIALS_PER_EVENT=1;

void step2_initial_to_final(int randseed=2022){
  // Inputs
  TFile* ifi = new TFile("initial_muons.root","read");
  TTree* it = (TTree*) ifi->Get("Events");
  float ipx, ipy, ipz;
  int ipdg;
  it->SetBranchAddress("px",&ipx);
  it->SetBranchAddress("py",&ipy);
  it->SetBranchAddress("pz",&ipz);
  it->SetBranchAddress("pdg",&ipdg);
  
  // Outputs
  TFile* f = new TFile(TString::Format("final_muons_%d.root",randseed),"recreate");
  TTree* t = new TTree("Events","");
  float x, y, px, py, pz, dx, dxBeam, dxBfield;
  int pdg;
  t->Branch("x"  ,&x  ,"x/F"  );
  t->Branch("y"  ,&y  ,"y/F"  );
  t->Branch("px" ,&px ,"px/F" );
  t->Branch("py" ,&py ,"py/F" );
  t->Branch("pz" ,&pz ,"pz/F" );
  t->Branch("pdg",&pdg,"pdg/I");
  t->Branch("dxScatter" ,&dx ,"dxScatter/F" );
  t->Branch("dxBeam" ,&dxBeam ,"dxBeam/F" );
  t->Branch("dxBfield" ,&dxBfield ,"dxBfield/F" );

  t->Branch("init_px" ,&ipx ,"init_px/F" );
  t->Branch("init_py" ,&ipy ,"init_py/F" );
  t->Branch("init_pz" ,&ipz ,"init_pz/F" );

  // Utilities
  TRandom* r = new TRandom3(randseed);
  ROOT::Math::PxPyPzMVector m;
  float z, e, eloss, rescale, beta, p, dist_x0, t0, dzStep;
  TF1* scatterFunc = new TF1("scatterFunc","1/sqrt(TMath::Pi())*exp(-x*x) + (fabs(x)>2)*1/(8*log(204*pow(26,1/3))*fabs(x*x*x))",-20,20);

  long nEntries = DO_RANDOM_INPUTS ? DUMMY_NEVENT : it->GetEntries();
  for(long itree=0; itree<nEntries; itree++){
    if(!DO_RANDOM_INPUTS){
      it->GetEntry(itree);
    } else {
      if(DO_MUMINUS_SKIM){
        ipdg=13;
      } else if (DO_MUPLUS_SKIM) {
        ipdg=-13;
      } else {
        ipdg = r->Uniform()<0.45 ? 13 : -13;
      }
      ipx = r->Gaus(0, beam_sigma_pxy);
      ipy = r->Gaus(0, beam_sigma_pxy);
      ipz=200;
      while(ipz>120) ipz = r->Landau(5.56787e+00,7.17116e-01); // fit pz
    }
    pdg=ipdg; // doesn't change
    if (DO_MUMINUS_SKIM && pdg!=13) continue;
    if (DO_MUPLUS_SKIM && pdg!=-13) continue;
    for(int itrial=0; itrial<NTRIALS_PER_EVENT; itrial++){
      x = r->Gaus(0, beam_sigma_xy);
      y = r->Gaus(0, beam_sigma_xy);
      z = r->Exp(fe_nucl_int);
      dzStep = dump_len-z;

      if(DO_BEAMPXY){
        px = ipx;
        py = ipy;
      } else {
        px = 0;
        py = 0;
      }
      pz = ipz; 
      e = sqrt(px*px + py*py + pz*pz + mmass*mmass);
      eloss = (1.-z/dump_len) * r->Landau(landau_mpv_ref, landau_wid_ref)*landau_rescale;
      
      if( e > eloss || !DO_ELOSS){        
        // assess half of energy loss
        if(DO_ELOSS){
          rescale = sqrt(1. - eloss/e);
          px = px * rescale;
          py = py * rescale; 
          pz = pz * rescale;
        }
        dxBeam = dzStep * px/pz;
        
        // half of B field bending
        if(DO_BFIELD){
          pz = sqrt( std::max(1*MeV*MeV, pz*pz - half_fmag_dp*half_fmag_dp - 2*half_fmag_dp*px) ); // do first; uses pre-bend px
          px += (pdg<0 ? half_fmag_dp : -half_fmag_dp);
        }
        dxBfield = dzStep * px/pz - dxBeam;
        
        if(DO_SCATTER){
          // calc the random scattering angle
          p = sqrt(px*px + py*py + pz*pz);
          beta = p*p + mmass*mmass; // gamma2
          beta = sqrt(1 - 1./beta);
          dist_x0 = dzStep / fe_rad_len;
          t0 = 13.6*MeV / (beta * p) * sqrt(dist_x0) * (1 + 0.038 * log(dist_x0  / (beta*beta)));
          // propagate and scatter
          dx = dzStep * t0/2 * scatterFunc->GetRandom(-20,20);
          x += dzStep * px/pz + dx;
          y += dzStep * py/pz + dzStep * t0/2 * scatterFunc->GetRandom(-20,20);
        } else {
          // propagate only
          x += dzStep * px/pz;
          y += dzStep * py/pz;
        }
        if (DO_MUPLUS_SKIM && (x<MUPLUS_SKIM_MINX || x>MUPLUS_SKIM_MAXX)) continue;
        if (DO_MUMINUS_SKIM && (x<MUMINUS_SKIM_MINX || x>MUMINUS_SKIM_MAXX)) continue;

        // finish bending and energy loss
        if(DO_BFIELD){
          pz = sqrt( std::max(1*MeV*MeV, pz*pz - half_fmag_dp*half_fmag_dp - 2*half_fmag_dp*px) ); // do first; uses pre-bend px
          px += (pdg<0 ? half_fmag_dp : -half_fmag_dp);
        }
        if(DO_ELOSS){
          px = px * rescale;
          py = py * rescale; 
          pz = pz * rescale;
        }
        if (DO_MUPLUS_SKIM && pz<MUPLUS_SKIM_MINPZ) continue;
        if (DO_MUMINUS_SKIM && pz<MUMINUS_SKIM_MINPZ) continue;
      } else { // all energy is lost in the dump
        pz=0;
        if (DO_MUPLUS_SKIM) continue;
        if (DO_MUMINUS_SKIM) continue;
      }
      
      t->Fill();
    }
  }
  t->Write();
  f->Close();
  ifi->Close();
}

int main(int argc, char *argv[]){
  if (argc>1){
    cout << "Setting random seed: " << atoi(argv[1]) << endl;
    step2_initial_to_final( atoi(argv[1]) );
  } else {
    step2_initial_to_final();
  }
  return 0;
}

