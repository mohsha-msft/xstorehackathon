import argparse
import os
import queue
import threading
from collections import namedtuple

from core import azure_wrapper as azure

# Queue item to be iterated by the thread pool
QueueItem = namedtuple("QueueItem", "Container Type ListPath")
# Type : Block / Page

# Info for each directory for block blob and each page for page blob
DeletionQueue = namedtuple("DeletionQueue",
                           "Container BlobList")

# Below is how to use the namedtuple
# a = BlobInfo(Container="abc", Folder="def", DirCount=5, FileCount=6)
# print(a.Container, a.DirCount)

# List Containing pending iteration objects
PendingList = queue.Queue()
UsageSummary = queue.Queue()

StopProcessing = False
InitialIterationDone = False
TotalContainer = 0

MaxThreadCount = 8
IterationRunning = 0
IteratorLock = threading.Lock()

IteratorPoolList = []


def thread_handler(thrId):
    # print("Child " + str(thrId) + " started")
    global InitialIterationDone
    global IterationRunning
    global MaxThreadCount

    Done = False

    total_path_processed = 0
    while not Done:
        try:
            queue_item = PendingList.get(timeout=3)
        except:
            if PendingList.empty() and IterationRunning == 0:
                Done = True
            continue

        IteratorLock.acquire()
        IterationRunning += 1
        IteratorLock.release()

        # print("Iterating path : " + queue_item.Container + ":" + queue_item.ListPath)

        total_path_processed += 1

        dir_count = 0
        file_count = 0
        total_size = 0
        if queue_item.Type == "Block":
            blob_list = azure.list_storage_blobs(queue_item.Container, queue_item.ListPath)
            blob_path_list = []
            for blob in blob_list:
                blob_info = azure.get_blob_info(blob)
                if blob_info["dir"]:
                    dir_count += 1
                    PendingList.put(QueueItem(Container=queue_item.Container, Type="Block", ListPath=blob_info["name"]))
                else:
                    file_count += 1
                    total_size += blob_info["size"]
                    blob_path_list.append(blob_info["name"])
                blob_info.clear()

            if len(blob_path_list) > 0:
                UsageSummary.put(DeletionQueue(Container=queue_item.Container, BlobList=blob_path_list))

        PendingList.task_done()

        IteratorLock.acquire()
        IterationRunning -= 1
        IteratorLock.release()

    # print("Child " + str(thrId) + " exited : Dir " + str(total_path_processed))
    IteratorLock.acquire()
    MaxThreadCount -= 1
    IteratorLock.release()



def delete_batch():
    Done = False
    while not Done:
        try:
            usage_item = UsageSummary.get(block=False, timeout=3)
        except:
            if MaxThreadCount == 0:
                Done = True
            continue

        print(usage_item.BlobList)
        azure.delete_blob_batch(usage_item.Container, usage_item.BlobList)
        UsageSummary.task_done()


# ----------------------- Main processing --------------------------
def main(cli_options):
    global MaxThreadCount

    if cli_options['connection_string']:
        azure.set_connection_string(cli_options['connection_string'])
    else:
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        azure.set_connection_string(conn_str)

    if cli_options['parallel_factor']:
        MaxThreadCount = int(cli_options['parallel_factor'])

    # Get the list of containers from the storage account
    # Push them to queue for first level of iteration
    global TotalContainer
    container_list = azure.list_storage_containers()
    TotalContainer = len(container_list)

    if TotalContainer == 0:
        print("There is nothing to iterate in this account")
        exit()

    for container in container_list:
        PendingList.put(QueueItem(Container=container, Type="Block", ListPath=""))
    # container_list.clear()

    # Start the thread to report the usage info
    report_thread = threading.Thread(target=delete_batch)
    report_thread.daemon = True
    report_thread.start()

    # Start N threads to iterate the directory and list recursively
    for i in range(MaxThreadCount):
        # print("Starting child thread " + str(i))
        t = threading.Thread(target=thread_handler, args=[i])
        t.daemon = True
        IteratorPoolList.append(t)
        t.start()

    # StopProcessing = True
    for itr in IteratorPoolList:
        itr.join()
    report_thread.join()


if __name__ == "__main__":
    # Construct the argument parser
    arg_parser = argparse.ArgumentParser(description="Batch Delete : Program to delete content in blob storage account")

    # Add the basic arguments to parser
    arg_parser.add_argument("-s", "--connection-string",
                            help="Connection string to the storage account")
    arg_parser.add_argument("-p", "--parallel-factor",
                            help="Parallel execution factor")

    cli_options = vars(arg_parser.parse_args())
    main(cli_options)
    print("Graceful exit ... bye bye !!!")
