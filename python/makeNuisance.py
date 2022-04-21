import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-y', '--years', default="2016,2017,2018", help="Comma delimited list of years to include in datacard.")
args = parser.parse_args()

datacard_years = args.years
years = datacard_years.split(',')
years_out_str = '_'.join(years)

basename = "ADDGravToGG_NegInt-1_LambdaT-5000_TuneCP2_13TeV-pythia8_" + years_out_str


cmd = "combine -M FitDiagnostics ../../diphoton-analysis/Tools/datacards/" + basename + ".dat --rMax 2 -n " + basename + ' -m 5000 --plots --saveShapes  --text2workspace "--max-bin 20"'
print(cmd)
os.system(cmd)

cmd = "python test/diffNuisances.py fitDiagnostics" + basename + ".root -g diffNuisances_" + years_out_str + ".root"
print(cmd)
os.system(cmd)

cmd = "python test/diffNuisances.py fitDiagnostics" + basename + ".root -a --format=latex -g diffNuisances_" + years_out_str + ".root"
print(cmd)
os.system(cmd)

cmd = 'root -b -q plot_nuisances.cc\'("' + years_out_str + '")\''
print(cmd)
os.system(cmd)
