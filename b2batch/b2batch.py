#!/usr/bin/env python3

import yaml
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description='Argparse example')
parser.add_argument('-y','--yaml', help='Some YAML file', required=True)
args = parser.parse_args()

with open(args.yaml, 'r') as f:
  doc = yaml.safe_load(f)

if doc['bucket'] == None:
  sys.exit(0)

for item in doc['localhost']:
  bucket = doc['bucket']
  if doc['delete']:
    cmd = "b2 sync --delete --excludeAllSymlinks {} b2://{}{}".format(item,bucket,item)
  else
    cmd = "b2 sync --excludeAllSymlinks {} b2://{}{}".format(item,bucket,item)
  
  if doc['sync'] 
    print("Executing {}".format(cmd))
    subprocess.run(cmd, shell=True)
  else:
    print("Test run: {}".format(cmd))

print("Done!")
