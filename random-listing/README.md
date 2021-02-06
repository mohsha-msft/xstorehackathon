# Batch Deletion 

## Team - DevEx IDC
 - Vikas (Vikas.Bhansali@microsoft.com)
 - Narasimha (Narasimha.Kulkarni@microsoft.com)
 - Mohit (mohsha@microsoft.com)
 

## How does it work 
    * Using connection string (provided as input), a list of containers is obtained from storage account

    * Root directory for each container is pushed into worker queue

    * Based on parallelism factor (default 8) number of worker threads are started

    * Each thread takes the next request in worker queue and tries to iterate one level of directories and blobs on that path

    * On encountering a new directory in the path, another item is pushed to the worker queue for further iteration

    * Post iterating each level a summary of that level is created and pushed in output queue

    * A consolidator thread picks up these summary items and list the blobs giving a psuedo-random listing behaviour

  
## Input
```
usage: main.py [-h] [-s CONNECTION_STRING] [-p PARALLEL_FACTOR] [-f OUTPUT_FILE]

Batch Delete : Program to delete content in blob storage account

optional arguments:
  -h, --help            show this help message and exit
  -s CONNECTION_STRING, --connection-string CONNECTION_STRING
                        Connection string to the storage account
  -p PARALLEL_FACTOR, --parallel-factor PARALLEL_FACTOR
                        Parallel execution factor
  -f OUTPUT_FILE, --output-file OUTPUT_FILE
                        File path to dump the list of blobs
```

## Output
```
Output is a list (either dumped to file or printed on screen) in format 
<container name> : <blob name>

e.g. 
test-cnt-ubn-20 : testLargeFileDir/a6ab90df-858d-4e6a-94a5-4f43cbe19920
test-cnt-ubn-20 : testLargeFileDir/bdb322ab-4c09-45f2-a696-934a7bcbe9ba
testcnt : LICENSE
testcnt : NOTICES
testcnt : README.md
```

 