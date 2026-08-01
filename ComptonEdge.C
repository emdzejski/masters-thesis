#include <iostream>
#include <fstream>
#include <algorithm> 
#include <iterator>
#include <filesystem> // for iterating over files in the directory

namespace fs = std::filesystem;


TH1D* MovingAverage(TH1D* h_original, int window) {
    
    TH1D* h_smoothed = (TH1D*)h_original->Clone(Form("%s_ma", h_original->GetName())); // ma == moving average
    h_smoothed->SetTitle(Form("%s (Moving Average)", h_original->GetTitle() ));
    h_smoothed->Reset(); 

    int nBins = h_original->GetNbinsX();
    int half_window = window/2;

    for (int i = 1 + half_window; i <= nBins - half_window; ++i) {
        double sum = 0;

        // Loop over the window around bin 'i'
        for (int j = i - half_window; j <= i + half_window; ++j) 
        {
            sum += h_original->GetBinContent(j);
        }
        double mean = sum / window;
        h_smoothed->SetBinContent(i, mean);
    }

    return h_smoothed;
}

TH2D* sum_histos(std::string path = "/home/jpet/ccb_dane/djpet_ccb/ccb_ssd/DJ_2021.10.24_0004")
{   
    //TCanvas *can = new TCanvas("can", "My Canvas", 800, 600);
    TH2D* hSum = nullptr; //pointer for the sum histo

    // Iterate through the directory
    for (const auto& entry : fs::directory_iterator(path)) {
        // Check if the file has a .root extension
        if (entry.path().extension() == ".root") {
            std::string file_path = entry.path().string();
            
            // Open the ROOT file
            TFile* file = TFile::Open(file_path.c_str(), "READ");
            
            // Safety check
            if (!file || file->IsZombie()) {
                std::cerr << "Error opening " << file_path << std::endl;
                continue;
            }

            TDirectory *dir = file->GetDirectory("HitFinder subtask 3 stats;1");
            if (!dir) 
            {
            std::cerr << "Error: Directory not found!" << std::endl;
            continue;
            }

            TH2D *hist = (TH2D*)dir->Get("hit_tot_scin");

            if (hSum == nullptr) 
            {

            //cloning the frist file to have the same binning structure for the sum
            hSum = (TH2D*)hist->Clone("hSum_total");
            
            hSum->SetDirectory(0); 
            hSum->SetTitle("Sum of hit_tot_scin from off-beam files");
            } 
            else 
            {
                hSum->Add(hist);
            }
                
            file->Close();    
        }
    }

    return hSum;
}



void ComptonEdge()
{
    gROOT->SetBatch(kTRUE);
    gStyle->SetOptTitle(0); //no titles in graphs/histos
    gStyle->SetOptStat(0); //no stats box
    gStyle->SetTitleOffset(1.2, "Y");
    gStyle->SetTitleOffset(1.1, "X");
   

    
    double tot_340 = 168301.0; //[ps]; ToT value corresponding to 340 keV energy 
    std::ofstream edges("compt_edge_pos.txt"); //output file with positions of compton edges
    std::ofstream edgesNorm("compt_edge_pos_norm.txt");

    std::string offBeamFiles = "/home/jpet/ccb_dane/djpet_ccb/ccb_ssd/DJ_2021.10.24_0004"; //files path 
    TString saveDir = "/home/jpet/ccb_dane/DJ_2021.10.24_0004_graphs/"; //path for saving graphs

    //getting a summed 2D histo of ToT val. vs scin ID form off-beam files
    TH2D *sumHist = sum_histos(offBeamFiles);
    sumHist->SetTitle("");
    TGraph *gr = new TGraph(312); // graph for ToT compton edge values
    gr->GetXaxis()->SetTitle("scin ID");
    gr->GetYaxis()->SetTitle("ToT [ps]");
    gr->SetMarkerStyle(20); 
    
    int nBins2Dx = sumHist->GetNbinsX();
    
    TCanvas *can1 = new TCanvas("can1", "My Canvas", 800, 600);
    can1->SetMargin(0.15, 0.15, 0.15, 0.1);
    // gPad->SetLeftMargin(0.15);
    // gPad->SetBottomMargin(0.15);

    can1->cd();
    sumHist->Draw("colz");
    //can1->SaveAs(saveDir + "hits_tot_scin.png");
    can1->SaveAs(saveDir + "hits_tot_scin.root");
    
    TCanvas *can2 = new TCanvas("can2", "My Canvas", 800, 600);
    TCanvas *can3 = new TCanvas("can3", "My Canvas", 800, 600);
    // gPad->SetLeftMargin(0.15);
    // gPad->SetBottomMargin(0.15);
    if (edges.is_open()) 
    {
        for (int i = 1; i <= nBins2Dx; i++)
        {
            TH1D *projY = sumHist->ProjectionY("myProjY", i,i);
            projY->GetYaxis()->SetTitle("counts");
            projY->GetYaxis()->SetTitleOffset(1.6);
            projY->SetTitle("");

            int scinID = sumHist->GetXaxis()->GetBinCenter(i);
            TH1D *histDeriv = (TH1D*)projY->Clone("histDeriv");
            histDeriv->Reset(); 
            histDeriv->GetYaxis()->SetTitle("derivative [1/ps]");
            histDeriv->SetTitle("");
            //smoothing the projection by applying moving average 
            TH1D *projY_avrg = MovingAverage(projY,5); 
            //projY->Smooth();

            int nBins = projY_avrg->GetNbinsX();

            //Loop over the bins to calculate the slope
            for (int j = 1; j < nBins; ++j) 
            { 
                double dy = projY_avrg->GetBinContent(j + 1) - projY_avrg->GetBinContent(j);
                
                double dx = projY_avrg->GetBinCenter(j + 1) - projY_avrg->GetBinCenter(j);
                
                
                if (dx != 0) 
                {
                    histDeriv->SetBinContent(j, dy / dx);
                }
            }

            histDeriv->GetXaxis()->SetRangeUser(145000, 190000);
            double minBin = histDeriv->GetMinimumBin();
            double minX = histDeriv->GetXaxis()->GetBinCenter(minBin);
            histDeriv->GetXaxis()->UnZoom();
            
            
            // myParabola->SetRange(minX-0.15*minX, minX + 0.15*minX);
            // TFitResultPtr res = histDeriv->Fit("myParabola", "RS");
            // //getting the chi2 parameter 
            
            //setting the fit range as minBin +- 7.5%
            histDeriv->Fit("pol2","QW", "", minX-0.075*minX, minX + 0.075*minX); //"Q"-> does not print result on the screen; "W" -> ignores errors 
            TF1 *res = histDeriv->GetFunction("pol2");
            res->SetLineWidth(3);
            
            // double fitQual = res->GetChisquare();
            // chi2.push_back(fitQual);
            histDeriv->GetXaxis()->SetRangeUser(100000, 250000);
            can2->cd();
            can2->SetMargin(0.12, 0.105, 0.12, 0.10);
            can2->Update();
            histDeriv->Draw();
            TLegend *leg = new TLegend(0.65, 0.75, 0.9, 0.9); 
            leg->SetBorderSize(0); //removes the border around the legend
            leg->SetFillStyle(0); //transparent background 
            leg->AddEntry(res, "quadratic function", "l"); // "l" -> draws a line in the legend
            leg->Draw();
            can2->SaveAs(saveDir + Form("fits/fit_compt_edge_scinID_%i.png", scinID));
            // if(scinID == 230)
            // {
            //     can2->SaveAs(saveDir + Form("fit_compt_edge_scinID_%i.root", scinID));
            // }

            //calculating the parabola vertex 
            double b = res->GetParameter(1);
            double a = res->GetParameter(2);
            double edgePos = -b/(2*a);
            
            //writing into file
            edges << scinID << " " << edgePos << "\n"; 
            edgesNorm << scinID << " " << tot_340/edgePos << "\n";


            //filling the graph
            gr->SetPoint(i-1,scinID,edgePos);

            //saving the projection with marked compt edge position
            can3->cd();
            can2->SetMargin(0.15, 0.05, 0.15, 0.10);
            can3->Update();
            projY->Draw();
            can3->Update();

            //line indicating the comton edge pos
            double ymin = gPad->GetUymin();
            double ymax = gPad->GetUymax();
            TLine* edge = new TLine(edgePos,ymin,edgePos,ymax);
            edge->SetLineColor(kRed);
            edge->SetLineWidth(3);
            edge->Draw("same");
            TLegend *legProj = new TLegend(0.65, 0.75, 0.9, 0.9); 
            legProj->SetBorderSize(0); //removes the border around the legend
            legProj->SetFillStyle(0); //transparent background 
            legProj->AddEntry(edge, "Compton edge", "l"); // "l" -> draws a line in the legend
            legProj->Draw();
            can3->SaveAs(saveDir + Form("projY_compt_edge/proj_%i.png", scinID));
            // if(scinID == 230)
            // {
            //    can3->SaveAs(saveDir + Form("proj_%i.root", scinID));
            // }
        }


        edges.close();

        //saving the graph with ToTs
        TCanvas *can4 = new TCanvas("can4", "My Canvas", 800, 600);
        can4->cd();
        //can->Update();
        gr->SetMinimum(80000);
        gr->SetMaximum(200000);
        gr->SetTitle("");
        gr->Draw("AP");
        can4->SaveAs(saveDir + "tots_edges.png");
        can4->SaveAs(saveDir + "tots_edges.root");
    }
    else
    {
        cout << "File didnt open :(" << endl;
    }
   
}