from . import azure_wrapper


def schedule_job(blob_list, options):
    if options["operation"] == "delete_blobs":
        return "delete_blobs"
    elif options["operation"] == "download_blobs":
        return "download_blobs"
    elif options["operation"] == "add_tag":
        return "add_tags"
    elif options["operation"] == "update_tag":
        return "update_tag"
    elif options["operation"] == "delete_tag":
        return "delete_tags"
    else:
        raise Exception('Invalid option chosen')
