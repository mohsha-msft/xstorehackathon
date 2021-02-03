#!/usr/bin/python
import queue 
import threading
import os
import time
import sys
from pathlib import Path

import azure_wrapper as Azure

from collections import namedtuple

# Queue item to be iterated by the thread pool
QueueItem = namedtuple("QueueItem", "Container Type ListPath")
# Type : Block / Page

# Info for each directory for block blob and each page for page blob
UsageInfo = namedtuple("UsageInfo", "Container Type Folder DirCount FileCount TotalSize Allocated")

# Below is how to use the namedtuple
#a = BlobInfo(Container="abc", Folder="def", DirCount=5, FileCount=6)
#print(a.Container, a.DirCount)

# List Containing pending iteration objects
PendingList = queue.Queue()
UsageSummary = queue.Queue()

StopProcessing = False
InitialIterationDone = False
TotalContainer = 0

IteratorPoolList = []
def SizeCalculator(thrId):
    #print("Child " + str(thrId) + " started")
    global InitialIterationDone

    totalPathProcessed = 0
    while True:
        queue_item = PendingList.get()
        #print("Iterating path : " + queue_item.Container + ":" + queue_item.ListPath)
        
        totalPathProcessed += 1
        
        dir_count = 0
        file_count = 0
        total_size = 0
        if queue_item.Type == "Block" :
            blob_list = Azure.ListStorageBlobs(queue_item.Container, queue_item.ListPath)

            for blob in blob_list:
                blob_info = Azure.GetBlobInfo(blob)
                if blob_info["dir"]:
                    dir_count += 1
                    PendingList.put(QueueItem(Container=queue_item.Container, Type="Block", ListPath=blob_info["name"]))
                else:
                    file_count += 1
                    total_size += blob_info["size"]
                blob_info.clear()

            # Append this folder summary to usage queue
            if queue_item.Container == "":
                queue_item.Container = "$ROOT"

            UsageSummary.put(UsageInfo(
                                Container=queue_item.Container, 
                                Folder=queue_item.ListPath,
                                Type="Block",
                                DirCount=dir_count, 
                                FileCount=file_count, 
                                TotalSize=total_size,
                                Allocated=0))

        else:
            print("Page blob support to be added here")


        PendingList.task_done()

    print("Child " + str(thrId) + " exited : Dir " + str(totalPathProcessed))


def ReportUsage():
    page_count = 0
    dir_count = 0
    file_count = 0
    total_size = 0

    while True:
        usage_item = UsageSummary.get()
        
        dir_count += usage_item.DirCount
        file_count += usage_item.FileCount
        total_size += usage_item.TotalSize
        
        print(usage_item)
        UsageSummary.task_done()



# ----------------------- Main processing --------------------------
def main(argv):
    if len(argv) < 1:
        print("Provide connection string as input parameter")
        exit()
    
    Azure.SetConnectionString(argv[0])

    # Get the list of containers from the storage account
    # Push them to queue for first level of iteration
    container_list = Azure.ListStorageContainers()
    TotalContainer = len(container_list)

    for container in container_list:
        PendingList.put(QueueItem(Container=container, Type="Block", ListPath=""))
    container_list.clear()


    # Start the thread to report the usage info
    report_thread = threading.Thread(target=ReportUsage)
    report_thread.daemon = True
    report_thread.start()


    # Start N threads to iteratre the directory and list recursively
    MaxThreadCount = 8
    for i in range(MaxThreadCount):
        #print("Starting child thread " + str(i))
        t = threading.Thread(target=SizeCalculator,  args=[i])
        t.daemon = True
        IteratorPoolList.append(t)
        t.start()

    #StopProcessing = True
    for itr in IteratorPoolList:
        itr.join()



if __name__ == "__main__":
    main(sys.argv[1:])

