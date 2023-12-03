#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <TString.h>
#include <math.h>
#include <iomanip>

using namespace std;

int main() {

    //open root
    TString filename[3] = {"2023-6-26_SPMT1_1150V_LED_ext.root", "2023-6-26_SPMT1_1200V_LED_ext.root",
                           "2023-6-27_SPMT1_1250V_LED_ext.root"};

    for (int i = 0; i < 3; i++) {
        double baseline;
        double amplitude;
        double charge;
        double pe;
        double risetime;
        double falltime;
        double hittime;
        double FWHM;


        //read root
        cout << filename[i] << endl;
        TString infilepath = "/uraid5/dengmn/SPMT/1/";
        TString inputfilename = infilepath + filename[i];
        TFile *inputfile = new TFile(inputfilename);
        cout<<"open success" <<endl;

        TTree *mytree = (TTree *)inputfile->Get("Wave_channel0");
        mytree->SetBranchAddress("amplitude", &amplitude);
        mytree->SetBranchAddress("charge", &charge);

        //define root

        TString outfilename = filename[i];
        TString outfile = outfilename;
        TFile *outrootfile = new TFile(outfile, "RECREATE");
        TH1F *hist_charge = new TH1F("charge", "charge", 300, -2,4);
        TH1F *hist_amp = new TH1F("amplitude", "amplitude", 300, -2,4);


        int entries = (int) mytree->GetEntries();
        cout << "--------> test1 : " << entries << endl;
        for (int eventID = 0; eventID < entries; eventID++) {
            mytree->GetEntry(eventID);
            //cout << amplitude <<"\t" << charge << endl;
            hist_charge->Fill(charge);
            hist_amp->Fill(amplitude);
        }
        inputfile->Close();

        outrootfile->Write();
        outrootfile->Close();
    }
    return 0;
}

