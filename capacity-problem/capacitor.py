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
UsageInfo = namedtuple("UsageInfo", "Container Type Folder DirCount FileCount AppendCount PageCount TotalSize Allocated")

# Below is how to use the namedtuple
#a = BlobInfo(Container="abc", Folder="def", DirCount=5, FileCount=6)
#print(a.Container, a.DirCount)

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
def SizeCalculator(thrId):
    #print("Child " + str(thrId) + " started")
    global InitialIterationDone
    global IterationRunning
    global MaxThreadCount


    Done = False

    totalPathProcessed = 0
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
                                AppendCount=0,
                                PageCount=0,
                                Allocated=0))

        elif queue_item.Type == "Append":
            UsageSummary.put(UsageInfo(
                                Container=queue_item.Container, 
                                Folder=queue_item.ListPath,
                                Type="Append",
                                DirCount=0, 
                                FileCount=0, 
                                TotalSize=0,
                                AppendCount=1,
                                PageCount=0,
                                Allocated=0))
        elif queue_item.Type == "Page":
            UsageSummary.put(UsageInfo(
                                Container=queue_item.Container, 
                                Folder=queue_item.ListPath,
                                Type="Page",
                                DirCount=0, 
                                FileCount=0, 
                                TotalSize=0,
                                AppendCount=0,
                                PageCount=1,
                                Allocated=0))
        else:
            print("Unsupported Blob Type")


        PendingList.task_done()

        IteratorLock.acquire()
        IterationRunning -= 1
        IteratorLock.release()
        
    #print("Child " + str(thrId) + " exited : Dir " + str(totalPathProcessed))
    MaxThreadCount -= 1


def ReportUsage():
    page_count = 0
    dir_count = 0
    file_count = 0
    append_count = 0
    page_count = 0

    total_size = 0

    Done = False
    while not Done:
        try:
             usage_item = UsageSummary.get(timeout=3)
        except:
            if MaxThreadCount == 0:
                Done = True
            continue

        usage_item = UsageSummary.get()
        if usage_item.Type == "Block":
            dir_count += usage_item.DirCount
            file_count += usage_item.FileCount
            total_size += usage_item.TotalSize
        elif usage_item.Type == "Append":
            append_count += usage_item.AppendCount
        elif usage_item.Type == "Page":
            page_count += usage_item.PageCount
        
        #print(usage_item)
        print(".", end ="")
        UsageSummary.task_done()

    # Count the file share items seperatly
    fileShareStats = Azure.ListFileShares()
    fileShareUsage = 0
    for fileShareItem in fileShareStats:
        fileShareUsage += fileShareStats[fileShareItem]
        print("#", end ="")

    global TotalContainer
    print("")
    print("----------------------------------------------------------------")
    print("Total Containers        : " + str(TotalContainer))
    print("Total Directories       : " + str(dir_count))
    print("Total Block Blobs       : " + str(file_count))
    print("Total Append Blobs      : " + str(append_count))
    print("Total Page Blobs        : " + str(page_count))
    print("Total Data              : " + str(total_size))
    print("----------------------------------------------------------------")
    print("Total File Shares       : " + str(len(fileShareStats)))
    print("Total File Share Usage  : " + str(fileShareUsage))
    print("----------------------------------------------------------------")
    
    fileShareStats.clear()
    print("Capacitor is tired... bye bye !!!")    



# ----------------------- Main processing --------------------------
def main(argv):
    if len(argv) < 1:
        print("Provide connection string as input parameter")
        exit()
    
    Azure.SetConnectionString(argv[0])

    # Get the list of containers from the storage account
    # Push them to queue for first level of iteration
    global TotalContainer
    container_list = Azure.ListStorageContainers()
    TotalContainer = len(container_list)

    if TotalContainer == 0:
        print("There is nothing to iterate in this account")
        exit()

    for container in container_list:
        PendingList.put(QueueItem(Container=container, Type="Block", ListPath=""))
    container_list.clear()

    # Start the thread to report the usage info
    report_thread = threading.Thread(target=ReportUsage)
    report_thread.daemon = True
    report_thread.start()


    # Start N threads to iteratre the directory and list recursively
    for i in range(MaxThreadCount):
        #print("Starting child thread " + str(i))
        t = threading.Thread(target=SizeCalculator,  args=[i])
        t.daemon = True
        IteratorPoolList.append(t)
        t.start()

    #StopProcessing = True
    for itr in IteratorPoolList:
        itr.join()
    report_thread.join()



if __name__ == "__main__":
    main(sys.argv[1:])

