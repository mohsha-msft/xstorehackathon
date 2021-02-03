# set up
import os
import wrapper
import core.another_wrapper as caw

from azure.storage.blob import BlobServiceClient
# from azure.storage.filedatalake import DataLakeServiceClient
# from azure.storage.filedatalake import FileSystemClient
from azure.storage.fileshare import ShareServiceClient

azure_storage_account_name = ""
azure_storage_account_key = ""
connection_string = ""
storage_account_attributes = {
    "FILE_SHARE_STATS": {},
    "BLOB_STATS": {},
    "GEN2_STATS": {},
}


def get_credentials():
    return "", "", os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    # return os.getenv("ACCOUNT_NAME"), os.getenv("ACCOUNT_KEY"), os.getenv("AZURE_STORAGE_CONNECTION_STRING")


def compute_file_storage_size():
    file_storage_stats, size, count = {}, 0, 0
    try:

        file_share_service_client = ShareServiceClient.from_connection_string(conn_str=connection_string)
        file_shares = file_share_service_client.list_shares(include_metadata=True, include_snapshots=True)
        for share_obj in file_shares:
            share_client = file_share_service_client.get_share_client(share_obj.name)
            share_stats = share_client.get_share_stats()
            file_storage_stats[share_obj.name] = share_stats
            size += share_stats
            count += 1
            # print(share_stats)

    finally:
        storage_account_attributes["FILE_SHARE_STATS"] = {
            "TOTAL_USAGE": size,
            "TOTAL_FILE_SHARES": count,
            "FILE_SHARE_LEVEL_STATS": file_storage_stats
        }


def compute_blob_storage_size():
    blob_storage_stats, size, count = {}, 0, 0
    try:
        # include_attr = ['snapshots', 'metadata', 'uncommittedblobs', 'copy', 'deleted']
        include_attr = ['snapshots', 'metadata', 'copy']
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_containers = blob_service_client.list_containers()
        for blob_container in blob_containers:
            blob_container_client = blob_service_client.get_container_client(container=blob_container.name)
            blob_list = blob_container_client.list_blobs(include=include_attr)
            container_size = 0
            for blob in blob_list:
                container_size += blob.size
            count += 1
            blob_storage_stats[blob_container.name] = container_size
            size += container_size
            # print(blob_container.name + " " + str(container_size) + "\n")

    finally:

        storage_account_attributes["BLOB_STATS"] = {
            "TOTAL_USAGE": size,
            "TOTAL_CONTAINERS": count,
            "CONTAINER_LEVEL_STATS": blob_storage_stats
        }


def compute_gen2_storage_size():
    gen2_storage_stats, size, count = {}, 0, 0
    # TODO


if __name__ == '__main__':
    # azure_storage_account_name, azure_storage_account_key, connection_string = get_credentials()
    # compute_file_storage_size()
    # compute_blob_storage_size()
    # print(storage_account_attributes["FILE_SHARE_STATS"])
    # print(storage_account_attributes["BLOB_STATS"])
    # total_size = storage_account_attributes["FILE_SHARE_STATS"]["TOTAL_USAGE"] + \
    #              storage_account_attributes["BLOB_STATS"]["TOTAL_USAGE"]
    # print("Total Size in Bytes " + str(total_size))
    wrapper.print_hello()
    caw.print_hello()
