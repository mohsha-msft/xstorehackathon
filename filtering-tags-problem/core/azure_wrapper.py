import sys

import azure.core.exceptions as excpt
from azure.storage.blob import BlobServiceClient, BlobClient

from . import common_utils

StorageAccountConnectionString = ""
BlobServiceClientObj = None


def filter_blobs_by_tags(credentials, options):
    filtered_blobs = []
    blob_service_client = None
    if "connection_string" in credentials:
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=credentials["connection_string"])
    else:
        raise Exception("Not Implemented")

    try:
        blob_list_resp = blob_service_client.find_blobs_by_tags(
            filter_expression=common_utils.create_filter_expression(options)).by_page()
        while True:
            result_page = next(blob_list_resp)
            items_on_page = list(result_page)
            filtered_blobs.extend(items_on_page)
    except excpt.HttpResponseError as e:
        print(e.message)
        print("Hi")
    except StopIteration as err:
        pass
    except Exception as err:
        print(err)

    finally:
        blob_service_client.close()

    return filtered_blobs


def get_blob_tags(credentials, _container_name, _blob_name):
    blob_tags = {}
    try:
        blob_client = BlobClient.from_connection_string(conn_str=credentials["connection_string"],
                                                        container_name=_container_name,
                                                        blob_name=_blob_name)

        blob_tags = blob_client.get_blob_tags()

    except excpt.HttpResponseError as e:
        print(e.message)


    except Exception as err:
        print(err)

    return blob_tags


def set_blob_tags(credentials, _container_name, _blob_name, _tags):
    try:
        blob_client = BlobClient.from_connection_string(conn_str=credentials["connection_string"],
                                                        container_name=_container_name,
                                                        blob_name=_blob_name)

        _ = blob_client.set_blob_tags(tags=_tags)

    except excpt.HttpResponseError as e:
        print(e.message)

    except Exception as err:
        print(err)


def delete_blob(credentials, _container_name, _blob_name):
    try:
        blob_client = BlobClient.from_connection_string(conn_str=credentials["connection_string"],
                                                        container_name=_container_name,
                                                        blob_name=_blob_name)

        _ = blob_client.delete_blob()

    except excpt.HttpResponseError as e:
        print(e.message)

    except Exception as err:
        print(err)


def download_blob(credentials, _container_name, _blob_name, _file_path):
    try:
        blob_client = BlobClient.from_connection_string(conn_str=credentials["connection_string"],
                                                        container_name=_container_name,
                                                        blob_name=_blob_name)

        download_resp = blob_client.download_blob()
        content = download_resp.readall()
        blob_data = open(_file_path, 'wb').write(content)

    except excpt.HttpResponseError as e:
        print(e.message)

    except Exception as err:
        print(err)
