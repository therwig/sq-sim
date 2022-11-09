TRandom3* r = new TRandom3(2022);
float s(float x){return r->Gaus(1,.05/3) * x;}

void makeSigFriend(){}
void makeSigFriend(TString fname){
  TFile* f = new TFile(fname,"r");
  TTree* it = (TTree*) f->Get("Events");

  // take the generated particle momenta and translate to "observe-ables"
  //   e.g. momentum-ordered muons without truth labeling
  
  float rx, ry, rz, s1x, s1y, s1z, s2x, s2y, s2z; // scalar decay products
  it->SetBranchAddress("rx",&rx); // recoil mu- (13)
  it->SetBranchAddress("ry",&ry);
  it->SetBranchAddress("rz",&rz);
  it->SetBranchAddress("s1x",&s1x); // mu- (13) from the scalar
  it->SetBranchAddress("s1y",&s1y);
  it->SetBranchAddress("s1z",&s1z);
  it->SetBranchAddress("s2x",&s2x); // mu+ (-13) from the scalar
  it->SetBranchAddress("s2y",&s2y);
  it->SetBranchAddress("s2z",&s2z);
  
  TFile* fo = new TFile(fname.ReplaceAll(".root","")+"_Friend.root","recreate");
  TTree* t = new TTree("Friends","");
  float Mx, My, Mz, m1x, m1y, m1z, m2x, m2y, m2z;
  float mass1, mass2;
  float dot1, dot2; //, p1, p2, P;
  float dr1, dr2, drr1, drr2; //, p1, p2, P;
  float pair1x, pair1y, pair1z, pair1p, pair2x, pair2y, pair2z, pair2p;
  float pair1z1fracP, pair2z1fracP, pair1z1fracPz, pair2z1fracPz;
  t->Branch("Mx"  ,&Mx  ,"Mx/F"  ); // mu+ (-13) 
  t->Branch("My"  ,&My  ,"My/F"  );
  t->Branch("Mz"  ,&Mz  ,"Mz/F"  );
  t->Branch("m1x"  ,&m1x  ,"m1x/F"  ); // mu- (13) with leading pz
  t->Branch("m1y"  ,&m1y  ,"m1y/F"  );
  t->Branch("m1z"  ,&m1z  ,"m1z/F"  );
  t->Branch("m2x"  ,&m2x  ,"m2x/F"  ); // mu- (13) with sub-leading pz
  t->Branch("m2y"  ,&m2y  ,"m2y/F"  );
  t->Branch("m2z"  ,&m2z  ,"m2z/F"  );
  t->Branch("mass1"  ,&mass1  ,"mass1/F"  );
  t->Branch("mass2"  ,&mass2  ,"mass2/F"  );
  t->Branch("dot1"  ,&dot1  ,"dot1/F");
  t->Branch("dot2"  ,&dot2  ,"dot2/F");
  t->Branch("dr1"  ,&dr1  ,"dr1/F");
  t->Branch("dr2"  ,&dr2  ,"dr2/F");
  t->Branch("drr1"  ,&drr1  ,"drr1/F");
  t->Branch("drr2"  ,&drr2  ,"drr2/F");
  t->Branch("pair1x"  ,&pair1x  ,"pair1x/F");
  t->Branch("pair1y"  ,&pair1y  ,"pair1y/F");
  t->Branch("pair1z"  ,&pair1z  ,"pair1z/F");
  t->Branch("pair1p"  ,&pair1p  ,"pair1p/F");
  t->Branch("pair2x"  ,&pair2x  ,"pair2x/F");
  t->Branch("pair2y"  ,&pair2y  ,"pair2y/F");
  t->Branch("pair2z"  ,&pair2z  ,"pair2z/F");
  t->Branch("pair2p"  ,&pair2p  ,"pair2p/F");
  t->Branch("pair1z1fracP"  ,&pair1z1fracP  ,"pair1z1fracP/F");
  t->Branch("pair2z1fracP"  ,&pair2z1fracP  ,"pair2z1fracP/F");
  t->Branch("pair1z1fracPz"  ,&pair1z1fracPz  ,"pair1z1fracPz/F");
  t->Branch("pair2z1fracPz"  ,&pair2z1fracPz  ,"pair2z1fracPz/F");

  float s_Mx, s_My, s_Mz;
  float s_m1x, s_m1y, s_m1z, s_m2x, s_m2y, s_m2z;
  float s_mass1, s_mass2;
  float s_dot1, s_dot2;
  float s_dr1, s_dr2, s_drr1, s_drr2;
  float s_pair1x, s_pair1y, s_pair1z, s_pair1p, s_pair2x, s_pair2y, s_pair2z, s_pair2p;
  float s_pair1z1fracP, s_pair2z1fracP, s_pair1z1fracPz, s_pair2z1fracPz;
  t->Branch("s_m1x"  ,&s_m1x  ,"s_m1x/F"  );
  t->Branch("s_m1y"  ,&s_m1y  ,"s_m1y/F"  );
  t->Branch("s_m1z"  ,&s_m1z  ,"s_m1z/F"  );
  t->Branch("s_m2x"  ,&s_m2x  ,"s_m2x/F"  );
  t->Branch("s_m2y"  ,&s_m2y  ,"s_m2y/F"  );
  t->Branch("s_m2z"  ,&s_m2z  ,"s_m2z/F"  );
  t->Branch("s_Mx"  ,&s_Mx  ,"s_Mx/F"  );
  t->Branch("s_My"  ,&s_My  ,"s_My/F"  );
  t->Branch("s_Mz"  ,&s_Mz  ,"s_Mz/F"  );
  t->Branch("s_mass1"  ,&s_mass1  ,"s_mass1/F");
  t->Branch("s_mass2"  ,&s_mass2  ,"s_mass2/F");
  t->Branch("s_dot1"  ,&s_dot1  ,"s_dot1/F");
  t->Branch("s_dot2"  ,&s_dot2  ,"s_dot2/F");
  t->Branch("s_dr1"  ,&s_dr1  ,"s_dr1/F");
  t->Branch("s_dr2"  ,&s_dr2  ,"s_dr2/F");
  t->Branch("s_drr1"  ,&s_drr1  ,"s_drr1/F");
  t->Branch("s_drr2"  ,&s_drr2  ,"s_drr2/F");
  t->Branch("s_pair1x"  ,&s_pair1x  ,"s_pair1x/F");
  t->Branch("s_pair1y"  ,&s_pair1y  ,"s_pair1y/F");
  t->Branch("s_pair1z"  ,&s_pair1z  ,"s_pair1z/F");
  t->Branch("s_pair1p"  ,&s_pair1p  ,"s_pair1p/F");
  t->Branch("s_pair2x"  ,&s_pair2x  ,"s_pair2x/F");
  t->Branch("s_pair2y"  ,&s_pair2y  ,"s_pair2y/F");
  t->Branch("s_pair2z"  ,&s_pair2z  ,"s_pair2z/F");
  t->Branch("s_pair2p"  ,&s_pair2p  ,"s_pair2p/F");
  t->Branch("s_pair1z1fracP"  ,&s_pair1z1fracP  ,"s_pair1z1fracP/F");
  t->Branch("s_pair2z1fracP"  ,&s_pair2z1fracP  ,"s_pair2z1fracP/F");
  t->Branch("s_pair1z1fracPz"  ,&s_pair1z1fracPz  ,"s_pair1z1fracPz/F");
  t->Branch("s_pair2z1fracPz"  ,&s_pair2z1fracPz  ,"s_pair2z1fracPz/F");

  TLorentzVector m1V, m2V, MV;
  float mMu=0.105;
  for(long itree=0; itree<it->GetEntries(); itree++){
    it->GetEntry(itree);
    if(s1z>rz){
      m1x=s1x;
      m1y=s1y;
      m1z=s1z;
      m2x=rx;
      m2y=ry;
      m2z=rz;
    } else {
      m2x=s1x;
      m2y=s1y;
      m2z=s1z;
      m1x=rx;
      m1y=ry;
      m1z=rz;
    }
    Mx=s2x;
    My=s2y;
    Mz=s2z;

    m1V.SetXYZM(m1x, m1y, m1z, mMu);
    m2V.SetXYZM(m2x, m2y, m2z, mMu);
    MV.SetXYZM(Mx, My, Mz, mMu);
    
    mass1 = (m1V+MV).M();
    pair1x = (m1V+MV).Px();
    pair1y = (m1V+MV).Py();
    pair1z = (m1V+MV).Pz();
    pair1p = (m1V+MV).P();
    pair1z1fracP = max(m1V.P(),MV.P())/(m1V+MV).P();
    pair1z1fracPz = max(m1V.Pz(),MV.Pz())/(m1V+MV).P();
    mass2 = (m2V+MV).M();
    pair2x = (m2V+MV).Px();
    pair2y = (m2V+MV).Py();
    pair2z = (m2V+MV).Pz();
    pair2p = (m2V+MV).P();
    pair2z1fracP = max(m2V.P(),MV.P())/(m2V+MV).P();
    pair2z1fracPz = max(m2V.Pz(),MV.Pz())/(m2V+MV).P();
    dot1 = m1V.Dot(MV);
    dot2 = m2V.Dot(MV);
    dr1 = m1V.DrEtaPhi(MV);
    dr2 = m2V.DrEtaPhi(MV);
    drr1 = m1V.Vect().Angle(MV.Vect());
    drr2 = m2V.Vect().Angle(MV.Vect());

    s_m1x=s(m1x);
    s_m1y=s(m1y);
    s_m1z=s(m1z);
    s_m2x=s(m2x);
    s_m2y=s(m2y);
    s_m2z=s(m2z);
    s_Mx=s(Mx);
    s_My=s(My);
    s_Mz=s(Mz);
    m1V.SetXYZM(s_m1x, s_m1y, s_m1z, mMu);
    m2V.SetXYZM(s_m2x, s_m2y, s_m2z, mMu);
    MV.SetXYZM (s_Mx,  s_My,  s_Mz, mMu);
    
    s_mass1 = (m1V+MV).M();
    s_pair1x = (m1V+MV).Px();
    s_pair1y = (m1V+MV).Py();
    s_pair1z = (m1V+MV).Pz();
    s_pair1p = (m1V+MV).P();
    s_pair1z1fracP = max(m1V.P(),MV.P())/(m1V+MV).P();
    s_pair1z1fracPz = max(m1V.Pz(),MV.Pz())/(m1V+MV).P();
    s_mass2 = (m2V+MV).M();
    s_pair2x = (m2V+MV).Px();
    s_pair2y = (m2V+MV).Py();
    s_pair2z = (m2V+MV).Pz();
    s_pair2p = (m2V+MV).P();
    s_pair2z1fracP = max(m2V.P(),MV.P())/(m2V+MV).P();
    s_pair2z1fracPz = max(m2V.Pz(),MV.Pz())/(m2V+MV).P();
    s_dot1 = m1V.Dot(MV);
    s_dot2 = m2V.Dot(MV);
    s_dr1 = m1V.DrEtaPhi(MV);
    s_dr2 = m2V.DrEtaPhi(MV);
    s_drr1 = m1V.Vect().Angle(MV.Vect());
    s_drr2 = m2V.Vect().Angle(MV.Vect());
    
    /* m1V.SetXYZM(m1x, m1y, m1z, mMu); */
    /* m2V.SetXYZM(m2x, m2y, m2z, mMu); */
    /* MV.SetXYZM(Mx, My, Mz, mMu); */
    /* mass1 = (m1V+MV).M(); */
    /* pair1x = (m1V+MV).Px(); */
    /* pair1y = (m1V+MV).Py(); */
    /* pair1z = (m1V+MV).Pz(); */
    /* pair1z1fracP = max(m1V.P(),MV.P())/(m1V+MV).P(); */
    /* pair1z1fracPz = max(m1z,Mz)/(m1V+MV).Pz(); */
    /* mass2 = (m2V+MV).M(); */
    /* pair2x = (m2V+MV).Px(); */
    /* pair2y = (m2V+MV).Py(); */
    /* pair2z = (m2V+MV).Pz(); */
    /* pair2z1fracP = max(m2V.P(),MV.P())/(m2V+MV).P(); */
    /* pair2z1fracPz = max(m2z,Mz)/(m2V+MV).Pz(); */
    /* dot1 = m1V.Dot(MV); */
    /* dot2 = m2V.Dot(MV); */
    /* dr1 = m1V.DrEtaPhi(MV); */
    /* dr2 = m2V.DrEtaPhi(MV); */
    /* drr1 = m1V.Vect().Angle(MV.Vect()); */
    /* drr2 = m2V.Vect().Angle(MV.Vect()); */
    
    t->Fill();
  }
  t->Write();
  fo->Close();
  f->Close();
  gSystem->Exit(0);
}
