# download_blobs.py
# Python program to bulk download blob files from azure storage
# Uses latest python SDK() for Azure blob storage
# Requires python 3.6 or above
# pip3 install azure-storage-blob --user
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

# azure blob 스토리지 연결
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# 로컬 파일 경로
LOCAL_BLOB_PATH = "/Users/yusunglee/Downloads/slack"
# 업로드 경로: azure blob container
BLOB_CONTAINER = "testapibuild"


# blob 스토리지 연결 문자열을 통해 blob에 접근하는 인스턴스 생성
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER)


def save_blob(file_name,file_content):
    download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)   # /LOCAL_BLOB_PATH/file_name
    # for nested blobs, create local path as well!
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True) # 하위 디렉토리까지 생성
    with open(download_file_path, "wb") as file:
      file.write(file_content)

def download_all_blobs_in_container():
    my_blobs = container_client.list_blobs()            # blob 리스트가 있는 my_blobs 인스턴스 생성
    print("my_blobs:", my_blobs)
    for blob in my_blobs:                               # my_blobs 인스턴스에서 blob을 하나씩 꺼냄
        print(blob.name)
        bytes = container_client.get_blob_client(blob).download_blob().readall() # blob의 콘텐츠를 하나하나 읽으면서 다운로드한다.
        save_blob(blob.name, bytes)

download_all_blobs_in_container()
