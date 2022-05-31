#! /bin/env python
''' Run limits for ADD diphoton analysis'''
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--blind', default=False, help="Run with blinded data observation")
parser.add_argument('-c', '--cards', action='store_true', help="Create full datacards")
parser.add_argument('-d', '--directory', default="../../diphoton-analysis/Tools/", help="Datacard directory.")
parser.add_argument('-o', '--old', default=False, action='store_true', help="Use old 94X ADD samples.")
parser.add_argument('-y', '--years', default="2016,2017,2018", help="Comma delimited list of years to include in datacard.")
parser.add_argument('-r', '--run', default=False, action='store_true', help="Run limits.")
args = parser.parse_args()

blind_data = args.blind
create_cards = args.cards
relative_path = args.directory
use_old_ADD = args.old
datacard_years = args.years
run = args.run

ms_values = {'NED-2_KK-1': {3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000},
             'NED-4_KK-1': {3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000},
             'NED-2_KK-4': {3000, 3500, 4000, 4500, 5000, 5500, 6000},
             'NegInt-1':   {4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 9000, 10000, 11000, 13000},
             'NegInt-0':   {4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 9000, 10000, 11000, 13000}}

dimensions = []
if use_old_ADD:
    dimensions.extend(['NED-2_KK-1', 'NED-4_KK-1', 'NED-2_KK-4'])
else:
    dimensions.extend(['NegInt-1', 'NegInt-0'])

extraOptions = "--rMax 2"
if blind_data:
    extraOptions += " --run blind"
else:
    extraOptions += ' --text2workspace "--max-bin 20"'

regions = ["BB", "BE"]
years = datacard_years.split(',')
years_out_str = '_'.join(years)
for dimension in dimensions:
    for ms_value in ms_values[dimension]:
        name = 'ADDGravToGG_' + dimension + '_LambdaT-' + str(ms_value) + '_TuneCP2_13TeV-pythia8'
        name_no_ms = 'ADDGravToGG_' + dimension + '_TuneCP2_13TeV-pythia8'
        if use_old_ADD:
            name = 'ADDGravToGG_MS-' + str(ms_value) + '_' + dimension
            name_no_ms = 'ADDGravToGG_' + dimension
        if not blind_data:
            name_no_ms += "_lowmass"
        outputdatacard = relative_path + "datacards/" + name + '_' + years_out_str + ".dat"
        if create_cards:
            fulldatacardcmd = "combineCards.py "
            # combine datacards
            for year in years:
                for region in regions:
                    fulldatacardcmd += region + "_" + year + "=" + relative_path + "datacards/" + name + "_" + year + "_" + region + ".dat "
            fulldatacardcmd += " > " + outputdatacard
            print fulldatacardcmd
            # output combined datacard
            os.system(fulldatacardcmd)
            # hack to avoid bug in combineCards.py
            cmd = "sed -i 's|datacards/datacards|datacards|g' " + outputdatacard
            print cmd
            os.system(cmd)
        cmd = 'combine -M AsymptoticLimits ' + outputdatacard + ' ' + extraOptions + ' -n ' + name_no_ms + ' -m ' + str(ms_value)
        print cmd
        if run:
            os.system(cmd)