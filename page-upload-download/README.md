# Optimized Uploader/Downloader For Page Blob

## Team - DevEx IDC
 - Vikas (Vikas.Bhansali@microsoft.com)
 - Narasimha (Narasimha.Kulkarni@microsoft.com)
 - Mohit (mohsha@microsoft.com)
 

 ## About the tool 
 
 ```
 Tool provides two operations on page blobs

 1. Upload 
    - Create page blob of required size.
    - Read the local VHD file.
    - Upload only those ranges which have data.
 2. Download 
    - Make get_page_range call to get list of valid and empty ranges.
    - Before downloading, verify that the range overlaps with one of the valid page.
    - If the range is empty, write a string of 0 to the local file.
 3. Copy
    - Make get_page_range call to get a list of valid and empty ranges.
    - For each range in valid ranges, copy page to destination usign copy_page_from_url, with a block size of 4M
 
 Both upload and download are done in chunks of 4MB.
 ```
 
 ## Input
 ```
usage: main.py [-h] -o OPERATION -s SOURCE -d DESTINATION

VHD Uploader/Download : Optimize page blob uploads/downloads

optional arguments:
  -h, --help            show this help message and exit
  -o OPERATION, --operation OPERATION
                        Enum(upload/download/copy)
  -s SOURCE, --source SOURCE
                        Source Blob URL with SAS or local VHD
  -d DESTINATION, --destination DESTINATION
                        Destination Blob URL with SAS or local path to download

```

 ## Output 
 
 ![Upload](https://github.com/mohsha-msft/xstorehackathon/blob/nakulkar/page-upload-download/output/upload.png?raw=true)
 
 ![Download](https://github.com/mohsha-msft/xstorehackathon/blob/nakulkar/page-upload-download/output/download.png?raw=true)

 ![Copy](https://github.com/mohsha-msft/xstorehackathon/blob/nakulkar/page-upload-download/output/copy.png?raw=true)



     