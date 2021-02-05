import argparse

from core import page_upload_download

def main(cli_options):
    if cli_options['operation'] == "upload":
        page_upload_download.upload_page_blob(cli_options['destination'], cli_options['source'])
    elif cli_options['operation'] == "download":
        page_upload_download.download_page_blob(cli_options['source'], cli_options['destination'])
    elif cli_options['operation'] == "copy":
        page_upload_download.copy_page_from_url(cli_options['source'], cli_options['destination'])
    else:
        raise Exception("Invalid argument")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="VHD Uploader/Download : Optimize page blob uploads/downloads")

    # Add the basic arguments to parser
    arg_parser.add_argument("-o", "--operation", required=True,
                            help="Enum(upload/download/copy)")
    arg_parser.add_argument("-s", "--source", required=True,
                            help="Source Blob URL with SAS or local VHD")
    arg_parser.add_argument("-d", "--destination", required=True,
                            help="Destination Blob URL with SAS or local path to download")

    cli_options = vars(arg_parser.parse_args())
    main(cli_options)