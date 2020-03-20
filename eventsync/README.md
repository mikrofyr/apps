### Description:
Script to download a list of sources.
Trigger when the config file is saved.
Abandons source if cannot connect.

### Case:
Sync data from phone ftp to server, config file edited remotely from server

### Usage:
eventsync -y config.yaml

### YAML:
Item  | Description
------------- | -------------
sources       | List of sources to download
outdir        | Location to store data
sync          | true=execute, false=dry run 
