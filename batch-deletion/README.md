# Batch Deletion 

## Team - DevEx IDC
 - Vikas (Vikas.Bhansali@microsoft.com)
 - Narasimha (Narasimha.Kulkarni@microsoft.com)
 - Mohit (mohsha@microsoft.com)
 
 ## Input
 ```
usage: main.py [-h] -s CONNECTION_STRING [-p PARALLEL_FACTOR]

Batch Delete : Program to delete content in blob storage account

optional arguments:
  -h, --help            show this help message and exit
  -s CONNECTION_STRING, --connection-string CONNECTION_STRING
                        Connection string to the storage account
  -p PARALLEL_FACTOR, --parallel-factor PARALLEL_FACTOR
                        Parallel execution factor (OPTIONAL : default 8)
```

 ## How does it work 
* Simple Depth First Search Algorithm to delete the blobs.

 