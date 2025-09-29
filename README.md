# S3 File Sorter Lambda Function

A simple Lambda function that automatically sorts files uploaded to an S3 bucket based on their filenames.

## What Does This Do?

When you upload a file to your S3 source bucket, this Lambda function automatically:
- Checks if the filename is **purely numeric** (like `123.txt`, `456.pdf`)
- Moves **numeric files** to **Destination2 bucket**
- Moves **all other files** to **Destination1 bucket**
- Deletes the original file from the source bucket

## How to Use:

### Prerequisites
- AWS Account
- 3 S3 buckets created (source, destination1, destination2)
- Lambda function with Python 3.9 runtime
- IAM role with S3 read/write permissions

### Setup Steps:

1. **Create a Lambda Function**
   - Go to AWS Lambda Console
   - Click "Create function"
   - Choose "Author from scratch"
   - Runtime: Python 3.9
   - Create or choose an execution role with S3 permissions

2. **Copy the Code**
   - Copy the code from `file_sorter.py`
   - Paste it into your Lambda function

3. **Set Environment Variables**
   - `DESTINATION1_BUCKET` = your-destination1-bucket-name
   - `DESTINATION2_BUCKET` = your-destination2-bucket-name

4. **Add S3 Trigger**
   - Click "Add trigger"
   - Choose "S3"
   - Select your source bucket
   - Event type: "All object create events"
   - Click "Add"

5. **Test It!**
   - Upload a file named `123.txt` to your source bucket
   - It should appear in Destination2
   - Upload a file named `report.doc` to your source bucket
   - It should appear in Destination1

## Required IAM Permissions

Your Lambda execution role needs these S3 permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::your-source-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::your-destination1-bucket/*",
        "arn:aws:s3:::your-destination2-bucket/*"
      ]
    }
  ]
}
```

