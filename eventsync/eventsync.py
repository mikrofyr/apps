#!/usr/bin/env python3

import argparse
import pyinotify
import yaml
import subprocess
import re

class SyncEngine:
  def __init__(self,config):
    with open(config) as file:
      ydata = yaml.load(file, Loader=yaml.FullLoader)
      print(ydata)
      self.sources = []
      for item in ydata['sources']:
        self.sources.append(item)
      self.outdir = ydata['outdir']
      self.doSync = ydata['sync']

  def sync(self):
    for source in self.sources:
      print("Proessing {}".format(source))
     
      # Create destination folder with no special characters
      #protocol://192.168.10.111:9999/path/to/file
      m_dest = re.match( r'^[a-zA-Z]+://([0-9\.:]+)/.*', source)
      if m_dest:
        src = m_dest.group(1)
        dst = src.replace(":","_")
      else:
        print("Error: Invalid format for {}".format(source))
        return
      
      # Fetch by wget, then fix name
      cmd = "cd {}; wget -r {} && mv {} {}".format(self.outdir,source, src,dst)
      try: 
        if self.doSync:
          print("Executing: '{}'".format(cmd))
          subprocess.run(cmd,shell=True)
        else:
          print("Test run: '{}'".format(cmd))
      except:
        print("Failed to sync {}".format(source))
      
class MyEventHandler(pyinotify.ProcessEvent):
  
  def __init__(self, config):
    self.config = config
  
  def process_IN_ACCESS(self, event):
    a=10 # print("Event")

  def process_IN_ATTRIB(self, event):
    a=10 # print("Event")

  def process_IN_CLOSE_NOWRITE(self, event):
    a=10 # print("Event")

  def process_IN_CLOSE_WRITE(self, event):
    a=10 # print("Event")
    #try: 
    handler = SyncEngine(self.config)
    handler.sync()
    #except:
    #  print("Issue handling request")

  def process_IN_CREATE(self, event):
    a=10 # print("Event")

  def process_IN_DELETE(self, event):
    a=10 # print("Event")

  def process_IN_MODIFY(self, event):
    a=10 # print("Event")
  
  def process_IN_OPEN(self, event):
    a=10 # print("Event")

# -- Script
parser = argparse.ArgumentParser(description='esync')
parser.add_argument('-y','--yaml', help='Some YAML file', required=True)
args = parser.parse_args()

# watch manager
#config = "/srv/droppy/files/Pictures/sync.yaml"
wm = pyinotify.WatchManager()
wm.add_watch(args.yaml, pyinotify.ALL_EVENTS, rec=True)

# event handler
eh = MyEventHandler(args.yaml)

# notifier
notifier = pyinotify.Notifier(wm, eh)
notifier.loop()
