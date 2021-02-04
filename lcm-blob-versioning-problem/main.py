import sys
from core import azure_wrapper


def main(argv):
    azure_wrapper.set_credentials(argv[0])
    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas2935502929500",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas2938769234400")
    # azure_wrapper.delete_blob_version("godeletespecificblobversionwithblobsas425511080800",
    #                                   "gotestblobdeletespecificblobversionwithblobsas4256178906400",
    #                                   blob_version[0]["version_id"])
    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas425511080800",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas4256178906400")

    # options = {
    #     "file_path": "./README.md",
    #     "blob_type": "BlockBlob",
    # }
    # azure_wrapper.add_blob_version("godeletespecificblobversionwithblobsas425511080800",
    #                                "gotestblobdeletespecificblobversionwithblobsas4256178906400",
    #                                options)
    #
    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas425511080800",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas4256178906400")

    # options = {
    #     "file_path": "./README1.md",
    #     "version_id": blob_version[4]["version_id"],
    # }
    # azure_wrapper.download_blob_version("godeletespecificblobversionwithblobsas425511080800",
    #                                "gotestblobdeletespecificblobversionwithblobsas4256178906400",
    #                                options)

    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas425511080800",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas4256178906400")

    # options = {
    #     'delete_before': blob_version[1]['last_modified'],
    # }
    #
    # delete_cond_resp = azure_wrapper.delete_blob_with_condition("godeletespecificblobversionwithblobsas224244571900",
    #                                                             "gotestblobdeletespecificblobversionwithblobsas225557027000",
    #                                                             options)
    #
    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas224244571900",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas225557027000")

    # options = {
    #     'delete_between': [blob_version[0]['last_modified'], blob_version[1]['last_modified']],
    # }
    #
    # delete_cond_resp = azure_wrapper.delete_blob_with_condition("godeletespecificblobversionwithblobsas224244571900",
    #                                                             "gotestblobdeletespecificblobversionwithblobsas225557027000",
    #                                                             options)
    #
    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas224244571900",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas225557027000")

    # options = {
    #     'blob_type': "BlockBlob",
    #     'tier': "Cool",
    #     'version_id': blob_version[1]["version_id"]
    # }
    #
    # azure_wrapper.blob_version_set_tier("godeletespecificblobversionwithblobsas2935502929500", "gotestblobdeletespecificblobversionwithblobsas2938769234400", options)
    #
    # blob_version = azure_wrapper.list_blob_versions("godeletespecificblobversionwithblobsas2935502929500",
    #                                                 "gotestblobdeletespecificblobversionwithblobsas2938769234400")


if __name__ == "__main__":
    main(sys.argv[1:])
