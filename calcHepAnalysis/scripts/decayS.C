void decayS(){}
void decayS(TString fname, float mS, int nDecays=1){
  TFile* f = new TFile(fname,"r");
  TTree* it = (TTree*) f->Get("Events");

  float rIz, nIz, rx, ry, rz, sx, sy, sz, nx, ny, nz;
  it->SetBranchAddress("mInitialz",&rIz);
  it->SetBranchAddress("nInitialz",&nIz);
  it->SetBranchAddress("rx",&rx); // recoil muon
  it->SetBranchAddress("ry",&ry);
  it->SetBranchAddress("rz",&rz);
  it->SetBranchAddress("sx",&sx); // scalar
  it->SetBranchAddress("sy",&sy);
  it->SetBranchAddress("sz",&sz);
  it->SetBranchAddress("nz",&nz); // nucleon
  it->SetBranchAddress("nx",&nx);
  it->SetBranchAddress("ny",&ny);

  
  TFile* fo = new TFile(fname.ReplaceAll(".root","")+"_decayed.root","recreate");
  TTree* t = new TTree("Events","");
  float s1x, s1y, s1z, s2x, s2y, s2z; // scalar decay products
  // new
  t->Branch("s1x"  ,&s1x  ,"s1x/F"  ); // mu- (13) from the scalar
  t->Branch("s1y"  ,&s1y  ,"s1y/F"  );
  t->Branch("s1z"  ,&s1z  ,"s1z/F"  );
  t->Branch("s2x"  ,&s2x  ,"s2x/F"  ); // mu+ (-13) from the scalar
  t->Branch("s2y"  ,&s2y  ,"s2y/F"  );
  t->Branch("s2z"  ,&s2z  ,"s2z/F"  );
  // old
  t->Branch("rIz"  ,&rIz, "rIz/F");
  t->Branch("nIz"  ,&nIz, "nIz/F");
  t->Branch("rx"   ,&rx,  "rx/F");
  t->Branch("ry"   ,&ry,  "ry/F");
  t->Branch("rz"   ,&rz,  "rz/F");
  t->Branch("sx"   ,&sx,  "sx/F");
  t->Branch("sy"   ,&sy,  "sy/F");
  t->Branch("sz"   ,&sz,  "sz/F");
  t->Branch("nz"   ,&nz,  "nz/F");
  t->Branch("nx"   ,&nx,  "nx/F");
  t->Branch("ny"   ,&ny,  "ny/F");

  /* ROOT::Math::PxPyPzMVector m1, m2, s; */
  TLorentzVector s1, s2, s;
  TRandom* r = new TRandom3(2022);
  float phi, cosTheta, sinTheta;
  float mMu=0.105;
  float pCoM = sqrt(pow(mS,2)-2*pow(mMu,2))/2.;
  
  for(long itree=0; itree<it->GetEntries(); itree++){
    it->GetEntry(itree);
    for (int iDecay=0; iDecay<nDecays; iDecay++){
      // random CoM coords
      phi = 2*TMath::Pi() * r->Rndm();
      cosTheta = 2 * r->Rndm() - 1;
      sinTheta = sqrt(1-cosTheta*cosTheta);
      /* m1.SetCoordinates(pCoM*sin(phi)*sinTheta,  pCoM*cos(phi)*sinTheta,  pCoM*cosTheta,  mMu); */
      /* m2.SetCoordinates(-pCoM*sin(phi)*sinTheta, -pCoM*cos(phi)*sinTheta, -pCoM*cosTheta, mMu); */
      /* s.SetCoordinates(sx, sy, sz, mS); */
      s1.SetXYZM(pCoM*sin(phi)*sinTheta,  pCoM*cos(phi)*sinTheta,  pCoM*cosTheta,  mMu);
      s2.SetXYZM(-pCoM*sin(phi)*sinTheta, -pCoM*cos(phi)*sinTheta, -pCoM*cosTheta, mMu);
      s.SetXYZM(sx, sy, sz, mS);
      s1.Boost( s.BoostVector() );
      s2.Boost( s.BoostVector() );
      s1x=s1.Px();
      s1y=s1.Py();
      s1z=s1.Pz();
      s2x=s2.Px();
      s2y=s2.Py();
      s2z=s2.Pz();
      t->Fill();
    }
  }
  t->Write();
  fo->Close();
  f->Close();
  gSystem->Exit(0);
}

