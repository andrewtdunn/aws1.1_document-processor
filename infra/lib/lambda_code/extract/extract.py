import urllib.parse


def handler(event, context):
  # Get the bucket name
  bucket = event['Records'][0]['s3']['bucket']['name']

  # Get the object key (filename/path) and decode it
  # Decoding is necessary for filenames with spaces or special characters
  key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding="utf-8")

  print(f"Bucket: {bucket}")
  print(f"Key: {key}")

  