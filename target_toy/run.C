TRandom* r = new TRandom3(2022);
vector<int> colz {kBlack, kRed, kBlue, 8,6,7,40,41,42,43,44};

void genMC(){
  TFile* f = new TFile("out.root","recreate");
  TTree* t = new TTree("Events","");
  float m, ms, z;
  t->Branch("z"  ,&z  ,"z/F" );
  t->Branch("m"  ,&m  ,"m/F" );
  t->Branch("ms"  ,&ms  ,"ms/F" );
  
  constexpr int NTRIALS=10*1000*1000;
  for(int itrial=0; itrial<NTRIALS; itrial++){
    z = 300 * r->Rndm(); // in x0
    float relUnc = 28e-3 * sqrt(z); // from pvs studies
    m = r->Gaus(1, relUnc);
    ms = r->Gaus(m, 0.05);
    t->Fill();
  }
  t->Write();
  f->Close();
}
std::pair<float, float> FindMinSRB(TH1* h, float bscale=1.){
  int iCent = h->GetNbinsX()/2+1;
  float best=0, v;
  int bestW=0;
  float nom;
  for(int iWid=0; iWid < h->GetNbinsX()/2; iWid++){
    v = h->Integral(iCent-iWid,iCent+iWid);
    v /= sqrt( (1+2*iWid)*bscale );
    if (v>best){
      best=v;
      bestW=iWid;
    }
    if (iWid==5){
      cout << h->Integral(iCent-iWid,iCent+iWid) << " "
           << sqrt(1+2*iWid) << " "
           << h->Integral(iCent-iWid,iCent+iWid) / sqrt(1+2*iWid) << " "
           << v << " "
           << endl;
      nom = v;
    }
  }

  cout << "  The best width is found to be " << bestW << "% " << endl;
  printf("  This (srb=%.3f) is %.3f times better than the +/- 50 MeV result (srb=%.3f)\n",best, best/nom, nom);
  /* cout << "  This is " << best/nom << " times better than +/- 5 MeV" << endl; */
  return std::make_pair(best,bestW);
}
std::vector<float> GetAllSRB(TH1* h, float bscale=1.){
  int iCent = h->GetNbinsX()/2+1;
  float best=0, v;
  int bestW=0;
  float nom;
  vector<float> srbs;
  for(int iWid=0; iWid < h->GetNbinsX()/2; iWid++){
    v = h->Integral(iCent-iWid,iCent+iWid);
    v /= sqrt( (1+2*iWid)*bscale );
    srbs.push_back(v);
  }
  return srbs;
}
void fitSimple(){
  TFile* f = new TFile("out.root","read");
  TTree* t = (TTree*) f->Get("Events");
  TH1F* h = new TH1F("h","",401,-1,3);
  /* std::vector<float> x0s{1,5,10,20,50,100,200,300}; */
  /* std::vector<float> x0s{1,6,60,120,350}; */
  std::vector<float> x0s{1,5,10,20,50,100};
  std::vector<float> sigs;
  std::vector<float> wids;
  std::vector<TH1*> hs;
  TCanvas c("c","");

  float N = t->GetEntries();
  std::vector<float> srbs;
  std::vector< std::vector<float> > srbVecs;
  float hmax=0;
  for(auto x0 : x0s){
    cout << "Considering " << x0 << " x0:" << endl;
    t->Draw("ms>>h",Form("z<%f",x0));
    h->Scale(568*1.753*3./1.428/N/1.519);
    auto p = FindMinSRB(h, x0);
    srbs.push_back( p.first );
    wids.push_back( p.second );
    srbVecs.push_back( GetAllSRB(h, x0) );
    hs.push_back((TH1*) h->Clone(Form("h_%f",x0)));
    if( h->GetMaximum() > hmax) hmax = h->GetMaximum();
  }
  TGraph* g = new TGraph( x0s.size(), &x0s[0], &srbs[0] );
  g->Draw("AC*");
  c.SaveAs("plots/srbs.pdf");
  g = new TGraph( x0s.size(), &x0s[0], &wids[0] );
  g->Draw("AC*");
  c.SaveAs("plots/wids.pdf");
  
  
  vector<TGraph*> gs;
  vector<float> binsWids;
  for(int iWid=0; iWid < h->GetNbinsX()/2; iWid++)
    binsWids.push_back( h->GetBinWidth(1)*(1+2*iWid) * 100 / 2.);
  TMultiGraph* mg = new TMultiGraph();
  int NN=50;
  for (auto srbVec : srbVecs){
    srbVec.resize(NN);
    binsWids.resize(NN);
    gs.push_back( new TGraph( NN, &binsWids[0], &srbVec[0] ) );
    /* gs.back().SetLineColor(colz[gs.size()-1]); */
    mg->Add(gs.back());
  }
  mg->Draw("AC PLC");
  mg->SetTitle(";m_{#mu+#mu-} window [%];S/#sqrt{B}");

  g = new TGraph( wids.size(), &wids[0], &srbs[0] );
  g->SetMarkerStyle(5);
  g->SetMarkerColor(kBlack);
  g->Draw("P same");
  
  c.SaveAs("plots/scanSrB.pdf");

  auto leg = new TLegend(0.7,0.4,0.88,0.85);
  leg->SetTextFont(42);
  leg->SetNColumns(1);
  leg->SetHeader("Target thickness");
  
  gStyle->SetOptStat(0);
  for (int i=0; i<hs.size();i++){
    hs[i]->Scale(1./hmax);
    if (i==0){
      hs[i]->Draw("hist plc");
    } else {
      hs[i]->Draw("hist plc same");
    }
    float rms = 100 * hs[i]->GetRMS();
    if (rms < 10) leg->AddEntry(hs[i], Form("%d X0, %.1f%% RMS",int(x0s[i]),rms), "l");
    else leg->AddEntry(hs[i], Form("%d X0, %.0f%% RMS",int(x0s[i]),rms), "l");
  }
  hs[0]->GetXaxis()->SetRangeUser(0,2);
  hs[0]->GetYaxis()->SetRangeUser(0,1.1);
  hs[0]->SetTitle(";m_{#mu+#mu-}/m_{S, true} ;events [arbitrary units]");
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetBorderSize(0);
  leg->Draw();
          
  c.SaveAs("plots/scanSrB_hists.pdf");
    
  // TMP
  f->Close();
  return;

}
void fit(){
  TFile* f = new TFile("out.root","read");
  TTree* t = (TTree*) f->Get("Events");
  TH1F* h = new TH1F("h","",401,-1,3);
  /* std::vector<float> x0s{1,5,10,20,50,100,200,300}; */
  std::vector<float> x0s{1,6,60,120,350};
  std::vector<float> sigs;
  std::vector<float> wids;
  TCanvas c("c","");
  
  float s, wid;
  float N = t->GetEntries();
  for(auto x0 : x0s){
    t->Draw("ms>>h",Form("z<%f",x0));
    sigs.push_back( h->Integral(0,h->GetNbinsX()+2) / N );
    wids.push_back( h->GetRMS() );
    h->Draw();
    TF1 *fb1 = new TF1("fb1","gaus(0)",-1,3); fb1->SetLineColor(kRed);
    TF1 *fb2 = new TF1("fb2","gaus(0)+gaus(3)",-1,3); fb2->SetLineColor(kBlue);
    h->Fit("fb1","q");
    fb2->SetParameter(0, fb1->GetParameter(0));
    fb2->SetParameter(1, fb1->GetParameter(1));
    fb2->SetParameter(2, fb1->GetParameter(2));
    fb2->SetParameter(3, 0.1* fb1->GetParameter(0));
    fb2->SetParameter(4, fb1->GetParameter(1));
    fb2->SetParameter(5, 2*fb1->GetParameter(2));
    h->Fit("fb2","q");
    fb1->Draw("same");
    c.SaveAs(Form("plots/fit_%d.pdf",int(x0)));
  }
  /* TCanvas c("c",""); */

  TGraph* g = new TGraph( x0s.size(), &x0s[0], &sigs[0] );
  g->Draw("AC*");
  c.SaveAs("plots/sigs.pdf");
  g = new TGraph( x0s.size(), &x0s[0], &wids[0] );
  g->Draw("AC*");
  c.SaveAs("plots/wids.pdf");

  TF1 *fb = new TF1("fb","gaus(0)+pol0(3)",-1,3); fb->SetLineColor(kRed);

  TH1F* hAmp = new TH1F("hAmp","",40,0,10);
  
  constexpr int NTOYS=1000;
  for(int iToy=0; iToy<NTOYS; iToy++){
    h->Reset();
    for(int i=0;i<4000;i++) h->Fill( -1+4*r->Rndm() );
    for(int i=0;i<100/0.68;i++) h->Fill( r->Gaus(1,0.05) );
    h->Draw();
    fb->SetParameter(0, 20);
    fb->SetParameter(1, 1);
    fb->SetParameter(2, 0.05);
    fb->SetParameter(3, 10);
    h->Fit("fb","q");
    /* hAmp->Fill( fb->GetParameter(0) ); */
    hAmp->Fill( fb->GetParameter(0)/fb->GetParError(0) );
    if(iToy<3) c.SaveAs(Form("plots/pseudo_%d.pdf",iToy));
  }
  
  hAmp->Draw();
  c.SaveAs("plots/smp.pdf");
  
  /* cout << sigs << endl; */
  /* cout << wids << endl; */
  f->Close();
}

void run(){
  //genMC();
  fitSimple();
  gSystem->Exit(0);
}
