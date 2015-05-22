import os, sys, copy, math, numpy
import subprocess as sp
from ROOT import *

do_test = False

txt_file_path = os.environ["LQANA"] + "optimizationCuts_enujj_MTandMET.txt"
mc_filepath = os.environ["LQDATA"] + "/enujj_analysis/enujj_opt_METandMT//output_cutTable_lq_enujj_opt_METandMT/analysisClass_lq_enujj_plots.root"
qcd_data_filepath = os.environ["LQDATA"] + "/enujj_analysis/enujj_qcd_opt_METandMT//output_cutTable_lq_enujj_opt_METandMT/analysisClass_lq_enujj_QCD_plots.root"

no_mt_tuples = [ 
    ('500', '100', '250'),
    ('600', '100', '300'),
    ('700', '125', '350'),
    ('800', '150', '400'),
    ('900', '200', '450'),
    ('1000', '200', '450'),
    ('1000', '200', '500'),
    ('1100', '225', '550'),
    ('1200', '275', '550'),
    ('1200', '275', '600'),
    ('1300', '275', '600'),
    ('1400', '250', '750'),
    ('1500', '250', '750'),
    ('1500', '250', '750'),
    ('1500', '250', '750'),
    ('1700', '350', '800'),
    ('1700', '350', '800'),
    ('1800', '350', '750'),
    ('1800', '350', '750')
]

mej_cuts = [ 200, 
             250, 
             300, 
             350, 
             400, 
             450, 
             500, 
             550, 
             600, 
             650, 
             700, 
             750, 
             800, 
             800, 
             800, 
             800, 
             800, 
             800, 
             800 ]    

txt_file = open ( txt_file_path, "r" ) 

l_cut_variables = []
l_bin_numbers = []

d_cutVariable_cutValues = {} 
d_binNumber_cutTuple = {}
d_cutTuple_binNumber = {}
d_binNumber_line = {}
d_cutVariable_maxCutValues = {}

d_background_filepaths = { 
    "ttbar" : [ "TTbar_Madgraph", mc_filepath        , 1.0  ],
    "qcd"   : [ "DATA"          , qcd_data_filepath  , 1.0  ],
    "wjet"  : [ "WJet_Madgraph" , mc_filepath        , 1.0  ],
    "zjet"  : [ "ZJet_Madgraph" , mc_filepath        , 1.0  ],
    "stop"  : [ "SingleTop"     , mc_filepath        , 1.0  ],
    "vv"    : [ "DIBOSON"       , mc_filepath        , 1.0  ],
    "gjet"  : [ "PhotonJets"    , mc_filepath        , 1.0  ] 
}


d_qcd_filepath = { 
    "qcd"   : [ "DATA"          , qcd_data_filepath  , 1.0  ]
}

d_ttbar_filepath = { 
   "ttbar" : [ "TTbar_Madgraph", mc_filepath        , 1.0  ]
}

d_wjet_filepath = {
    "wjet"  : [ "WJet_Madgraph"   , mc_filepath        , 1.0  ]
}

d_other_filepath = {
    "stop"  : [ "SingleTop"     , mc_filepath        , 1.0  ],
    "vv"    : [ "DIBOSON"       , mc_filepath        , 1.0  ],
    "gjet"  : [ "PhotonJets"    , mc_filepath        , 1.0  ], 
    "zjet"  : [ "ZJet_Madgraph"   , mc_filepath        , 1.0  ]
}

d_signal_filepaths_list = [ 
    { "300"  : ["LQ_M300" , mc_filepath, 1.0 ] } ,
    { "350"  : ["LQ_M350" , mc_filepath, 1.0 ] } ,
    { "400"  : ["LQ_M400" , mc_filepath, 1.0 ] } ,
    { "450"  : ["LQ_M450" , mc_filepath, 1.0 ] } ,
    { "500"  : ["LQ_M500" , mc_filepath, 1.0 ] } ,
    { "550"  : ["LQ_M550" , mc_filepath, 1.0 ] } ,
    { "600"  : ["LQ_M600" , mc_filepath, 1.0 ] } ,
    { "650"  : ["LQ_M650" , mc_filepath, 1.0 ] } ,
    { "700"  : ["LQ_M700" , mc_filepath, 1.0 ] } ,
    { "750"  : ["LQ_M750" , mc_filepath, 1.0 ] } ,
    { "800"  : ["LQ_M800" , mc_filepath, 1.0 ] } ,
    { "850"  : ["LQ_M850" , mc_filepath, 1.0 ] } ,
    { "900"  : ["LQ_M900" , mc_filepath, 1.0 ] } ,
    { "950"  : ["LQ_M950" , mc_filepath, 1.0 ] } ,
    { "1000" : ["LQ_M1000", mc_filepath, 1.0 ] } ,
    { "1050" : ["LQ_M1050", mc_filepath, 1.0 ] } ,
    { "1100" : ["LQ_M1100", mc_filepath, 1.0 ] } ,
    { "1150" : ["LQ_M1150", mc_filepath, 1.0 ] } ,
    { "1200" : ["LQ_M1200", mc_filepath, 1.0 ] } ,
]


d_data_filepaths =  {"DATA" : [ "DATA", mc_filepath, 1.0 ] }

n_mass_points = len ( d_signal_filepaths_list )

def evaluation ( nS, nB, eS, eB ) :

    if ( nS + nB != 0.0 ):
        value = nS / ( math.sqrt ( nS + nB ) )
    else:
        value = 0.0
    eValue = 0
    return value, eValue

def evaluate ( bin_number, d_signal, d_background, d_eSignal, d_eBackground ) :
    nS = d_signal     [ bin_number ] 
    nB = d_background [ bin_number ] 
    eS = d_eSignal    [ bin_number ] 
    eB = d_eBackground[ bin_number ] 

    v, eV  = evaluation ( nS, nB, eS, eB ) 
    return v, eV

def tuple_to_bins ( cut_tuple ) : 
    
    bins = []

    for i_cut_value, cut_value in enumerate(cut_tuple):
        cut_variable = l_cut_variables [ i_cut_value ]
        cut_value_bin = d_cutVariable_cutValues[cut_variable].index  ( cut_value ) 
        bins.append ( cut_value_bin ) 

    return bins

def bins_to_tuple ( cut_bins ) : 
    
    cut_list = []
    for i_bin, bin in enumerate(cut_bins):
        cut_variable = l_cut_variables [ i_bin ] 
        cut_value = d_cutVariable_cutValues [cut_variable][bin]
        cut_list.append ( cut_value ) 

    return tuple ( cut_list )


def parse_root_file( d_input ) :
    d_binNumber_nSample = {}
    d_binNumber_eSample = {}

    made_hist = False
    
    sum_hist = TH1F()

    for sample in d_input.keys():
        
        sample_name = d_input[sample][0]
        sample_file = TFile ( d_input[sample][1] ) 
        sample_scale = float ( d_input[sample][2] ) 
        hist_name = "histo1D__" + sample_name + "__Optimizer"
        
        hist = sample_file.Get(hist_name)
        hist.Scale ( sample_scale ) 

        if not made_hist:
            sum_hist = copy.deepcopy ( hist ) 
            made_hist = True
        else:
            sum_hist.Add ( hist ) 
        
        sample_file.Close() 
        
    nbins = sum_hist.GetNbinsX() 
    
    for ibin in range (0, nbins + 1 ) :

        plot_bin = sum_hist.FindBin ( ibin ) 

        d_binNumber_nSample [ ibin ] = sum_hist.GetBinContent ( plot_bin )
        d_binNumber_eSample [ ibin ] = sum_hist.GetBinError   ( plot_bin )
    
    return d_binNumber_nSample, d_binNumber_eSample

for line in txt_file:

    l_line_split = line.split()

    if len ( l_line_split ) == 0: continue

    # if line.split()[-1] != "50" : continue
    
    bin_number = int ( l_line_split [2] )

    l_bin_numbers.append ( bin_number ) 

    l_bin_cut_values = []
    
    cut_variable = ""

    for i_entry, entry in enumerate(l_line_split[3:]):
        
        if i_entry % 3 == 0: # variable name

            cut_variable = entry

            if cut_variable not in l_cut_variables: 
                l_cut_variables.append ( cut_variable ) 
            if cut_variable not in d_cutVariable_cutValues.keys():
                d_cutVariable_cutValues[cut_variable] = []

        if i_entry % 3 == 1 : # <, >, or = 
            continue 
                
        if i_entry % 3 == 2: # variable value
            cut_value = str ( entry ) 
            if cut_value not in d_cutVariable_cutValues[cut_variable]:
                d_cutVariable_cutValues [cut_variable].append ( cut_value )
            l_bin_cut_values.append ( cut_value ) 

    t_bin_cut_values = tuple ( l_bin_cut_values ) 
    
    d_binNumber_cutTuple [bin_number ] = t_bin_cut_values
    d_cutTuple_binNumber [t_bin_cut_values] = bin_number
    d_binNumber_line     [bin_number] = line.strip()

test_tuple = ('2200', '525', '950', '50')
test_bin_number = d_cutTuple_binNumber [ test_tuple ]
test_line = d_binNumber_line [ test_bin_number ]
test_bins = tuple_to_bins ( test_tuple )
test2_tuple = bins_to_tuple ( test_bins ) 

d_binNumber_nB, d_binNumber_eB = parse_root_file( d_background_filepaths )
d_binNumber_nD, d_binNumber_eD = parse_root_file( d_data_filepaths )

d_binNumber_nQCD  , d_binNumber_eQCD   = parse_root_file ( d_qcd_filepath ) 
d_binNumber_nWJets, d_binNumber_eWJets = parse_root_file ( d_wjet_filepath ) 
d_binNumber_nTTbar, d_binNumber_eTTbar = parse_root_file ( d_ttbar_filepath ) 
d_binNumber_nOther, d_binNumber_eOther = parse_root_file ( d_other_filepath ) 


if do_test:
    print "test_tuple =", test_tuple
    print "test_bin_number =", test_bin_number
    print "test_line =", test_line
    print "test_bins =", test_bins
    print "test2_tuple =", test2_tuple
    
    print "test_nQCD   = ", d_binNumber_nQCD  [test_bin_number]
    print "test_nWJets = ", d_binNumber_nWJets[test_bin_number]
    print "test_nTTbar = ", d_binNumber_nTTbar[test_bin_number]
    print "test_nOther = ", d_binNumber_nOther[test_bin_number]


    print "Processed bins:", l_bin_numbers[0], "-", l_bin_numbers[-1]
    print "Found", len ( l_cut_variables ), "cut variables:"
    for i_cut_variable, cut_variable in enumerate(l_cut_variables):
        cut_values = d_cutVariable_cutValues [ cut_variable ] 
        print "\t", "Cut variable #", i_cut_variable + 1 , ",", cut_variable, ", has", len ( cut_values ) , "cuts"
        for i_cut_value, cut_value in enumerate(cut_values):
            print "\t\t", "#", i_cut_value, ":" , cut_value
    sys.exit()

tex_file = open ("optimization.tex","w")

tex_file.write("\documentclass[10pt]{article}\n")
tex_file.write("\usepackage[landscape, top=1cm, bottom=1cm, left=1cm, right=1cm]{geometry}\n")
tex_file.write("\usepackage{amssymb}\n")
tex_file.write("\usepackage{amsmath}\n")
tex_file.write("\\begin{document}\n")
tex_file.write("\\begin{table}\n")

tex_line = "\\begin{tabular}{c|"
for mass in d_signal_filepaths_list: tex_line = tex_line + "c|"
tex_line = tex_line + "}\n"
tex_file.write(tex_line)

tex_file.write("\\cline{2-" + str ( n_mass_points + 1 ) + "} \n")
tex_file.write(" & \multicolumn{" + str ( n_mass_points ) + "}{|c|}{LQ Mass (evjj)} \\\ \n")
tex_file.write("\\cline{2-" + str ( n_mass_points + 1 ) + "} \n")

tex_line = ""
for mass in d_signal_filepaths_list: tex_line = tex_line + " & " + mass.keys()[0]
tex_line = tex_line + " \\\ \n"
tex_file.write(tex_line)

for i_signal_sample, signal_sample in enumerate(d_signal_filepaths_list):

    best_no_mt_tuple = no_mt_tuples[i_signal_sample]

    d_binNumber_nS, d_binNumber_eS = parse_root_file( signal_sample ) 

    max_bin = -999
    max_value = -999
    max_nS = -999
    max_nB = -999
    max_nD = -999
    max_nQCD = -999

    max_nWJets = -999
    max_nTTbar = -999
    max_nOther = -999

    max_eWJets = -999
    max_eTTbar = -999
    max_eOther = -999

    max_tuple = ()

    for binNumber in l_bin_numbers:
        nS = d_binNumber_nS [ binNumber ] 
        nB = d_binNumber_nB [ binNumber ] 
        nD = d_binNumber_nD [ binNumber ] 
        eS = d_binNumber_eS [ binNumber ] 
        eB = d_binNumber_eB [ binNumber ] 
        eD = d_binNumber_eD [ binNumber ] 

        nQCD = d_binNumber_nQCD [ binNumber ] 
        eQCD = d_binNumber_eQCD [ binNumber ] 
        
        nWJets = d_binNumber_nWJets [ binNumber ] 
        nTTbar = d_binNumber_nTTbar [ binNumber ] 
        nOther = d_binNumber_nOther [ binNumber ] 

        eWJets = d_binNumber_eWJets [ binNumber ] 
        eTTbar = d_binNumber_eTTbar [ binNumber ] 
        eOther = d_binNumber_eOther [ binNumber ] 

        this_tuple  = d_binNumber_cutTuple  [ binNumber ]
        no_mt_tuple = this_tuple[:-1]

        # if no_mt_tuple != best_no_mt_tuple: continue

        value, e_value = evaluate ( binNumber, d_binNumber_nS, d_binNumber_nB, d_binNumber_eS, d_binNumber_eB )

        if value >= max_value : 
            max_value = value
            max_bin = binNumber
            max_nS = nS
            max_nB = nB
            max_nD = nD
            max_eS = eS
            max_eB = eB
            max_eD = eD
            max_nQCD = nQCD
            max_eQCD = eQCD

            max_nWJets = nWJets
            max_nTTbar = nTTbar
            max_nOther = nOther

            max_eWJets = eWJets
            max_eTTbar = eTTbar
            max_eOther = eOther

            max_tuple = this_tuple

    # print signal_sample.keys()[0], ": Bin with best value was bin #" + str ( max_bin ), "\nCut info was:\t", max_tuple , "\nv = %.2f" % max_value, " nS = %.2f" % max_nS, " +/- %.2f" % max_eS, ", nB = %.2f" % max_nB, " +/- %.2f" % max_eB, ", nD = %d" % max_nD
    # 
    # print "\tQCD   =", max_nQCD,    "\t+/-\t", max_eQCD
    # print "\tWJets =", max_nWJets,  "\t+/-\t", max_eWJets
    # print "\tTTbar =", max_nTTbar,  "\t+/-\t", max_eQCD
    # print "\tOther =", max_nOther, "\t+/-\t", max_eOther
    # for i_cut_variable, cut_variable in enumerate(l_cut_variables):
    #     print "\t", cut_variable, "\t>\t" , max_tuple[i_cut_variable]
    
    print max_tuple

    max_bins = tuple_to_bins ( max_tuple) 
    test_max_tuple = bins_to_tuple ( max_bins ) 
    test_binNumber = d_cutTuple_binNumber [ test_max_tuple ]

    if test_max_tuple != max_tuple:
        print "ERROR: Something is wrong with how you map tuples to bins (tuple test)"
        sys.exit()

    if test_binNumber != max_bin : 
        print "ERROR: Something is wrong with how you map tuples to bins (bin test)"
        sys.exit()
        
        
    for i,cut_variable in enumerate(l_cut_variables):

        if cut_variable not in d_cutVariable_maxCutValues.keys():
            d_cutVariable_maxCutValues[ cut_variable ] = []

        this_bin = max_bins[i]

        this_cut_value = d_cutVariable_cutValues[ cut_variable][this_bin]

        n_bins = len ( d_cutVariable_cutValues [ cut_variable ] ) 

        x_values = []
        y_values = []
        
        for ibin in range ( 0, n_bins ):
            new_max_bins = max_bins[:i] + [ ibin ] + max_bins[i+1:]
            new_max_tuple = bins_to_tuple ( new_max_bins )
            new_max_binNumber = d_cutTuple_binNumber [ new_max_tuple ] 
            new_value, new_eValue = evaluate ( new_max_binNumber, d_binNumber_nS, d_binNumber_nB, d_binNumber_eS, d_binNumber_eB )
            new_cut = d_cutVariable_cutValues [ cut_variable ][ ibin ]
            
            x_values.append ( float ( new_cut ) )
            y_values.append ( float ( new_value ) ) 

        scan_graph = TGraph ( n_bins, numpy.array ( x_values ), numpy.array (y_values ))
        scan_canvas = TCanvas()
        scan_canvas.SetGridx()
        scan_canvas.SetGridy()
        scan_graph.Draw("AP")
        

        scan_graph.GetHistogram().GetXaxis().SetTitle("LQ M(" + signal_sample.keys()[0] + "), scan of " + cut_variable )
        scan_graph.GetHistogram().GetYaxis().SetTitle("Significance")
        scan_graph.SetMarkerStyle(20)
        scan_graph.Draw("AP")
        scan_canvas.SaveAs( "scan_gif/significanceScan_" + signal_sample.keys()[0] + "_" + cut_variable + ".gif" )
        
        d_cutVariable_maxCutValues[ cut_variable].append ( this_cut_value ) 

tex_file.write("\\hline \n")
tex_file.write("\\hline \n")

optimization_plots_file = TFile ("optimization_plots.root","RECREATE")
optimization_plots_file.cd()

for cut_variable in l_cut_variables:
    tex_line = "\multicolumn{1}{|c|}{" + cut_variable.replace ("_","\_") + "}"
    text_line = cut_variable + "\t" 
    x_values = []
    y_values = []
    for i_mass, mass in enumerate(d_signal_filepaths_list): 
        x_values.append ( float ( mass.keys()[0] ) ) 
        if cut_variable == "Mej_opt":
            y_values.append ( float ( mej_cuts[i_mass] ) ) 
            # y_values.append ( float (d_cutVariable_maxCutValues[cut_variable][i_mass] ) )
        else : 
            y_values.append ( float (d_cutVariable_maxCutValues[cut_variable][i_mass] ) )
        tex_line = tex_line + " & " + d_cutVariable_maxCutValues[cut_variable][i_mass]
    cut_graph = TGraph ( n_mass_points, numpy.array ( x_values ), numpy.array (y_values ))
    cut_graph.Write(cut_variable)
    tex_line = tex_line + " \\\ \n"
    tex_file.write(tex_line)
    tex_file.write("\\hline \n")

tex_file.write("\end{tabular}\n")
tex_file.write("\end{table}\n")
tex_file.write("\end{document}\n")
