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
 
 Both upload and download are done in chunks of 4MB.
 ```
 
 ## Input
 ```
usage: main.py [-h] -u BLOB_SAS_URL -p PATH -o OPERATION

VHD Uploader/Download : Optimize page blob uploads/downloads

optional arguments:
  -h, --help            show this help message and exit
  -u BLOB_SAS_URL, --blob-sas-url BLOB_SAS_URL
                        Blob URL containing SAS
  -p PATH, --path PATH  Path to upload/download
  -o OPERATION, --operation OPERATION
                        Enum(Upload/Download)
```

 ## Output 
 
 ![Upload](https://github.com/mohsha-msft/xstorehackathon/blob/nakulkar/page-upload-download/output/upload.png?raw=true)
 
 ![Download](https://github.com/mohsha-msft/xstorehackathon/blob/nakulkar/page-upload-download/output/download.png?raw=true)



     