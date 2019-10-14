#! /bin/env python
''' Run limits for ADD diphoton analysis'''
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--blind', default=False, help="Run with blinded data observation")
parser.add_argument('-c', '--cards', default=False, help="Create full datacards")
parser.add_argument('-d', '--directory', default="../../diphoton-analysis/Tools/", help="Datacard directory.")
args = parser.parse_args()

blind_data = args.blind
create_cards = args.cards
relative_path = args.directory

ms_values = {'NED-2_KK-1': {3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000},
             'NED-4_KK-1': {3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000},
             'NED-2_KK-4': {3000, 3500, 4000, 4500, 5000, 5500, 6000}}

dimensions = {'NED-2_KK-1', 'NED-4_KK-1', 'NED-2_KK-4'}

extraOptions = "--rMax 2"
if blind_data:
    extraOptions += " --run blind"
else:
    extraOptions += ' --text2workspace "--max-bin 20"'

regions = {"BB", "BE"}
years = {"2016", "2017", "2018"}
for dimension in dimensions:
    for ms_value in ms_values[dimension]:
        name = 'ADDGravToGG_MS-' + str(ms_value) + '_' + dimension
        name_no_ms = 'ADDGravToGG_' + dimension
        if not blind_data:
            name += "_lowmass"
            name_no_ms += "_lowmass"
        if create_cards:
            fulldatacardcmd = "combineCards.py "
            outputdatacard = relative_path + "datacards/" + name + ".dat"
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
        os.system(cmd)
