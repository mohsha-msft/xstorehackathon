# Hackathon for XStore

Welcome! We all have been busy at work trying to make the best experiences for our customers. But every feature travels through many hands before they reach the customer. And sometimes we never get to see the end product. This Hackathon is a chance to walk a mile in our customers shoes and celebrate the work we do.

``` Note: Everything in this repo is in the public domain. ```

## What do you need to get started

* A computer that can host an editor
* A storage account
* You hacking hat

## Things to watch out for

* Do not checkin your SAS token/SharedKey Credential or any other creds

## Recommended Languages (alphabetically)

* .Net
* Java
* JS
* Python

## Some ideas for things to try (don't hesitate in asking for samples)



| Project	|.Net  	| Java 	| JS 	| Python 	|
|---	|---	|---	|---	|---	|
|  List Million Blobs 	|   2	|   2	|  3 	|  3 	|
|  List Million Blobs in a non-alphabetic randomized order (extra credits for bigger randomizations) 	|   3	|   3	|   3	|   3	|
|   Azure Function that does LCM at large scale	|   3	|   3	|  3 	|   3	|
|   Setup AAD and use it to transfer data from one account to another	|   3	|   3	|   3	|   3	|
|   Download PageBlob ignoring pages that are empty	|   4	|   4	|   4	|   4	|
|   Copy a VHD from one account to another	|   3	|   3	|   3	|   3	|
|   Using Batch API delete all the data in your account with error handling	|   2	|   2	|   2	|   2	|
|   Compare the performance across DFS endpoint and Blob endpoint for same file	|   2	|   2	|   2	|   2	|
|   Create a azcopy wrapper to start transfers and listen to job status	|   2	|   3	|   3	|   4	|
|   Use BlobFuse on WSL2.0 and file bugs (4 points)	|   	|   	|   	|   	|
|   Create a tool that will help users manage blob versioning (keep/delete/add versions)	|   2	|   3	|   3	|   3	|
|   Tool/API to copy between blobs and files service (extra credits for preserving metadata/smb info)	|   3	|   3	|   3	|   3	|
|   	|   	|   	|   	|   	|

## Rules

* Fork this repo and develop at your comfort
* Submit PR to the main branch of this repo
* PR deadline 12/17
* We will provide PR feedback and assign points. Max points listed in table
* Winner is the person with maximum point 
* One random winner too

## SDK location

| Service	|Blobs  	| Files 	| Queues 	| ADLS Gen2 	|
|---	|---	|---	|---	|---	|
| .Net  	|   [Link](https://www.nuget.org/packages/Azure.Storage.Blobs/12.8.0-beta.1)	|   [Link](https://www.nuget.org/packages/Azure.Storage.Files.Shares/12.6.0-beta.1)	|   [Link](https://www.nuget.org/packages/Azure.Storage.Queues/12.6.0-beta.1)	|   [Link](https://www.nuget.org/packages/Azure.Storage.Files.DataLake/12.6.0-beta.1)	|
|  Java 	|  [Link](https://search.maven.org/artifact/com.azure/azure-storage-blob/12.10.0-beta.1/jar) 	|   [Link](https://search.maven.org/artifact/com.azure/azure-storage-file-share/12.8.0-beta.1/jar)	|  [Link](https://search.maven.org/artifact/com.azure/azure-storage-queue/12.8.0-beta.1/jar) 	|   [Link](https://search.maven.org/artifact/com.azure/azure-storage-file-datalake/12.4.0-beta.1/jar)	|
|  JS 	|   [Link](https://www.npmjs.com/package/@azure/storage-blob)	|   [Link](https://www.npmjs.com/package/@azure/storage-file-share)	|   [Link](https://www.npmjs.com/package/@azure/storage-queue/v/12.2.0)	|   [Link](https://www.npmjs.com/package/@azure/storage-file-datalake)	|
|  Python 	|   [Link](https://pypi.org/project/azure-storage-blob/12.7.0b1/)	|   [Link](https://pypi.org/project/azure-storage-file-share/12.4.0b1/)	|   [Link](https://pypi.org/project/azure-storage-queue/12.1.4/)	|   [Link](https://pypi.org/project/azure-storage-file-datalake/12.2.0/)	|