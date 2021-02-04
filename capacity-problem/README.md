# Storage Account Capacity Calculator

## Team - DevEx IDC
 - Vikas (Vikas.Bhansali@microsoft.com)
 - Narasimha (Narasimha.Kulkarni@microsoft.com)
 - Mohit (mohsha@microsoft.com)
 
 ## Input
 ```
python main.py <connection string> <parallelism factor>
     <connection string>  : MANDATORY : Connection string for the storage account 
     <parallelism factor> : OPTIONAL  : Default to 8
```

 ## Output 
 
 ![Result](https://github.com/mohsha-msft/xstorehackathon/blob/devex-idc/capacity-problem/capacity-problem/output.png?raw=true)


 ## How does it work 
    * Using connection string (provided as input), a list of containers is obtained from storage account

    * Root directory for each container is pushed into worker queue

    * Based on parallelism factor (default 8) number of worker threads are started

    * Each thread takes the next request in worker queue and tries to iterate one level of directories and blobs on that path

    * On encountering a new directory in the path, another item is pushed to the worker queue for further iteration

    * Post iterating each level a summary of that level is created and pushed in output queue

    * A consolidator thread picks up these summary items and creates a consolidated report, which is printed at the end

    * Tool iterates through container and then following all directories in each container. It will also look up at all the file-shares that exists in the account.

 