import argparse
import os
from core import azure_wrapper, scheduler


def parse_operation():
    if cli_options["list_blobs"]:
        return "list_blobs"
    if cli_options["delete_blobs"]:
        return "delete_blobs"
    elif cli_options["download_blobs"]:
        return "download_blobs"
    elif cli_options["add_tag"]:
        return "add_tag"
    elif cli_options["update_tag"]:
        return "update_tag"
    elif cli_options["delete_tag"]:
        return "delete_tag"
    else:
        raise Exception('Invalid option chosen')


def main():
    credentials = {}
    if cli_options["connection_string"]:
        credentials["connection_string"] = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        # credentials["connection_string"] = cli_options["connection_string"]
    elif cli_options["sas_url"]:
        credentials["sas_url"] = cli_options["sas_url"]

    options = {
        "container_name": cli_options["container"],
        "name_starts_with": cli_options["name_starts_with"],
        "tag_key": cli_options["tag_key"],
        "tag_value": cli_options["tag_value"],
        "concurrency": cli_options["concurrency_factor"],
        "operation": parse_operation(),
        "condition_file_path": cli_options["condition_file_path"],
        "path": cli_options["path"],
    }

    filtered_blobs = azure_wrapper.filter_blobs_by_tags(credentials, options)
    # print(str(len(filtered_blobs)) + " blobs match the condition")
    if cli_options["list_blobs"]:
        for filtered_blob in filtered_blobs:
            print(filtered_blob)
    else:
        scheduler.schedule_job(filtered_blobs, credentials, options)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Blob Tagger : Blob tags Lifecycle Manager")

    # Add the basic arguments to parser
    ex_group = arg_parser.add_mutually_exclusive_group()
    ex_group.add_argument("-lcs", "--connection-string", help="Connection String for storage account")
    ex_group.add_argument("-lsu", "--sas-url", help="Service SAS URL for blob storage account")

    arg_parser.add_argument("-z", "--concurrency-factor",
                            help="Concurrency factor for parallelism. By default threading is disabled", default=1)

    arg_parser.add_argument("-c", "--container", help="Specify the name of the containers to be search")
    arg_parser.add_argument("-n", "--name-starts-with", help="Blobs whose name start with given value")
    arg_parser.add_argument("-p", "--condition-file-path", help="Path of the file containing tag filters")

    op_group = arg_parser.add_mutually_exclusive_group()
    op_group.add_argument("-l", "--list-blobs", help="List all the filtered blobs", action="store_true")
    op_group.add_argument("-x", "--delete-blobs", help="Delete the filtered blobs", action="store_true")
    op_group.add_argument("-g", "--download-blobs",
                          help="Download the filtered blobs. Provide the destination direction using  --path",
                          action="store_true")
    op_group.add_argument("-a", "--add-tag", help="Add tag to the filtered blobs", action="store_true")
    op_group.add_argument("-u", "--update-tag", help="Update tag in the filtered blobs", action="store_true")
    op_group.add_argument("-d", "--delete-tag", help="Delete tag from the filtered blobs", action="store_true")

    arg_parser.add_argument("-tk", "--tag-key", help="Key of the tag")
    arg_parser.add_argument("-tv", "--tag-value", help="Value of the tag")
    arg_parser.add_argument("-s", "--path", help="Destination directory to download filtered blobs")

    cli_options = vars(arg_parser.parse_args())
    main()
