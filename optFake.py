import ROOT as R
import math

def get_fr(gr, iP):
    fr, eta = R.Double(), R.Double()
    gr.GetPoint(iP, eta, fr)
    return fr

# optimise such that fr<target, but choose highest possible nHits that satisfies this
# without decreasing efficiency by less than eff_thresh relative to the minimum mHits that satisfies the fr<target
# requirement (ie require eff_N>eff_thresh*eff_Nmin)
def optimise_fake(tag, layout, nHoles, targets, eff_thresh=0.998):
    print
    rfname = "InDetUpPerfPlots_Zmumu_{}_{}.root".format(tag, layout)
    print tag, layout, nHoles
    rf = R.TFile(rfname)
    fake_grs = {}
    eff_grs = {}
    for nHits in [4,5,6,7,8,9,10,11,12,13,14]:
        if "VF" in rfname: extended = "_extendedEta"
        else: extended = ""
        fake_grs[nHits] = rf.Get("Zmumu_{}hits_{}holes{}/frPlot_etaSingleSided".format(nHits, nHoles, extended))
        eff_grs[nHits] = rf.Get("Zmumu_{}hits_{}holes{}/efficiencyPlot_etaSingleSidedMC".format(nHits, nHoles, extended))
    print "{:12}".format("eta"),
    for hits in fake_grs.keys(): print "{:<9}".format(hits),
    for t in targets: print "{:6.0e}".format(t),
    print
    etas = []
    cuts_targets = dict( [ (t, []) for t in targets ] )
    for iP in range(fake_grs[4].GetN()):
        fr, fr_e, eta, deta = R.Double(), R.Double(), R.Double(), R.Double()
        fake_grs[4].GetPoint(iP, eta, fr)
        deta = fake_grs[4].GetErrorX(iP)
        eta_low = eta-deta
        eta_high = eta+deta
        etas.append(eta_low)
        if "VF_Silver_m10" in rfname and eta_low>3.0: continue
        if "Silver" in rfname and eta_low>3.2: continue
        frs = [ (nHits, get_fr(gr, iP)) for nHits, gr in sorted(fake_grs.items()) ]
        effs = dict([ (nHits, get_fr(gr, iP)) for nHits, gr in sorted(eff_grs.items()) ])
        print "{:5.3}~{:5.3}  ".format(eta_low, eta_high),
        for hits, fr in frs: print "{:6.2e} ".format(fr),
        hits_cuts = []
        hits_cuts_min = []
        for t in targets:
            min_hits = reduce( lambda x,y: y[0] if not x and y[1]<t else x, frs, 0)
            cut = min_hits
            for nH in range(min_hits+1,15):
                if effs[nH]<eff_thresh*effs[min_hits]: break
                cut = nH
            hits_cuts.append(cut)
            hits_cuts_min.append(min_hits)
            cuts_targets[t].append(cut)
        for cut, min_cut in zip(hits_cuts, hits_cuts_min): print "{:6} {:6}".format(cut, min_cut),
        print
    etas.append(eta_high)
    ofilename = "varEtaCuts_{}_{}holes.py".format(layout, nHoles)
    ofile = file(ofilename, "w")
    ofile.write("eta_{} = {} \n".format(layout, repr(etas)))
    for t, cuts in cuts_targets.items():
        ofile.write( "eta_cuts_{}_{}holes_fr{} = {}\n".format(layout, nHoles, str(t).replace(".","p").replace("-","m"), repr(cuts)))
    ofile.close()

targets = [1e-2,2e-2,5e-2]
nHoles=0
tag = "flatEff_22Jul"
optimise_fake(tag, "Bronze_m10", nHoles, targets)
optimise_fake(tag, "Bronze", nHoles, targets)
optimise_fake(tag, "VF_Silver_m10", nHoles, targets)
optimise_fake(tag, "VF_Silver", nHoles, targets)
optimise_fake(tag, "VF_Gold_m10", nHoles, targets)
optimise_fake(tag, "VF_Gold", nHoles, targets)
#
optimise_fake(tag, "Silver_m10", nHoles, targets)
optimise_fake(tag, "Silver", nHoles, targets)
optimise_fake(tag, "Gold_m10", nHoles, targets)
optimise_fake(tag, "Gold", nHoles, targets)
#
