import argparse
import datetime as dt
import os

from core import azure_wrapper
datetime_format = '%Y-%m-%d %H:%M:%S'

def main(cli_options):
    if cli_options['connection_string']:
        azure_wrapper.set_credentials(cli_options['connection_string'])
    else:
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        azure_wrapper.set_credentials(conn_str)

    # azure_wrapper.generate_blob_with_versions(cli_options['container'], cli_options['blob'], 10, 'BlockBlob')

    if cli_options['list_versions']:
        blob_versions = azure_wrapper.list_blob_versions(cli_options['container'], cli_options['blob'])
        print("Total versions found: " + str(len(blob_versions)))
        for blob_version in blob_versions:
            print(blob_version)

    elif cli_options['delete_version']:
        azure_wrapper.delete_blob_version(cli_options['container'],
                                          cli_options['blob'],
                                          cli_options['delete_version'])
        print("Deleted successfully")

    elif cli_options['create_version']:
        options = {
            "file_path": cli_options['create_version'],
            "blob_type": cli_options['blob_type'],
        }
        azure_wrapper.add_blob_version(cli_options['container'],
                                       cli_options['blob'],
                                       options)
        print("New version created successfully")

    elif cli_options['get_version']:
        options = {
            "file_path": cli_options['file'],
            "version_id": cli_options['get_version'],
        }
        size = azure_wrapper.download_blob_version(cli_options['container'],
                                                   cli_options['blob'],
                                                   options)
        print("Version downloaded successfully to give file. Size : " + str(size))

    elif cli_options['delete_version_condition']:
        options = {}
        if cli_options['condition_between_date']:
            start_date_time = dt.datetime.strptime(cli_options['condition_after_date'], datetime_format)
            end_date_time = dt.datetime.strptime(cli_options['condition_before_date'], datetime_format)
            options = {
                'delete_between': [dt.datetime(start_date_time.year, start_date_time.month, start_date_time.day,
                                               start_date_time.hour,
                                               start_date_time.minute, start_date_time.second,
                                               start_date_time.microsecond, tzinfo=dt.timezone.utc),
                                   dt.datetime(end_date_time.year, end_date_time.month, end_date_time.day,
                                               end_date_time.hour,
                                               end_date_time.minute, end_date_time.second,
                                               end_date_time.microsecond, tzinfo=dt.timezone.utc)]
            }
        elif cli_options['condition_before_date']:
            date_time = dt.datetime.strptime(cli_options['condition_before_date'], datetime_format)
            options = {
                'delete_before': dt.datetime(date_time.year, date_time.month, date_time.day, date_time.hour,
                                             date_time.minute, date_time.second, date_time.microsecond,
                                             tzinfo=dt.timezone.utc)
            }
        elif cli_options['condition_after_date']:
            date_time = dt.datetime.strptime(cli_options['condition_after_date'], datetime_format)
            options = {
                'delete_after': dt.datetime(date_time.year, date_time.month, date_time.day, date_time.hour,
                                            date_time.minute, date_time.second, date_time.microsecond,
                                            tzinfo=dt.timezone.utc)
            }

        # print(options)
        deleted_versions = azure_wrapper.delete_blob_with_condition(cli_options['container'],
                                                                    cli_options['blob'],
                                                                    options)
        for deleted_version in deleted_versions:
            print(deleted_version)
        print("Deleted blob versions successfully")

    elif cli_options['set_tier_of_version']:
        options = {
            'blob_type': cli_options['blob_type'],
            'tier': cli_options['tier'],
            'version_id': cli_options['set_tier_of_version']
        }

        azure_wrapper.blob_version_set_tier(cli_options['container'],
                                            cli_options['blob'],
                                            options)

        print("Blob Version set successfully")


if __name__ == "__main__":
    # Construct the argument parser
    arg_parser = argparse.ArgumentParser(description="Blob version life cycle manager")

    # Add the basic arguments to parser
    arg_parser.add_argument("-s", "--connection-string",
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

    cli_options = vars(arg_parser.parse_args())
    print(cli_options)
    print("================================================================================")
    main(cli_options)
    print("================================================================================")
    print("Blob Version life cycle manager... signing off...")
