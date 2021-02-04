import datetime as dt
import random
import string
import time
import sys
import azure.core.exceptions as excpt

from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    generate_account_sas,
    AccountSasPermissions,
    ResourceTypes
)

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


def generate_blob_with_versions(_container_name, _relative_blob_path, _number_of_versions, _blob_type):
    blob_version = []
    for i in range(0, _number_of_versions):
        try:
            time.sleep(2)
            content = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(100, 10000))).encode()
            file_path = "./sample_files/generate_random_blob_" + str(i + 1) + ".txt"
            _ = open(file_path, 'wb').write(content)
            options = {
                "file_path": file_path,
                "blob_type": "BlockBlob",
            }
            upload_resp = add_blob_version(_container_name, _relative_blob_path, options)
            print(upload_resp)
        finally:
            print("=====================Generated Versions Successfully =======================================")


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
            # print(blob_version)
    except excpt.HttpResponseError as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)
    finally:
        container_client.close()

    return blob_versions


# Delete a specific version of a given bloob
def delete_blob_version(_container_name, _relative_blob_path, _version_id):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    return_code = -1
    try:
        delete_resp = blob_client.delete_blob(version_id=_version_id)
        return_code = 0
    except excpt.HttpResponseError as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)

    finally:
        # print("=====================Delete Successful =======================================")
        blob_client.close()

    return return_code


# Create a new version of given blob by uploading the file to that blob
def add_blob_version(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    return_code = -1
    try:
        blob_data = open(options["file_path"], 'rb').read()
        upload_resp = blob_client.upload_blob(data=blob_data, blob_type=options["blob_type"], overwrite=True)
        return_code = 0
    except excpt.HttpResponseError as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)
    finally:
        # print("=====================New version Added Successful =======================================")
        blob_client.close()

    return return_code


# Get specific version of a blob and save contents to given file
def download_blob_version(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )
    download_resp = None
    try:
        download_resp = blob_client.download_blob(version_id=options["version_id"])
        content = download_resp.readall()
        blob_data = open(options["file_path"], 'wb').write(content)
        print("Version downloaded successfully to give file. Size : " + str(download_resp.size))
    except excpt.HttpResponseError as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)

    finally:
        # print("=====================Download Successful =======================================")
        blob_client.close()
    if download_resp is None:
        return -1
    return download_resp.size


# Delete all version of blob matching given dates
def delete_blob_with_condition(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    delete_total_resp = []
    try:
        blob_versions = list_blob_versions(_container_name, _relative_blob_path)

        if 'delete_before' in options:
            for blob_version in blob_versions:
                if blob_version['last_modified'] <= options['delete_before'] and blob_version[
                    'is_current_version'] is None:
                    delete_resp = blob_client.delete_blob(version_id=blob_version["version_id"])
                    delete_total_resp.append(blob_version)
        if 'delete_after' in options:
            for blob_version in blob_versions:
                if blob_version['last_modified'] >= options['delete_after'] and blob_version[
                    'is_current_version'] is None:
                    delete_resp = blob_client.delete_blob(version_id=blob_version["version_id"])
                    delete_total_resp.append(blob_version)
        if 'delete_between' in options:
            for blob_version in blob_versions:
                if (options['delete_between'][0] <= blob_version['last_modified'] <= options['delete_between'][1]) \
                        and blob_version['is_current_version'] is None:
                    delete_resp = blob_client.delete_blob(version_id=blob_version["version_id"])
                    delete_total_resp.append(blob_version)

    except excpt.HttpResponseError as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)
    finally:
        blob_client.close()

    return delete_total_resp


# Set tier of given version of a blob
def blob_version_set_tier(_container_name, _relative_blob_path, options):
    blob_client = BlobClient.from_connection_string(
        container_name=_container_name,
        blob_name=_relative_blob_path,
        conn_str=connection_string,
    )

    set_tier_resp = None
    return_code = -1
    try:

        if options["blob_type"] == "BlockBlob":
            set_tier_resp = blob_client.set_standard_blob_tier(standard_blob_tier=options["tier"],
                                                               version_id=options["version_id"])
        elif options["blob_type"] == "PageBlob":
            set_tier_resp = blob_client.set_premium_page_blob_tier(premium_page_blob_tier=options["tier"],
                                                                   version_id=options["version_id"])

        return_code = 0
    except excpt.HttpResponseError as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)

    finally:
        blob_client.close()

    return return_code
