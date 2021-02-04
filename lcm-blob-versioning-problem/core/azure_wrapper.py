from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    generate_account_sas,
    AccountSasPermissions,
    ResourceTypes
)
import datetime as dt

storage_account = ""
storage_account_key = ""
blob_service_client = None
service_sas_token = ""
connection_string = ""


def account_url():
    return "https://" + storage_account + ".blob.core.windows.net/"


# Method to extract important info from connection string
def set_credentials(_connection_string):
    protocol, account_name, account_key, endpoint = _connection_string.split(";")
    global storage_account
    global storage_account_key
    global blob_service_client
    global service_sas_token
    global connection_string

    storage_account = account_name
    storage_account_key = account_key
    blob_service_client = BlobServiceClient(account_url(), storage_account_key)
    service_sas_token = generate_account_sas(
        account_name=storage_account,
        account_key=storage_account_key,
        resource_types=ResourceTypes(service=True, container=True, object=True),
        permission=AccountSasPermissions(read=True, list=True),
        start=dt.datetime.now() - dt.timedelta(hours=24),
        expiry=dt.datetime.now() - dt.timedelta(days=8)
    )
    connection_string = _connection_string


# List all available version of a given blob
def list_blob_versions(_container_name, relative_blob_path):
    container_client = ContainerClient.from_connection_string(
        container_name=_container_name,
        conn_str=connection_string
    )
    blob_versions = []
    try:
        include_attr = ['versions', 'metadata']

        list_resp = container_client.list_blobs(name_starts_with=relative_blob_path, include=include_attr)
        for resp in list_resp:
            blob_version = {
                "version_id": resp['version_id'],
                "is_current_version": resp['is_current_version'],
                "size": resp['size'],
                "last_modified": resp["last_modified"],
                "blob_tier": resp["blob_tier"],
            }
            blob_versions.append(blob_version)
            #print(blob_version)

    finally:
        #print("=====================Listing Successful =======================================")
        container_client.close()

    return blob_versions


# Delete a specific version of a given bloob
def delete_blob_version(_container_name, _relative_blob_path, _version_id):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    try:
        delete_resp = blob_client.delete_blob(version_id=_version_id)
        #print(delete_resp)

    finally:
        #print("=====================Delete Successful =======================================")
        blob_client.close()

    return delete_resp


# Create a new version of given blob by uploading the file to that blob
def add_blob_version(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    try:
        blob_data = open(options["file_path"], 'rb').read()
        upload_resp = blob_client.upload_blob(data=blob_data, blob_type=options["blob_type"], overwrite=True)
        #print(upload_resp)

    finally:
        #print("=====================New version Added Successful =======================================")
        blob_client.close()
        # blob_data.close()

    return upload_resp


# Get specific version of a blob and save contents to given file
def download_blob_version(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    try:
        download_resp = blob_client.download_blob(version_id=options["version_id"])
        content = download_resp.readall()
        blob_data = open(options["file_path"], 'wb').write(content)

    finally:
        #print("=====================Download Successful =======================================")
        blob_client.close()

    return download_resp.size


# Delete all version of blob matching given dates
def delete_blob_with_condition(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    try:
        delete_total_resp = []
        blob_versions = list_blob_versions(_container_name, _relative_blob_path)

        if 'delete_before' in options:
            for blob_version in blob_versions:
                if blob_version['last_modified'] <= options['delete_before']:
                    delete_resp = blob_client.delete_blob(version_id=blob_version["version_id"])
                    delete_total_resp.append(delete_resp)
        if 'delete_after' in options:
            for blob_version in blob_versions:
                if blob_version['last_modified'] >= options['delete_after']:
                    delete_resp = blob_client.delete_blob(version_id=blob_version["version_id"])
                    delete_total_resp.append(delete_resp)
        if 'delete_between' in options:
            for blob_version in blob_versions:
                if options['delete_between'][0] <= blob_version['last_modified'] <= options['delete_between'][1]:
                    delete_resp = blob_client.delete_blob(version_id=blob_version["version_id"])
                    delete_total_resp.append(delete_resp)


    finally:
        #print("=====================Delete Successful =======================================")
        blob_client.close()

    return delete_total_resp


# Set tier of given version of a blob
def blob_version_set_tier(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    try:
        set_tier_resp = None
        if options["blob_type"] == "BlockBlob":
            set_tier_resp = blob_client.set_standard_blob_tier(standard_blob_tier=options["tier"], version_id=options["version_id"])
        elif options["blob_type"] == "PageBlob":
            set_tier_resp = blob_client.set_premium_page_blob_tier(premium_page_blob_tier=options["tier"],
                                                               version_id=options["version_id"])

    finally:
        print("===================== Set Tier Successful =======================================")
        blob_client.close()

    return set_tier_resp

