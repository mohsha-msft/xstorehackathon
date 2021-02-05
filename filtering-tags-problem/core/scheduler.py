from . import azure_wrapper


def schedule_job(blob_list, credentials, options):
    if options["operation"] == "delete_blobs":
        return delete_blobs(blob_list, credentials, options)
    elif options["operation"] == "download_blobs":
        return download_blobs(blob_list, credentials, options)
    elif options["operation"] == "add_tag":
        return add_tag(blob_list, credentials, options)
    elif options["operation"] == "update_tag":
        return update_tags(blob_list, credentials, options)
    elif options["operation"] == "delete_tag":
        return delete_tag(blob_list, credentials, options)
    else:
        raise Exception('Invalid option chosen')


def update_tags(blob_list, credentials, options):
    if ("tag_key" not in options) or ("tag_value" not in options):
        raise Exception("Invalid Option")

    for blob in blob_list:
        tags = azure_wrapper.get_blob_tags(credentials, options["container_name"], blob["name"])
        print(tags)

        tags[options["tag_key"]] = options['tag_value']
        azure_wrapper.set_blob_tags(credentials, options["container_name"], blob["name"], tags)

        new_tags = azure_wrapper.get_blob_tags(credentials, options["container_name"], blob["name"])
        print(new_tags)


def add_tag(blob_list, credentials, options):
    if ("tag_key" not in options) or ("tag_value" not in options):
        raise Exception("Invalid Option")

    for blob in blob_list:
        tags = {options["tag_key"]: options['tag_value']}
        azure_wrapper.set_blob_tags(credentials, options["container_name"], blob["name"], tags)

        new_tags = azure_wrapper.get_blob_tags(credentials, options["container_name"], blob["name"])
        print(new_tags)


def delete_tag(blob_list, credentials, options):
    if "tag_key" not in options:
        raise Exception("Invalid Option")

    for blob in blob_list:
        tags = azure_wrapper.get_blob_tags(credentials, options["container_name"], blob["name"])
        print(tags)

        if options["tag_key"] in tags:
            del tags[options["tag_key"]]
            azure_wrapper.set_blob_tags(credentials, options["container_name"], blob["name"], tags)

            new_tags = azure_wrapper.get_blob_tags(credentials, options["container_name"], blob["name"])
            print(new_tags)


def delete_blobs(blob_list, credentials, options):
    for blob in blob_list:
        azure_wrapper.delete_blob(credentials, options["container_name"], blob["name"])


def download_blobs(blob_list, credentials, options):
    for blob in blob_list:
        file_path = options["path"] + "/" + blob["name"]
        azure_wrapper.download_blob(credentials, options["container_name"], blob["name"], file_path)
