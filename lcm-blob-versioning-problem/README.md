# Blob Versioning Life Cycle Manager

## Team - DevEx IDC
 - Vikas (vikas.bhansali@microsoft.com)
 - Narasimha (narasimha.kulkarni@microsoft.com)
 - Mohit (mohsha@microsoft.com)
 
 ## Input
 
 Set connection string for the storage account as a part of environment variable: `AZURE_STORAGE_CONNECTION_STRING`
 ```
python main.py [-h] -c CONTAINER -b BLOB [-l | -d DELETE_VERSION | -a CREATE_VERSION | -g GET_VERSION | -x | -e SET_TIER_OF_VERSION] [-t BLOB_TYPE] [-f FILE] [-lt CONDITION_BEFORE_DATE]
               [-gt CONDITION_AFTER_DATE] [-bt] [-tr TIER]

Blob version life cycle manager

optional arguments:
  -h, --help            show this help message and exit
  -s CONNECTION_STRING, --connection-string CONNECTION_STRING
                        Connection string to the storage account
  -c CONTAINER, --container CONTAINER
                        Name of the container in storage account
  -b BLOB, --blob BLOB  Path to blob to be used (exclude container name here) e.g. Dir1/Dir2/file3.txt
  -l, --list-versions   List all available version of the blob
  -d DELETE_VERSION, --delete-version DELETE_VERSION
                        Delete specified version of blob
  -a CREATE_VERSION, --create-version CREATE_VERSION
                        Create a new version of blob by uploading the given file to blob. --blob-type is mandatory with this
  -g GET_VERSION, --get-version GET_VERSION
                        Download specified version of blob. Data will be stored in file specified in --file parameter
  -x, --delete-version-condition
                        Delete all versions of blob matching given date in --condition* option
  -e SET_TIER_OF_VERSION, --set-tier-of-version SET_TIER_OF_VERSION
                        Set tier of given version of blob. --tier and --blob-type are mandatory for this option
  -t BLOB_TYPE, --blob-type BLOB_TYPE
                        Type of blob [BlockBlob, PageBlob
  -f FILE, --file FILE  Path to local file to be used
  -lt CONDITION_BEFORE_DATE, --condition-before-date CONDITION_BEFORE_DATE
                        Match blob versions based on last modified date <= given date
  -gt CONDITION_AFTER_DATE, --condition-after-date CONDITION_AFTER_DATE
                        Match blob versions based on last modified date >= given date
  -bt, --condition-between-date
                        Match blob versions based on : <condition-before-date> >= last modified date >= <condition-after-date>
  -tr TIER, --tier TIER
                        Tier value for the blob

```

 ## Output 
 
 ### Add version
 ![Add version](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/lcm-blob-versioning-problem/lcm-blob-versioning-problem/output/create.png?raw=true)
 
 ### List all versions of the given blob
 ![Add version](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/lcm-blob-versioning-problem/lcm-blob-versioning-problem/output/list.png?raw=true)
 
  ### Download specific version
 ![Add version](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/lcm-blob-versioning-problem/lcm-blob-versioning-problem/output/download.png?raw=true)
 
 ### Delete specific version
 ![Add version](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/lcm-blob-versioning-problem/lcm-blob-versioning-problem/output/delete.png?raw=true)
 
  ### Delete all version with last modified time greater than specified time (inclusive)
 ![Add version](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/lcm-blob-versioning-problem/lcm-blob-versioning-problem/output/delete_greater_than.png?raw=true)
 
  ### ### Delete all version with last modified time between specified start and end time ((inclusive))
 ![Add version](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/lcm-blob-versioning-problem/lcm-blob-versioning-problem/output/delete_between.png?raw=true)
 