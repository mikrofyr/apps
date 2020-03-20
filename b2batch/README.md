### Description:
Script to batch sync file trees to Backblaze B2 bucket

### Usage:
b2batch -y config.yaml

### YAML:
Item  | Description
------------- | -------------
localhost     | List of directories to sync
bucket        | Name of b2 bucket
delete        | Control --delete switch of 'b2 sync'
sync          | true=execute, false=dry run
