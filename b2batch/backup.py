#!/usr/bin/env python3

import yaml
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Argparse example')
parser.add_argument('-y','--yaml', help='Some YAML file', required=True)
args = parser.parse_args()

with open(args.yaml, 'r') as f:
  doc = yaml.safe_load(f)


for item in doc['localhost']:
  cmd = "b2 sync --excludeAllSymlinks {} b2://nasse-primary{}".format(item,item)
  #cmd = "b2 sync --delete --excludeAllSymlinks {} b2://nasse-primary{}".format(item,item)
  print(cmd)
  subprocess.run(cmd, shell=True)

print("Done!")

#b2 sync --excludeAllSymlinks ${dir} b2://nasse-primary/${dir}
#b2 sync --excludeAllSymlinks --delete test2 b2://nasse-test/atest

#subprocess.run(["ls", "-l"])
#subprocess.run(["ls", "-l"])

