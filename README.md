## Wrapper for Backblaze (Private)
<hr>

### Setup
```
pip install git+https://github.com/AlexQ0807/backblazewrapper.git
```

### Example - Initialize Wrapper

```
    from backblazewrapper.backblazewrapper import BackBlazeWrapper

    appkey_id = "XXXXXXXXXX"
    appkey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    bucket_name = "bucketname"
    bbw = BackBlazeWrapper(appkey_id, appkey, bucket_name=bucket_name)
```


### Example - Uploading file to backblaze

```
    with open("../test.json", "rb") as file:
        data = file.read()
        print(type(data))
        bbw.upload_local_file_bytes(data, "folder1/test.json")
```


### Example - Get bucket contents

```
    files = bbw.list_files()
    print(files)
```