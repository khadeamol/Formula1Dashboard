from google.cloud import storage


client = storage.Client()
bucket = client.get_bucket("f1dashboard")
blobs = bucket.list_blobs(prefix = "",delimiter="/")
# print(blobs.prefixes)

for blob in blobs:
    print("JJAJSJASJJAS")
    print(blob)