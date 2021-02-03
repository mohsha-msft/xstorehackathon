
from azure.storage.blob import BlobServiceClient
from azure.storage.fileshare import ShareServiceClient

StorageAccountConnectionString = ""
BlobServiceClientObj = None

# Method to set the connection string 
def SetConnectionString(con_str):
    global StorageAccountConnectionString
    global BlobServiceClientObj

    StorageAccountConnectionString = con_str

    BlobServiceClientObj = BlobServiceClient.from_connection_string(StorageAccountConnectionString)


# List the containers in account
def ListStorageContainers():
    StorageContainerList = []
    
    blob_containers = BlobServiceClientObj.list_containers()

    for blob_container in blob_containers:
        #print(blob_container.name)
        StorageContainerList.append(blob_container.name)

    return StorageContainerList


# List blobs from a given path
def ListStorageBlobs(container, listpath):
    BlobList = []
    try:
        include_attr = ['metadata', 'uncommittedblobs', 'copy', 'deleted']

        blob_container_client = BlobServiceClientObj.get_container_client(container=container)
        #BlobList = blob_container_client.list_blobs(name_starts_with=listpath, include=include_attr)
        BlobList = blob_container_client.walk_blobs(name_starts_with=listpath, include=include_attr)

        #print("Returning blobs : " + str(len(BlobList)))
        #for item in BlobList:
        #    print(item)
        #    print("-----------------------------------------------------------------------")
        
    finally:
        blob_container_client.close()

    return BlobList


def ListFileShares():
    FileShareStats = {}
    try:
        file_share_service_client = ShareServiceClient.from_connection_string(conn_str=StorageAccountConnectionString)
        
        file_shares = file_share_service_client.list_shares(include_metadata=True, include_snapshots=True)

        for share_obj in file_shares:
            share_client = file_share_service_client.get_share_client(share_obj.name)
            share_stats = share_client.get_share_stats()
            share_client.close()

            FileShareStats[share_obj.name] = share_stats 

    finally:
        file_share_service_client.close()

    return FileShareStats


# Convert blob data retreived from stroage to a dictionary holding important values
def GetBlobInfo(blob):
    #print(blob)
    #print("------- >>>>>>>>  ------------------------------------------------------------------------------------------------------")
    BlobInfo = {}
    BlobInfo["name"] = blob.name

    BlobInfo["dir"] = False
    BlobInfo["symlink"] = False
    
    if blob.name[-1] == "/":
        BlobInfo["dir"] = True
        BlobInfo["type"] = "Block"
    else:
        if (blob.metadata and blob.has_key("hdi_isfolder")):
            BlobInfo["dir"] = True
        
        if blob.metadata and blob.has_key("is_symlink"):
            BlobInfo["symlink"] = True

        BlobInfo["size"] = blob.size
        BlobInfo["tier"] = blob.blob_tier
        BlobInfo["type"] = blob.blob_type   

    return BlobInfo



if __name__ == '__main__':
    print("Shouldn't come here !!!")
