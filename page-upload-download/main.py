import argparse

from core import page_upload_download


def main(cli_options):
    if cli_options['operation'] == "Upload":
        page_upload_download.upload_page_blob(cli_options['blob_sas_url'], cli_options['path'])
    elif cli_options['operation'] == "Download":
        page_upload_download.download_page_blob(cli_options['blob_sas_url'], cli_options['path'])
    else:
        raise Exception("Invalid argument")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="VHD Uploader/Download : Optimize page blob uploads/downloads")

    # Add the basic arguments to parser
    arg_parser.add_argument("-u", "--blob-sas-url", required=True,
                            help="Blob URL containing SAS")
    arg_parser.add_argument("-p", "--path", required=True,
                            help="Path to upload/download")
    arg_parser.add_argument("-o", "--operation", required=True,
                            help="Enum(Upload/Download)")

    cli_options = vars(arg_parser.parse_args())
    main(cli_options)
