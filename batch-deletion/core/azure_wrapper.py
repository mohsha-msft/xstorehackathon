import azure.core.exceptions as excpt
from azure.storage.blob import BlobServiceClient

storage_account_connection_string = ""
blob_service_client_obj = None


# Method to set the connection string
def set_connection_string(con_str):
    global storage_account_connection_string
    global blob_service_client_obj

    storage_account_connection_string = con_str

    blob_service_client_obj = BlobServiceClient.from_connection_string(storage_account_connection_string)


# List the containers in account
def list_storage_containers():
    storage_container_list = []

    try:
        blob_containers = blob_service_client_obj.list_containers()

        for blob_container in blob_containers:
            # print(blob_container.name)
            storage_container_list.append(blob_container.name)

    except excpt.HttpResponseError as err:
        print(err)
    except excpt.AzureError as err:
        print(err)
    except Exception as err:
        print(err)

    return storage_container_list


# List blobs from a given path
def list_storage_blobs(container, listpath):
    blob_list = []
    blob_container_client = blob_service_client_obj.get_container_client(container=container)
    try:
        blob_list_resp = blob_container_client.walk_blobs(name_starts_with=listpath).by_page()

        while True:
            result_page = next(blob_list_resp)
            items_on_page = list(result_page)
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

    except excpt.HttpResponseError as err:
        print(err)
    except excpt.AzureError as err:
        print(err)
    except Exception as err:
        print(err)

    return blob_info


def delete_blob_batch(_container_name, _blob_path_list):
    blob_container_client = blob_service_client_obj.get_container_client(container=_container_name)
    try:
        blob_list_resp = blob_container_client.delete_blobs(*_blob_path_list)

    except excpt.HttpResponseError as err:
        print(err)
    except excpt.AzureError as err:
        print(err)
    except StopIteration as err:
        pass
    except Exception as err:
        print(err)

    finally:
        blob_container_client.close()
