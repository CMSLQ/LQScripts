import subprocess as sp
import os, sys, math

nuisance_parameter_pairs = [ 
    ["EESdown", "EESup" ],
    ["EER"    , "EER"   ],
    ["JESdown", "JESup" ],
    ["JER"    , "JER"   ],
    ["PUup"   , "PUdown"]
]

d_nuisanceParameter_title = {
    "ereco"  : "Electron efficiency"       ,
    "EESdown": "Electron energy scale"     ,
    "EESup"  : "Electron energy scale"     ,
    "EER"    : "Electron energy resolution",
    "JESdown": "Jet energy scale"          ,
    "JESup"  : "Jet energy scale"          ,
    "JER"    : "Jet energy resolution"     ,
    "PUup"   : "Pileup"                    ,
    "PUdown" : "Pileup"                    ,
    "lumi"   : "Luminosity"                ,
    "znorm"  : "Z normalization"           ,
    "zshape" : "Z shape"                   ,
    "qcd"    : "QCD multijet estimate"     ,
    "ttbar"  : "\\ttbar estimate"          ,
    "pdf"    : "PDF uncertainty"
}

d_nuisanceParameter_datFilePath = { 
    "EER"     : os.environ["LQDATA"] + "/eejj_analysis/eejj_EER/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat",
    "JER"     : os.environ["LQDATA"] + "/eejj_analysis/eejj_JER/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat",
    "EESup"   : os.environ["LQDATA"] + "/eejj_analysis/eejj_EESup/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat",
    "EESdown" : os.environ["LQDATA"] + "/eejj_analysis/eejj_EESdown/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat",
    "JESup"   : os.environ["LQDATA"] + "/eejj_analysis/eejj_JESup/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat",
    "JESdown" : os.environ["LQDATA"] + "/eejj_analysis/eejj_JESdown/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat",
    "PUdown"  : os.environ["LQDATA"] + "/eejj_analysis/eejj_PUdown/scaled_output_cutTable_lq_eejj_Systematics_PUdown/analysisClass_lq_eejj_tables.dat",
    "PUup"    : os.environ["LQDATA"] + "/eejj_analysis/eejj_PUup/scaled_output_cutTable_lq_eejj_Systematics_PUup/analysisClass_lq_eejj_tables.dat"
}


mean_scaledCombined_file_path   = os.environ["LQDATA"] + "eejj_analysis/eejj/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat"
qcd_file_path = os.environ["LQDATA"] + "eejj_analysis/eejj_qcd/output_cutTable_lq_eejj/analysisClass_lq_eejj_QCD_tables.dat"

mass_points = [ "300", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800", "850", "900", "950",  "1000",  "1050",  "1100",  "1150",  "1200" ]

gen_processes = []
for mass_point in mass_points: gen_processes.append ( "LQ_M" + mass_point ) 
gen_processes = gen_processes + [ 
    "WJet_Madgraph",   
    "ZJet_Madgraph",
    "DIBOSON",
    "PhotonJets",
    "SingleTop"
]

known_uncertainties = [ 
    "ereco",
    "lumi",
    "znorm",
    "zshape",
    "ttbar",
    "qcd",
    "pdf"
]

#--------------------------------------------------------------------------------
# Set mass varied uncertainties
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Set known uncertainties
#--------------------------------------------------------------------------------

d_knownUncertainty_mass_genProcess_value = {}

# LUMI 

d_knownUncertainty_mass_genProcess_value["lumi"] = {}
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["lumi"][mass_point] = {} 
    for gen_process in gen_processes:
        if gen_process == "ZJet_Madgraph":
            d_knownUncertainty_mass_genProcess_value["lumi"][mass_point][gen_process] = 0.0
        else:
            d_knownUncertainty_mass_genProcess_value["lumi"][mass_point][gen_process] = 0.026

# Electron efficiency (signal only)

electron_efficiency = 0.04
d_knownUncertainty_mass_genProcess_value["ereco"] = {} 
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["ereco"][mass_point] = {} 
    for gen_process in gen_processes:
        if "LQ" in gen_process:
            d_knownUncertainty_mass_genProcess_value["ereco"][mass_point][gen_process] = electron_efficiency
        else:
            d_knownUncertainty_mass_genProcess_value["ereco"][mass_point][gen_process] = 0.0

# QCD 

qcd_per_uncertainty = 0.30

d_knownUncertainty_mass_genProcess_value["qcd"] = {} 
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["qcd"][mass_point] = {} 
    for gen_process in gen_processes:
        d_knownUncertainty_mass_genProcess_value["qcd"][mass_point][gen_process] = 0.0

# ttbar

ttbar_per_uncertainty = 0.02

d_knownUncertainty_mass_genProcess_value["ttbar"] = {} 
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["ttbar"][mass_point] = {} 
    for gen_process in gen_processes:
        d_knownUncertainty_mass_genProcess_value["ttbar"][mass_point][gen_process] = 0.0

# Z normalization

d_knownUncertainty_mass_genProcess_value["znorm"] = {} 
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["znorm"][mass_point] = {} 
    for gen_process in gen_processes:
        d_knownUncertainty_mass_genProcess_value["znorm"][mass_point][gen_process] = 0.0
    d_knownUncertainty_mass_genProcess_value["znorm"][mass_point]["ZJet_Madgraph"] = 0.011

# Z shape

d_knownUncertainty_mass_genProcess_value["zshape"] = {} 
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["zshape"][mass_point] = {} 
    for gen_process in gen_processes:
        d_knownUncertainty_mass_genProcess_value["zshape"][mass_point][gen_process] = 0.0

d_knownUncertainty_mass_genProcess_value["zshape"]["300"] ["ZJet_Madgraph"] = 0.04
d_knownUncertainty_mass_genProcess_value["zshape"]["350"] ["ZJet_Madgraph"] = 0.06
d_knownUncertainty_mass_genProcess_value["zshape"]["400"] ["ZJet_Madgraph"] = 0.06
d_knownUncertainty_mass_genProcess_value["zshape"]["450"] ["ZJet_Madgraph"] = 0.11
d_knownUncertainty_mass_genProcess_value["zshape"]["500"] ["ZJet_Madgraph"] = 0.08
d_knownUncertainty_mass_genProcess_value["zshape"]["550"] ["ZJet_Madgraph"] = 0.08
d_knownUncertainty_mass_genProcess_value["zshape"]["600"] ["ZJet_Madgraph"] = 0.10
d_knownUncertainty_mass_genProcess_value["zshape"]["650"] ["ZJet_Madgraph"] = 0.17
d_knownUncertainty_mass_genProcess_value["zshape"]["700"] ["ZJet_Madgraph"] = 0.26
d_knownUncertainty_mass_genProcess_value["zshape"]["750"] ["ZJet_Madgraph"] = 0.22
d_knownUncertainty_mass_genProcess_value["zshape"]["800"] ["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["850"] ["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["900"] ["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["950"] ["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["1000"]["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["1050"]["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["1100"]["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["1150"]["ZJet_Madgraph"] = 0.30
d_knownUncertainty_mass_genProcess_value["zshape"]["1200"]["ZJet_Madgraph"] = 0.30

# TTBar shape


# PDF

d_knownUncertainty_mass_genProcess_value["pdf"] = {} 
for mass_point in mass_points:
    d_knownUncertainty_mass_genProcess_value["pdf"][mass_point] = {} 
    for gen_process in gen_processes:
        if "LQ" in gen_process:
            d_knownUncertainty_mass_genProcess_value["pdf"][mass_point][gen_process] = 0.02
        else:
            d_knownUncertainty_mass_genProcess_value["pdf"][mass_point][gen_process] = 0.00
    d_knownUncertainty_mass_genProcess_value["pdf"][mass_point]["ZJet_Madgraph"] = 0.03


d_nuisanceParameter_cardDataName = {
    "JER"     : "eejj_jer",
    "EER"     : "eejj_eer",
    "PUup"    : "eejj_pu" ,
    "PUdown"  : "eejj_pu" ,
    "JESup"   : "eejj_jes",
    "JESdown" : "eejj_jes",
    "EESup"   : "eejj_ees",
    "EESdown" : "eejj_ees"
}

d_nuisanceParameter_fileName = {
    "JER"     : "eejj_jer_card_info.py",
    "EER"     : "eejj_eer_card_info.py",
    "PUup"    : "eejj_pu_card_info.py",
    "PUdown"  : "eejj_pu_card_info.py",
    "JESup"   : "eejj_jes_card_info.py",
    "JESdown" : "eejj_jes_card_info.py",
    "EESup"   : "eejj_ees_card_info.py",
    "EESdown" : "eejj_ees_card_info.py"
}

d_genProcesses_cardProcessName = {
    "WJet_Madgraph" :"wjet" ,
    "ZJet_Madgraph" :"zjet" ,
    "DIBOSON"       :"vv"   , 
    "PhotonJets"    :"gjet" ,
    "SingleTop"     :"stop" 
}

preselection_cut_name = "sT_eejj_opt"
final_selection_cut_prefix = "min_M_ej_LQ"

def get_stdout ( command ) :
    output = sp.Popen ( command, shell=True, stdout=sp.PIPE ).communicate()[0]
    return output 


def getDictFromScaledCombinedDatFile ( file_path, combined_dataset ) : 
    
    file = open ( file_path ) 
    info = file.read() 

    d_cutName_nPassAndError = {} 

    combined_dataset_info = info.split(combined_dataset+"\n")[1].split("\n\n")[0]

    combined_dataset_info_lines = combined_dataset_info.split("\n") 

    for combined_dataset_info_line in combined_dataset_info_lines :
        if len ( combined_dataset_info_line.split() ) < 1: continue
        if "Npass" in combined_dataset_info_line : continue
        
        cut_name  = combined_dataset_info_line.split()[0]
        cut_nPass = float ( combined_dataset_info_line.split()[5] ) / 1000.
        cut_ePass = float ( combined_dataset_info_line.split()[6] ) / 1000.

        d_cutName_nPassAndError [ cut_name ] = [ cut_nPass, cut_ePass ]

    file.close() 

    return d_cutName_nPassAndError


d_iNuisanceParameterPair_genProcess_massPoint_minRatio = {}
d_iNuisanceParameterPair_genProcess_massPoint_maxRatio = {}
d_iNuisanceParameterPair_genProcess_massPoint_isOK     = {}

for i_nuisance_parameter_pair, nuisance_parameter_pair in enumerate(nuisance_parameter_pairs):

    if i_nuisance_parameter_pair not in d_iNuisanceParameterPair_genProcess_massPoint_minRatio.keys():
        d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair] = {}
    if i_nuisance_parameter_pair not in d_iNuisanceParameterPair_genProcess_massPoint_maxRatio.keys():
        d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair] = {}
    if i_nuisance_parameter_pair not in d_iNuisanceParameterPair_genProcess_massPoint_isOK.keys():
        d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair] = {}



    for nuisance_parameter in nuisance_parameter_pair:

        nuisance_dat_file_path = d_nuisanceParameter_datFilePath [ nuisance_parameter ]
        
        for gen_process in gen_processes:

            if gen_process not in d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair].keys():
                d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process] = {}
            if gen_process not in d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair].keys():
                d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process] = {}
            if gen_process not in d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair].keys():
                d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process] = {}

            d_nuisance_cutName_nPassAndError = getDictFromScaledCombinedDatFile ( nuisance_dat_file_path, gen_process ) 
            d_mean_cutName_nPassAndError     = getDictFromScaledCombinedDatFile ( mean_scaledCombined_file_path, gen_process ) 

            n_nuisance_preselection = d_nuisance_cutName_nPassAndError [preselection_cut_name][0]
            e_nuisance_preselection = d_nuisance_cutName_nPassAndError [preselection_cut_name][1]

            n_mean_preselection     = d_mean_cutName_nPassAndError     [preselection_cut_name][0]
            e_mean_preselection     = d_mean_cutName_nPassAndError     [preselection_cut_name][1]
            
            if n_mean_preselection != 0.0:
                ratio =  (n_nuisance_preselection - n_mean_preselection)  / n_mean_preselection
                
                e_ratio = abs ( ( ratio - 1.0 )  * math.sqrt ( ( ( e_nuisance_preselection / n_nuisance_preselection ) *
                                                                 ( e_nuisance_preselection / n_nuisance_preselection ) ) +
                                                               ( ( e_mean_preselection / n_mean_preselection ) *
                                                                 ( e_mean_preselection / n_mean_preselection ) ) ) )
                
            else:
                if n_nuisance_preselection == 0.0:
                    ratio = 1.0
                    e_ratio = 1.0
                else:
                    ratio = -999
                    e_ratio = -999

            
            if "pre" not in d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process].keys():
                d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process]["pre"] = [ 99999., 99999.]
            if "pre" not in d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process].keys():
                d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process]["pre"] = [ -99999., -99999.]
            if "pre" not in d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process].keys():
                d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process]["pre"] = ""
                
            
            if ratio > d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process]["pre"][0]:
                d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process]["pre"] = [ratio,e_ratio]
                
            if ratio < d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process]["pre"][0]:
                d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process]["pre"] = [ratio,e_ratio]
                        

            
            # print "\t\t","pre","\t %(n).4f +/- %(e).4f" % {"n":n_nuisance_preselection, "e":  e_nuisance_preselection },"\t %(n).4f +/- %(e).4f" % {"n":n_mean_preselection, "e":  e_mean_preselection },"\t %(n).4f +/- %(e).4f" % {"n":ratio, "e":  e_ratio },
            
            if e_mean_preselection / n_mean_preselection < 0.10:
                d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process]["pre"] = "OK"
                # print "OK"
            # else : 
            #     print ""
            
            for mass_point in mass_points:

                if mass_point not in d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process].keys():
                    d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][mass_point] = [ 99999., 99999.]
                if mass_point not in d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process].keys():
                    d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][mass_point] = [ -99999., -99999.]
                if mass_point not in d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process].keys():
                    d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process][mass_point] = ""
                    
                final_selection_cut_name = final_selection_cut_prefix + mass_point 

                n_nuisance_final_selection = d_nuisance_cutName_nPassAndError [final_selection_cut_name][0]
                e_nuisance_final_selection = d_nuisance_cutName_nPassAndError [final_selection_cut_name][1]
                
                n_mean_final_selection     = d_mean_cutName_nPassAndError     [final_selection_cut_name][0]
                e_mean_final_selection     = d_mean_cutName_nPassAndError     [final_selection_cut_name][1]

                if n_mean_final_selection != 0.0 and n_nuisance_final_selection != 0.0:
                    ratio = ( n_nuisance_final_selection - n_mean_final_selection ) / n_mean_final_selection
                    
                    e_ratio = abs ( ( ratio - 1. )  * math.sqrt ( ( ( e_nuisance_final_selection / n_nuisance_final_selection ) *
                                                                    ( e_nuisance_final_selection / n_nuisance_final_selection ) ) +
                                                                  ( ( e_mean_final_selection / n_mean_final_selection ) *
                                                                    ( e_mean_final_selection / n_mean_final_selection ) ) ) )
                else:
                    if n_nuisance_final_selection == 0.0:
                        ratio = 1.0
                        e_ratio = 1.0
                    else:
                        ratio = -999
                        e_ratio = -999

                if ratio > d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][mass_point][0]:
                    d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][mass_point] = [ratio,e_ratio]

                if ratio < d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][mass_point][0]:
                    d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][mass_point] = [ratio,e_ratio]
                        

            
                # print "\t\t",mass_point,"\t %(n).4f +/- %(e).4f" % {"n":n_nuisance_final_selection, "e":  e_nuisance_final_selection },"\t %(n).4f +/- %(e).4f" % {"n":n_mean_final_selection, "e":  e_mean_final_selection },"\t %(n).4f +/- %(e).4f" % {"n":ratio, "e":  e_ratio },

                if n_mean_final_selection != 0.0 and e_mean_final_selection / n_mean_final_selection < 0.10: 
                    d_iNuisanceParameterPair_genProcess_massPoint_isOK[i_nuisance_parameter_pair][gen_process][mass_point] = "OK"
                    # print "OK"
                # else : print ""


# print "\n\n\n"
      
d_nuisanceParameterPair_massPoint_percentUncertaintyBackground = {} 
d_nuisanceParameterPair_massPoint_percentUncertaintySignal     = {} 

d_knownUncertainty_massPoint_percentUncertaintyBackground = {}
d_knownUncertainty_massPoint_percentUncertaintySignal     = {} 
  
for i_nuisance_parameter_pair, nuisance_parameter_pair in enumerate(nuisance_parameter_pairs):
    print "--------------------------------------------------------------------------------"
    print nuisance_parameter_pair[0], nuisance_parameter_pair[1]
    print "--------------------------------------------------------------------------------"
    
    d_nuisanceParameterPair_massPoint_percentUncertaintyBackground[nuisance_parameter_pair[0]] = {}
    d_nuisanceParameterPair_massPoint_percentUncertaintySignal    [nuisance_parameter_pair[0]] = {}
    
    card_data_name = d_nuisanceParameter_cardDataName[nuisance_parameter_pair[0] ]
    file_name      = d_nuisanceParameter_fileName    [nuisance_parameter_pair[0] ]
    file = open ( file_name,"w" ) 

    card_process_name = "LQ"

    line = card_data_name + " = {}"
    print line,
    file.write(line + "\n")                                          

    line = "\n\n" + card_data_name + "[\""+ card_process_name + "\"] =  \t[\t"
    print line,
    file.write(line)                                          
    
    d_massPoint_totalSignal     = {}
    d_massPoint_totalSignalUnc  = {}
    
    d_massPoint_totalBackground = {}
    d_massPoint_totalUncSquared = {} 
    for mass_point in mass_points: 
        d_massPoint_totalBackground[mass_point] = 0.
        d_massPoint_totalUncSquared[mass_point] = 0.
        
    for gen_process in gen_processes:
        if "LQ" not in gen_process: continue
        
        for i_mass_point, mass_point in enumerate(mass_points):
            
            min_ratio = d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][mass_point][0]
            max_ratio = d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][mass_point][0]
            isOK      = d_iNuisanceParameterPair_genProcess_massPoint_isOK    [i_nuisance_parameter_pair][gen_process][mass_point]

            e_min_ratio = d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][mass_point][1]
            e_max_ratio = d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][mass_point][1]

            if "LQ" in gen_process and mass_point not in gen_process: continue
            if "LQ" not in gen_process and mass_point != "300" : continue

            uncertainty = (100. * max ( abs ( min_ratio ), abs ( max_ratio ) ))
            n_pass = getDictFromScaledCombinedDatFile ( mean_scaledCombined_file_path, gen_process )[final_selection_cut_prefix + mass_point][0]
            d_massPoint_totalSignal   [mass_point] = n_pass
            d_massPoint_totalSignalUnc[mass_point] = uncertainty
            
            line = ""
            if   i_mass_point                     == 0: 
                line = "%.4f," % uncertainty
            elif i_mass_point == len(mass_points) -  1: 
                line = "\t\t\t\t %.4f" % uncertainty +  "   ]"
            else :                                      
                line = "\t\t\t\t %.4f," % uncertainty
            print line
            file.write(line + "\n")                                          


    for gen_process in gen_processes:
        if "LQ" in gen_process: continue
        card_process_name = d_genProcesses_cardProcessName[gen_process]
        
        line = "\n\n" + card_data_name + "[\""+ card_process_name + "\"] =  \t[\t"
        print line,
        file.write(line)
        
        default_mass_point = "300"
        print "\n"
        
        for i_mass_point, mass_point in enumerate(mass_points):

            min_ratio = d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][default_mass_point][0]
            max_ratio = d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][default_mass_point][0]
            isOK      = d_iNuisanceParameterPair_genProcess_massPoint_isOK    [i_nuisance_parameter_pair][gen_process][default_mass_point]

            e_min_ratio = d_iNuisanceParameterPair_genProcess_massPoint_minRatio[i_nuisance_parameter_pair][gen_process][default_mass_point][1]
            e_max_ratio = d_iNuisanceParameterPair_genProcess_massPoint_maxRatio[i_nuisance_parameter_pair][gen_process][default_mass_point][1]
            
            uncertainty = (100. * max ( abs ( min_ratio ), abs ( max_ratio )))
            n_pass = getDictFromScaledCombinedDatFile ( mean_scaledCombined_file_path, gen_process )[final_selection_cut_prefix + mass_point][0]
            abs_uncertainty = (uncertainty / 100.) * n_pass 

            d_massPoint_totalBackground[mass_point] = d_massPoint_totalBackground[mass_point] + n_pass
            d_massPoint_totalUncSquared[mass_point] = d_massPoint_totalUncSquared[mass_point] + ( abs_uncertainty * abs_uncertainty ) 

            line = ""
            if   i_mass_point                     == 0: 
                line = "%.4f," % uncertainty
            elif i_mass_point == len(mass_points) -  1: 
                line = "\t\t\t\t %.4f" % uncertainty + "   ]"
            else :                                      
                line = "\t\t\t\t %.4f," % uncertainty
            print line
            file.write(line + "\n")       

    # QCD

    line = "\n\n" + card_data_name + "[\"qcd\"] =  \t[\t"
    file.write(line)
    for i_mass_point, mass_point in enumerate(mass_points):
        uncertainty = 0.0
        if   i_mass_point                     == 0: 
            line = "%.4f," % uncertainty
        elif i_mass_point == len(mass_points) -  1: 
            line = "\t\t\t\t %.4f" % uncertainty + "   ]"
        else :                                      
            line = "\t\t\t\t %.4f," % uncertainty
        file.write(line + "\n")   

    # TTbar

    line = "\n\n" + card_data_name + "[\"ttbar\"] =  \t[\t"
    file.write(line)
    for i_mass_point, mass_point in enumerate(mass_points):
        uncertainty = 0.0
        if   i_mass_point                     == 0: 
            line = "%.4f," % uncertainty
        elif i_mass_point == len(mass_points) -  1: 
            line = "\t\t\t\t %.4f" % uncertainty + "   ]"
        else :                                      
            line = "\t\t\t\t %.4f," % uncertainty
        file.write(line + "\n")   
    
    for mass_point in mass_points: 
        signal_uncertainty = d_massPoint_totalSignalUnc[mass_point]
        n_qcd    = getDictFromScaledCombinedDatFile (qcd_file_path, "DATA")[final_selection_cut_prefix + mass_point][0] * 1000.
        n_ttbar  = getDictFromScaledCombinedDatFile (mean_scaledCombined_file_path, "TTbar_FromData")[final_selection_cut_prefix + mass_point][0] * 1000.
        d_massPoint_totalBackground[mass_point] = d_massPoint_totalBackground[mass_point] + n_qcd + n_ttbar
        n_background = d_massPoint_totalBackground[mass_point]
        uncertainty = math.sqrt ( d_massPoint_totalUncSquared[mass_point] ) 
        per_uncertainty = 100. * uncertainty / n_background 
        print nuisance_parameter_pair[0], "LQ M =", mass_point, ", background =", d_massPoint_totalBackground[mass_point], "+/-", uncertainty, "(%1.1f %%)" % per_uncertainty
        d_nuisanceParameterPair_massPoint_percentUncertaintyBackground [ nuisance_parameter_pair[0] ][mass_point] = float ( per_uncertainty    )
        d_nuisanceParameterPair_massPoint_percentUncertaintySignal     [ nuisance_parameter_pair[0] ][mass_point] = float ( signal_uncertainty )
    file.close()

for known_uncertainty in known_uncertainties:

    d_massPoint_totalBackground = {}
    d_massPoint_totalUncSquared = {} 
    d_massPoint_totalSignal     = {}
    d_massPoint_totalSignalUnc  = {}
    
    for mass_point in mass_points: 
        d_massPoint_totalBackground[mass_point] = float(0.)
        d_massPoint_totalUncSquared[mass_point] = float(0.)
        
    d_knownUncertainty_massPoint_percentUncertaintyBackground[known_uncertainty] = {}
    d_knownUncertainty_massPoint_percentUncertaintySignal    [known_uncertainty] = {}
    
    for gen_process in gen_processes:
        for mass_point in mass_points: 
            per_uncertainty = d_knownUncertainty_mass_genProcess_value [known_uncertainty][mass_point][gen_process]
            n_pass = getDictFromScaledCombinedDatFile ( mean_scaledCombined_file_path, gen_process )[final_selection_cut_prefix + mass_point][0]
            abs_uncertainty = per_uncertainty * n_pass
            
            if "LQ" not in gen_process:
                d_massPoint_totalBackground[mass_point] = d_massPoint_totalBackground[mass_point] + n_pass
                d_massPoint_totalUncSquared[mass_point] = d_massPoint_totalUncSquared[mass_point] + ( abs_uncertainty * abs_uncertainty ) 
            else:
                d_massPoint_totalSignal    [mass_point] = n_pass
                d_massPoint_totalSignalUnc [mass_point] = per_uncertainty

    for mass_point in mass_points:
        signal_uncertainty = d_massPoint_totalSignalUnc[mass_point] * 100.
        n_qcd   = getDictFromScaledCombinedDatFile (qcd_file_path, "DATA")[final_selection_cut_prefix + mass_point][0] * 1000.
        n_ttbar = getDictFromScaledCombinedDatFile (mean_scaledCombined_file_path, "TTbar_FromData")[final_selection_cut_prefix + mass_point][0] * 1000.
        qcd_abs_uncertainty   = n_qcd * qcd_per_uncertainty 
        ttbar_abs_uncertainty = n_ttbar * ttbar_per_uncertainty 
        if known_uncertainty == "lumi":
            print "*** mass =", mass_point, "n(background) =", n_background
        d_massPoint_totalBackground[mass_point] = d_massPoint_totalBackground[mass_point] + n_qcd + n_ttbar
        n_background = d_massPoint_totalBackground[mass_point]

        if known_uncertainty == "lumi":
            print "*** mass =", mass_point, "n(background) =", n_background

        uncertainty = math.sqrt ( d_massPoint_totalUncSquared[mass_point] ) 
        if ( known_uncertainty == "qcd" ):
            uncertainty = math.sqrt ( d_massPoint_totalUncSquared[mass_point] + ( qcd_abs_uncertainty * qcd_abs_uncertainty ) )
        if ( known_uncertainty == "ttbar" ):
            uncertainty = math.sqrt ( d_massPoint_totalUncSquared[mass_point] + ( ttbar_abs_uncertainty * ttbar_abs_uncertainty ) )
        per_uncertainty = 100. * uncertainty / n_background 
        d_knownUncertainty_massPoint_percentUncertaintyBackground [known_uncertainty][mass_point] = float ( per_uncertainty    )
        d_knownUncertainty_massPoint_percentUncertaintySignal     [known_uncertainty][mass_point] = float ( signal_uncertainty )

uncertainties = []

ereco = known_uncertainties.pop(0)
first_uncertainties = [ereco]

for mass_point in mass_points: 
    
    latex_file_path = "systematics_tex/systematics_eejj_LQM" + mass_point + ".tex"
    latex_file = open ( latex_file_path, "w" ) 

    latex_file.write("\\begin{table}[htbp] \n")
    latex_file.write("\\caption{Systematic uncertainties and their effects on signal and background in the \eejj~channel for M(LQ) = "+mass_point +" GeV final selection. All uncertainties are symmetric.} \n")
    latex_file.write("\\label{tab:syst_eejj_" + mass_point + "} \n")
    latex_file.write("\\begin{tabular}{| l | c | c |}\n")
    latex_file.write("\hline \n")
    latex_file.write("\hline \n")
    latex_file.write("Systematic & Signal (\%) & Background (\%) \\\ \n")
    latex_file.write("\hline \n")
    latex_file.write("\hline \n")

    signal_uncertainty_sqr     = 0.0
    background_uncertainty_sqr = 0.0
    
    for known_uncertainty in first_uncertainties:
        title = d_nuisanceParameter_title [known_uncertainty]
        signal_uncertainty     = d_knownUncertainty_massPoint_percentUncertaintySignal     [known_uncertainty][mass_point]
        background_uncertainty = d_knownUncertainty_massPoint_percentUncertaintyBackground [known_uncertainty][mass_point]
        signal_uncertainty_sqr     = signal_uncertainty_sqr     + ( signal_uncertainty     * signal_uncertainty     )
        background_uncertainty_sqr = background_uncertainty_sqr + ( background_uncertainty * background_uncertainty )
        latex_file.write ( title + " & %1.2f" % signal_uncertainty  + "\%" + " & %1.2f" % background_uncertainty + "\% \\\ \n" )

    for nuisance_parameter_pair in nuisance_parameter_pairs:
        title = d_nuisanceParameter_title [nuisance_parameter_pair[0]]
        signal_uncertainty     = d_nuisanceParameterPair_massPoint_percentUncertaintySignal     [nuisance_parameter_pair[0]][mass_point]
        background_uncertainty = d_nuisanceParameterPair_massPoint_percentUncertaintyBackground [nuisance_parameter_pair[0]][mass_point]
        signal_uncertainty_sqr     = signal_uncertainty_sqr     + ( signal_uncertainty     * signal_uncertainty     )
        background_uncertainty_sqr = background_uncertainty_sqr + ( background_uncertainty * background_uncertainty )
        latex_file.write ( title + " & %1.2f" % signal_uncertainty  + "\%" + " & %1.2f" % background_uncertainty + "\% \\\ \n" )

    for known_uncertainty in known_uncertainties:
        title = d_nuisanceParameter_title [known_uncertainty]
        signal_uncertainty     = d_knownUncertainty_massPoint_percentUncertaintySignal     [known_uncertainty][mass_point]
        background_uncertainty = d_knownUncertainty_massPoint_percentUncertaintyBackground [known_uncertainty][mass_point]
        signal_uncertainty_sqr     = signal_uncertainty_sqr     + ( signal_uncertainty     * signal_uncertainty     )
        background_uncertainty_sqr = background_uncertainty_sqr + ( background_uncertainty * background_uncertainty )
        latex_file.write ( title + " & %1.2f" % signal_uncertainty  + "\%" + " & %1.2f" % background_uncertainty + "\% \\\ \n" )

    latex_file.write("\hline \n")
    latex_file.write("\hline \n")
    
    
    signal_uncertainty     = math.sqrt ( signal_uncertainty_sqr     )
    background_uncertainty = math.sqrt ( background_uncertainty_sqr )

    uncertainties.append ( background_uncertainty ) 

    latex_file.write ( "Total & %1.2f" % signal_uncertainty  + "\%" + " & %1.2f" % background_uncertainty + "\% \\\ \n" )

    latex_file.write("\hline \n")
    latex_file.write("\hline \n")
    latex_file.write("\end{tabular}\n")
    latex_file.write("\end{table}\n")
    latex_file.close()

print "Put this in table / plot scripts: "
print "systematic_uncertainty = [", uncertainties[0] / 100., ","

for uncertainty in uncertainties[1:] :
    print "                          ", uncertainty / 100., ","

print "]"
