import boto3
import os
import json

# Configuration
BUCKET_NAME = "mayur-sdk-static-website-0672"
REGION = "ap-south-1"
WEBSITE_FOLDER = "website"

s3 = boto3.client("s3", region_name=REGION)

# Create Bucket
try:
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={
            "LocationConstraint": REGION
        }
    )
    print(f"Bucket '{BUCKET_NAME}' created successfully.")

except Exception as e:
    print("Bucket already exists or cannot be created.")
    print(e)

# Upload Website Files
print("\nUploading website files...\n")

for file in os.listdir(WEBSITE_FOLDER):

    file_path = os.path.join(WEBSITE_FOLDER, file)

    if os.path.isfile(file_path):

        if file.endswith(".html"):
            content_type = "text/html"
        elif file.endswith(".css"):
            content_type = "text/css"
        elif file.endswith(".js"):
            content_type = "application/javascript"
        else:
            content_type = "application/octet-stream"

        s3.upload_file(
            file_path,
            BUCKET_NAME,
            file,
            ExtraArgs={"ContentType": content_type}
        )

        print(f"Uploaded: {file}")

print("\nAll website files uploaded successfully.")

# Enable Static Website Hosting
s3.put_bucket_website(
    Bucket=BUCKET_NAME,
    WebsiteConfiguration={
        "IndexDocument": {
            "Suffix": "index.html"
        }
    }
)

print("Static Website Hosting Enabled.")

# Apply Bucket Policy
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
        }
    ]
}

try:
    s3.put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=json.dumps(policy)
    )
    print("Bucket Policy Applied.")

except Exception as e:
    print("Could not apply bucket policy.")
    print(e)

print("\nWebsite URL:")
print(f"http://{BUCKET_NAME}.s3-website-{REGION}.amazonaws.com")