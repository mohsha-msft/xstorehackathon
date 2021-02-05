import os
import sys
import concurrent.futures

BLOCK_SIZE = 4 * 1024 * 1024  # 16M block


def download_current_block(page_ranges, curr_page):
    for page in page_ranges:
        if curr_page["end"] < page["start"]:
            return False
        elif curr_page["start"] <= page["end"] and curr_page["end"] >= page["start"]:
            return True
        else:
            continue
    return False


def upload_page(blob_client, start, bytes_arr, ):
    upload = False
    for i in bytes_arr:
        if i != 0:
            upload = True
            break

    if upload:
        blob_client.upload_page(bytes_arr, start, len(bytes_arr))


def upload_page_blob(sas_url, source_path):
    from azure.storage.blob import BlobClient
    from pathlib import Path

    blob_client = BlobClient.from_blob_url(sas_url)
    blob_client.create_page_blob(Path(source_path).stat().st_size)
    src_blob = open(source_path, "rb")

    executor = concurrent.futures.ThreadPoolExecutor(128)
    start = 0
    while block := src_blob.read(BLOCK_SIZE):
        executor.submit(upload_page, blob_client, start, block)
        start = start + BLOCK_SIZE

    executor.shutdown()
    src_blob.close()


def download_range(blob_client, valid_pages, start, length):
    if download_current_block(valid_pages, {"start": start, "end": start + BLOCK_SIZE}):
        download_stream = blob_client.download_blob(start, length)
        return download_stream.readall()
    return bytearray(length)

def download_page_blob(sas_url, destination_path):
    from azure.storage.blob import BlobClient

    blob_client = BlobClient.from_blob_url(sas_url)
    properties = blob_client.get_blob_properties()
    myblob = open(destination_path, "wb")

    page_ranges = blob_client.get_page_ranges(0, properties["size"])[0]

    start = 0
    executor = concurrent.futures.ThreadPoolExecutor(128)
    futures = []
    while start < properties["size"]:
        futures.append(executor.submit(download_range, blob_client, page_ranges, start, min(BLOCK_SIZE, properties["size"] - start +1 )))
        start = start + BLOCK_SIZE

    for future in concurrent.futures.as_completed(futures):
        myblob.write(future.result())
    myblob.close()

