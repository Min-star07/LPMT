//
// Created by Min Li on 2023/6/27.
//
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
#include <TLegend.h>
#include <TStyle.h>
using namespace std;

int main(){

    TString filename[3] = {"2023-6-26_SPMT1_1150V_LED_ext.root", "2023-6-26_SPMT1_1200V_LED_ext.root",
                           "2023-6-27_SPMT1_1250V_LED_ext.root"};
    TString histname[2] ={"charge", "amplitude"};
    TH1F* hist[3][2]; //3 3个root文件， 2：图
    //得到每一个root文件里面的charge， amplitude直方图
    for (int i = 0; i < 3; i++) {
        //read root
        cout << filename[i] << endl;
        //TString infilepath = "/uraid5/dengmn/SPMT/1/";
        TString inputfilename = filename[i];
        TFile *inputfile = new TFile(inputfilename);
        cout << "open success" << endl;

        for(int j = 0; j < 2; j ++)
        {
            cout <<  histname[j] << endl;
            hist[i][j] = (TH1F*)inputfile->Get(histname[j]);
            cout << i << '\t' << j  <<"\t" << histname[j] << endl;
        }

    }
    //画图
    TCanvas* c1 = new TCanvas("c1", "c1", 1200, 900);
    gStyle->SetOptStat(0);
    c1->SetFillColor(0);
    c1->SetTopMargin(0.05);;
    c1->SetBottomMargin(0.12);
    c1->SetRightMargin(0.05);
    c1->SetLeftMargin(0.12);
    gPad->SetLogy();
    hist[0][0]->SetTitle("");
    hist[0][0]->SetLineColor(2);
    hist[0][0]->SetLineWidth(3.);
    hist[0][0]->GetYaxis()->SetTitle("count");
    hist[0][0]->GetXaxis()->SetTitle("charge [pC]");
    hist[0][0]->GetYaxis()->CenterTitle();
    hist[0][0]->GetXaxis()->CenterTitle();
    hist[0][0]->GetYaxis()->SetLabelSize(0.05);
    hist[0][0]->GetXaxis()->SetLabelSize(0.05);
    hist[0][0]->GetXaxis()->SetLabelFont(132);
    hist[0][0]->GetYaxis()->SetLabelFont(132);
    hist[0][0]->GetXaxis()->SetTitleFont(132);
    hist[0][0]->GetYaxis()->SetTitleFont(132);
    hist[0][0]->GetYaxis()->SetTitleSize(0.05);
    hist[0][0]->GetXaxis()->SetTitleSize(0.05);
    hist[0][0]->SetLabelOffset(0.01,"xyz");
    hist[0][0]->SetTitleOffset(1.2, "xyz");
    hist[0][0]->GetYaxis()->SetTickSize(0.03);
    hist[0][0]->GetXaxis()->SetTickSize(0.03);
//    hist[0][0]->GetXaxis()->SetRangeUser(0, 2);
    hist[0][0]->Draw();
    hist[1][0]->SetLineColor(4);
    hist[1][0]->SetLineWidth(3.);
    hist[1][0]->Draw("same");
    hist[2][0]->SetLineColor(6);
    hist[2][0]->SetLineWidth(3.);
    hist[2][0]->Draw("same");

    //添加图例
    TLegend* led1 = new TLegend(0.7, 0.7, 0.9, 0.9);
    led1->SetTextFont(132);
    led1->SetTextSize(0.05);
    led1->SetFillColorAlpha(0, 0);
    led1->SetBorderSize(0);
    led1->AddEntry(hist[0][0], "1150V", "l");
    led1->AddEntry(hist[1][0], "1200V", "l");
    led1->AddEntry(hist[2][0], "1250V", "l");
    led1->Draw("same");

    c1->SaveAs("charge.pdf");
    return 0;
}