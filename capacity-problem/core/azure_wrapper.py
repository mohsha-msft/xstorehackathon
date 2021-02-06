import azure.core.exceptions as excpt
from azure.storage.blob import BlobServiceClient
from azure.storage.fileshare import ShareServiceClient

StorageAccountConnectionString = ""
BlobServiceClientObj = None


# Method to set the connection string
def set_connection_string(con_str):
    global StorageAccountConnectionString
    global BlobServiceClientObj

    StorageAccountConnectionString = con_str

    BlobServiceClientObj = BlobServiceClient.from_connection_string(StorageAccountConnectionString)


# List the containers in account
def list_storage_containers():
    storage_container_list = []

    try:
        blob_containers = BlobServiceClientObj.list_containers()

        for blob_container in blob_containers:
            # print(blob_container.name)
            storage_container_list.append(blob_container.name)

    except excpt.HttpResponseError as e:
        print(e.message)
    except excpt.AzureError as e:
        print(e)
    except Exception as e:
        print(e)

    return storage_container_list


# List blobs from a given path
def list_storage_blobs(container, listpath):
    blob_list = []

    try:
        include_attr = ['metadata', 'uncommittedblobs', 'copy', 'deleted']
        blob_container_client = BlobServiceClientObj.get_container_client(container=container)
        blob_list_resp = blob_container_client.walk_blobs(name_starts_with=listpath, include=include_attr).by_page()

        while True:
            result_page = next(blob_list_resp)
            items_on_page = list(result_page)
            if len(items_on_page) > 0:
                blob_list.extend(items_on_page)

    except excpt.HttpResponseError as e:
        print(e.message)
    except excpt.AzureError as err:
        print(err)
    except StopIteration as err:
        pass
    except Exception as err:
        print(err)
    finally:
        blob_container_client.close()

    return blob_list


def list_file_shares():
    file_share_stats = {}
    file_share_service_client = ShareServiceClient.from_connection_string(conn_str=StorageAccountConnectionString)
    try:
        file_shares = file_share_service_client.list_shares(include_metadata=True, include_snapshots=True)

        for share_obj in file_shares:
            share_client = file_share_service_client.get_share_client(share_obj.name)
            share_stats = share_client.get_share_stats()
            share_client.close()

            file_share_stats[share_obj.name] = share_stats

    except excpt.HttpResponseError as e:
        print(e)
    except excpt.AzureError as e:
        print(e)
    except Exception as e:
        print(e)

    finally:
        file_share_service_client.close()

    return file_share_stats


# Convert blob data retrieved from storage to a dictionary holding important values
def get_blob_info(blob):
    blob_info = {"name": blob.name, "dir": False, "symlink": False}

    try:
        if blob.name[-1] == "/":
            blob_info["dir"] = True
            blob_info["type"] = "Block"
        else:
            if blob.metadata and blob.has_key("hdi_isfolder"):
                blob_info["dir"] = True

            if blob.metadata and blob.has_key("is_symlink"):
                blob_info["symlink"] = True

            blob_info["size"] = blob.size
            blob_info["tier"] = blob.blob_tier
            blob_info["type"] = blob.blob_type

    except Exception as e:
        print(e)

    return blob_info
