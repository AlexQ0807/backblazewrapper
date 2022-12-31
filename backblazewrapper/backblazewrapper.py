import os
import json
import requests
from b2sdk.v1 import InMemoryAccountInfo, B2Api

class BackBlazeWrapper:

    b2_api = None
    bucket = None

    def __init__(self, appkey_id, appkey, bucket_name=None):
        try:
            info = InMemoryAccountInfo()  # store credentials, tokens and cache in memory
            self.b2_api = B2Api(info)
            self.b2_api.authorize_account("production", appkey_id, appkey)

            if bucket_name is not None:
                self.set_bucket(bucket_name)
        except Exception as e:
            raise Exception("Unable to establish b2_api credentials: {}".format(e))

    def bucket_exists(self, bucket_name):
        ''' Check if bucket exists in backblaze

        :param bucket_name:
        :return:
        '''
        exists = False
        try:
            self.b2_api.get_bucket_by_name(bucket_name)
            exists = True
        except:
            pass
        return exists


    def set_bucket(self, bucket_name):
        ''' Set the current bucket

        :param bucket_name:
        :return:
        '''
        was_set = False
        if self.bucket_exists(bucket_name):
            self.bucket = self.b2_api.get_bucket_by_name(bucket_name, )
            was_set = True
        return was_set

    def get_bucket(self):
        ''' Get the current bucket

        :return:
        '''
        return self.bucket


    def list_files(self, folder=""):
        ''' List files inside the bucket. Default show files located in the root folder
        :param folder:
        :return:
        '''
        if self.bucket is not None:
            files = [file_info.file_name for file_info, folder_name in
             self.bucket.ls(folder_to_list=folder, show_versions=False)]
        else:
            raise Exception("bucket was not set")
        return files


    def upload_local_file(self, local_filepath, upload_filepath):
        ''' Upload a local file/folder into the current bucket

        Note for upload_filepath:
        -specifying the filename only will upload the file to the root bucket directory
            ex) "test.json" ->   bucket/test.json
        -specifying a folder structure with the filename will upload the structure to the bucket
            ex) "folder1/test.json" -> bucket/folder1/test.json
        :param local_filepath: location path of the file to upload
        :param upload_filepath: filepath for the uploaded file
        :return:
        '''
        if self.bucket is not None:
            try:
                self.bucket.upload_local_file(local_filepath, upload_filepath)
            except Exception as e:
                raise Exception("Upload to BackBlaze failed: {}".format(e))
        else:
            raise Exception("bucket was not set")


    def upload_local_file_bytes(self, byte_data, upload_filepath):
        ''' Upload byte content to the bucket

        Note for upload_filepath:
        -specifying the filename only will upload the file to the root bucket directory
            ex) "test.json" ->   bucket/test.json
        -specifying a folder structure with the filename will upload the structure to the bucket
            ex) "folder1/test.json" -> bucket/folder1/test.json

        :param byte_data:
        :param upload_filepath:
        :return:
        '''
        if self.bucket is not None:
            try:
                self.bucket.upload_bytes(byte_data, upload_filepath)
            except Exception as e:
                raise Exception("Upload to BackBlaze failed: {}".format(e))
        else:
            raise Exception("bucket was not set")


    def get_download_url(self, file_to_download):
        ''' Get download URL for a given file in the bucket

        :param file_to_download:
        :return:
        '''
        try:
            download_url = self.bucket.get_download_url(file_to_download)
        except Exception as e:
            raise Exception("Failed to get download url from BackBlaze: {}".format(e))
        return download_url


    def get_download_authorization_header(self, file_to_download, duration_seconds=30):
        '''Request a download token returned in a header
        NOTE: token expires after a given amount of time

        :param file_to_download: file name
        :param duration_seconds: number of seconds before the token expire
        :return:
        '''
        try:
            header = {
                'Authorization': self.bucket.get_download_authorization(file_to_download, duration_seconds)
            }
        except Exception as e:
            raise Exception("Failed to get download auth header from BackBlaze: {}".format(e))
        return header

    def upload_file(self, filepath, upload_filepath=None):
        upload_success = False
        try:
            if upload_filepath is None:
                upload_filepath = os.path.basename(filepath)

            # Get absolute path
            with open(filepath, "rb") as file:
                data = file.read()
                self.upload_local_file_bytes(data, upload_filepath)
                upload_success = True
        except Exception as e:
            raise Exception("Failed to upload local file to BackBlaze: {}".format(e))

        return upload_success

    def upload_data(self, data, upload_filepath):
        upload_success = False
        try:
            byte_data = bytes(json.dumps(data), encoding='utf8')
            self.upload_local_file_bytes(byte_data, upload_filepath)
            upload_success = True
        except Exception as e:
            raise Exception("Failed to upload data to BackBlaze: {}".format(e))

        return upload_success

    def fetch_file_content_by_name(self, file_to_download):
        data = None
        try:
            download_url = self.get_download_url(file_to_download=file_to_download)
            res = requests.get(download_url)
            data = None
            if res.status_code == 200:
                data = res.json()
        except Exception as e:
            raise Exception("Failed to download file from BackBlaze: {}".format(e))

        return data


