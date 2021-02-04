import sys
import argparse
from core import azure_wrapper

CliOptions = None

def main():
    azure_wrapper.set_credentials(CliOptions.connection-string)

    if CliOptions.list-versions:
        blob_version = azure_wrapper.list_blob_versions(CliOptions.container,
                                                        CliOptions.blob) 
        print(blob_version)

    elif CliOptions.delete-version:
        azure_wrapper.delete_blob_version(CliOptions.container,
                                          CliOptions.blob,
                                          CliOptions.delete-version)
        print("Deleted successfully")

    elif CliOptions.create-version:
        options = {
             "file_path": CliOptions.create-version,
             "blob_type": CliOptions.blob-type,
        }
        azure_wrapper.add_blob_version(CliOptions.container,
                                       CliOptions.blob,
                                       options)
        print("New version created successfully")
    
    elif CliOptions.get-version:
        options = {
            "file_path": CliOptions.file,
            "version_id": CliOptions.get-version,
        }
        size = azure_wrapper.download_blob_version(CliOptions.container,
                                                   CliOptions.blob,
                                                   options)
        print("Version downloaded successfully to give file. Size : " + len(size))

    elif CliOptions.delete-version-condition:
        options = {}
        if CliOptions.condition-before-date:
            options = {
                'delete_before': CliOptions.condition-before-date
            }
        elif CliOptions.condition-after-date:
            options = {
                'delete_after': CliOptions.condition-after-date
            }
        elif CliOptions.condition-between-date:
            options = {
                'delete_between': [CliOptions.condition-before-date, CliOptions.condition-after-date],
            }
        
        delete_cond_resp = azure_wrapper.delete_blob_with_condition(CliOptions.container,
                                                                    CliOptions.blob,
                                                                    options)
        print("Deleted blob versions successfully")
        
    elif CliOptions.set-tier-of-version:
        options = {
            'blob_type': CliOptions.blob-type,
            'tier': CliOptions.tier,
            'version_id': CliOptions.set-tier-of-version
        }

        azure_wrapper.blob_version_set_tier(CliOptions.container,
                                            CliOptions.blob, 
                                            options)
        
        print("Blob Version set successfully")

    print("Blob Version life cycle manager... signing off...")


if __name__ == "__main__":
    # Construct the argument parser
    arg_parser = argparse.ArgumentParser(description="Blob version life cycle manager")

    # Add the basic arguments to parser
    arg_parser.add_argument("-s", "--connection-string", required=True,
                            help="Connection string to the storage account")
    arg_parser.add_argument("-c", "--container", required=True,
                            help="Name of the container in storage account")
    arg_parser.add_argument("-b", "--blob", required=True,
                            help="Path to blob to be used (exclude container name here) e.g. Dir1/Dir2/file3.txt")

    
    # Add operation specific arguments to parser
    # Below arguments are mutually exclusive as only one operation can be performed at a time
    ex_group = arg_parser.add_mutually_exclusive_group()
    ex_group.add_argument("-l", "--list-versions", action="store_true",
                            help="List all available version of the blob")
    ex_group.add_argument("-d", "--delete-version",
                            help="Delete specified version of blob")
    ex_group.add_argument("-a", "--create-version",
                            help="Create a new version of blob by uploading the given file to blob. --blob-type is mandatory with this")
    ex_group.add_argument("-g", "--get-version",
                            help="Download specified version of blob. Data will be stored in file specified in --file parameter")
    ex_group.add_argument("-x", "--delete-version-condition", action="store_true",
                            help="Delete all versions of blob matching given date in --condition* option")
    ex_group.add_argument("-e", "--set-tier-of-version", 
                            help="Set tier of given version of blob. --tier and --blob-type are mandatory for this option")

    # Optional arguments depending upon the above operation
    arg_parser.add_argument("-t", "--blob-type", 
                            help="Type of blob [BlockBlob, PageBlob")
    arg_parser.add_argument("-f", "--file", 
                            help="Path to local file to be used")
    arg_parser.add_argument("-lt", "--condition-before-date", 
                            help="Match blob versions based on last modified date <= given date")
    arg_parser.add_argument("-gt", "--condition-after-date", 
                            help="Match blob versions based on last modified date >= given date")
    arg_parser.add_argument("-bt", "--condition-between-date", action="store_true", 
                            help="Match blob versions based on : <condition-before-date> >=  last modified date >= <condition-after-date>")
    arg_parser.add_argument("-tr", "--tier", 
                            help="Tier value for the blob")

    #args = vars(arg_parser.parse_args())
    
    CliOptions = arg_parser.parse_args()
    print(CliOptions)
    main()
