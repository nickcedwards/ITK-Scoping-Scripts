for layout in VF_Gold VF_Gold_m10 VF_Silver VF_Silver_m10 Bronze Bronze_m10
do
  cp run_scoping_flatEff_23Jul/plots/Zmumu_flatEff_23Jul_1holes_${layout}/efficiencyPlot_etaSingleSidedMC.eps /Users/nedwards/Physics/Scoping/ScopingTrackingPerf/figures/flatCuts/${layout}_eff.eps
  cp run_scoping_flatEff_23Jul/plots/Zmumu_flatEff_23Jul_1holes_${layout}/frPlot_etaSingleSided.eps /Users/nedwards/Physics/Scoping/ScopingTrackingPerf/figures/flatCuts/${layout}_fr.eps
done
