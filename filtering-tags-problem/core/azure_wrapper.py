from azure.storage.blob import BlobServiceClient
from azure.storage.fileshare import ShareServiceClient
import azure.core.exceptions as excpt
import sys
from . import common_utils

StorageAccountConnectionString = ""
BlobServiceClientObj = None


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

    except:
        e = sys.exc_info()[0]
        print(e)

    return storage_container_list


# List blobs from a given path
# def list_tags_in_container(_credentails, _container_name, _options):
#     blob_list = []
#     try:
#         BlobServiceClient.from_connection_string()
#
#     except excpt.HttpResponseError as e:
#         print(e.message)
#
#     except:
#         e = sys.exc_info()[0]
#         print(e)
#
#     finally:
#         blob_container_client.close()
#
#     return blob_list


# Convert blob data retrieved from stroage to a dictionary holding important values
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

    except:
        e = sys.exc_info()[0]
        print(e)

    return blob_info


def filter_blobs_by_tags(credentials, options):
    filtered_blobs = []
    blob_service_client = None
    if "connection_string" in credentials:
        blob_service_client = BlobServiceClient.from_connection_string()
    else:
        raise Exception("Not Implemented")

    try:
        filtered_blobs = blob_service_client.find_blobs_by_tags(
            filter_expression=common_utils.create_filter_expression(options))
    except excpt.HttpResponseError as e:
        print(e.message)

    except:
        e = sys.exc_info()[0]
        print(e)

    finally:
        blob_service_client.close()

    return filtered_blobs
