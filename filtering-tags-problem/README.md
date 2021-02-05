# Filtering Tags

## Team - DevEx IDC
 - Vikas (Vikas.Bhansali@microsoft.com)
 - Narasimha (Narasimha.Kulkarni@microsoft.com)
 - Mohit (mohsha@microsoft.com)
 
 ## About the tool
  - This tool provides life cycle management of blob tags
  - Below are the feature available in the tool
      - List all the blobs matching given filter criteria
      - Delete all blobs matching filter criteria
      - Update any existing tag in all blobs matching filter criteria
      - Delete specific tag from all the filtered blobs
      - Remove existing tags and add a new tag to all filtered blobs
      - Download all filtered blobs to given directory
  

 ## Input
 ```
usage: main.py [-h] [-lcs CONNECTION_STRING | -lsu SAS_URL]
               [-z CONCURRENCY_FACTOR] [-c CONTAINER] [-n NAME_STARTS_WITH]
               [-p CONDITION_FILE_PATH] [-l | -x | -g | -a | -u | -d]
               [-tk TAG_KEY] [-tv TAG_VALUE] [-s PATH]

Blob Tagger : Blob tags Lifecycle Manager

optional arguments:
  -h, --help            show this help message and exit
  -lcs CONNECTION_STRING, --connection-string CONNECTION_STRING
                        Connection String for storage account
  -lsu SAS_URL, --sas-url SAS_URL
                        Service SAS URL for blob storage account
  -z CONCURRENCY_FACTOR, --concurrency-factor CONCURRENCY_FACTOR
                        Concurrency factor for parallelism. By default
                        threading is disabled
  -c CONTAINER, --container CONTAINER
                        Specify the name of the containers to be search
  -n NAME_STARTS_WITH, --name-starts-with NAME_STARTS_WITH
                        Blobs whose name start with given value
  -p CONDITION_FILE_PATH, --condition-file-path CONDITION_FILE_PATH
                        Path of the file containing tag filters
  -l, --list-blobs      List all the filtered blobs
  -x, --delete-blobs    Delete the filtered blobs
  -g, --download-blobs  Download the filtered blobs. Provide the destination
                        direction using --path
  -a, --add-tag         Add tag to the filtered blobs
  -u, --update-tag      Update tag in the filtered blobs
  -d, --delete-tag      Delete tag from the filtered blobs
  -tk TAG_KEY, --tag-key TAG_KEY
                        Key of the tag
  -tv TAG_VALUE, --tag-value TAG_VALUE
                        Value of the tag
  -s PATH, --path PATH  Destination directory to download filtered blobs

```

### Condition file should contain filter in one line. Keys should be in double quotes and values in single quote.
`"a1+"='b-2'`

 ## Output 
 - Output of blob list
```
Connected to pydev debugger (build 202.8194.22)
{'name': 'bc.dat', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'beta.py', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'cd.exe', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'delta.pdf', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'epsilon.mp3', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'gamma.go', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'mohit.cpp', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/ab.gzip', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/alpha.java', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/bc.dat', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/beta.py', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/cd.exe', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/delta.pdf', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/epsilon.mp3', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/gamma.go', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/mohit', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/mohit.cpp', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/rohit', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/test1/mohit', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
{'name': 'test1/test1/rohit', 'container_name': 'testcontainer', 'tags': {'a1+': 'b-2'}}
```