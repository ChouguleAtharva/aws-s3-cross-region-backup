# AWS Automatic Cross-Region Backup System ☁️

## 📌 Project Overview
This project implements a fully automated, event-driven disaster recovery (DR) system on AWS. It synchronizes files between a **Primary Production Bucket (us-east-1)** and a **Disaster Recovery Bucket (us-east-2)**.

The system is **bi-directional in logic**:
1.  **Backup:** When a file is uploaded to Production, it is automatically copied to DR.
2.  **Sync:** When a file is deleted from Production, it is automatically removed from DR to maintain consistency.

## 🏗️ Architecture
The system utilizes a **Serverless Architecture** to minimize cost and management overhead.

![Architecture Diagram](architecture-diagram.png)

### Workflow
1.  **Upload Event:** User uploads file -> S3 Event Notification -> Triggers `Backup Lambda`.
2.  **Copy Logic:** Lambda decodes the S3 key (handling URL encoding) and executes `CopyObject` to the Destination Region.
3.  **Delete Event:** User deletes file -> S3 Event Notification -> Triggers `Delete Lambda`.
4.  **Delete Logic:** Lambda decodes the key and executes `DeleteObject` in the Destination Region.

## 🛠️ Technologies Used
* **AWS S3:** Object storage (Source & Destination).
* **AWS Lambda (Python 3.11):** Serverless compute for logic execution.
* **AWS IAM:** Managed permissions using the Principle of Least Privilege.
* **Boto3 SDK:** AWS SDK for Python to interact with S3 APIs.
* **CloudWatch:** For logging and monitoring Lambda execution.

## 🧩 Key Challenges & Solutions
During development, I encountered and solved several critical engineering challenges:

1.  **Cross-Region Permissions (`AccessDenied`):**
    * *Problem:* The Lambda function in `us-east-1` could not write to the bucket in `us-east-2` despite having an IAM Role.
    * *Solution:* Implemented a **Resource-Based Bucket Policy** on the destination bucket to explicitly allow `s3:PutObject` and `s3:DeleteObject` actions from my AWS Account ID.

2.  **URL Encoding Issues:**
    * *Problem:* Files with spaces (e.g., `Project Idea.txt`) failed to copy/delete because S3 sends the key as `Project+Idea.txt` (URL encoded).
    * *Solution:* Implemented `urllib.parse.unquote_plus` in the Python Lambda code to decode the key before passing it to the Boto3 API.

## 🚀 How to Deploy
1.  **Create S3 Buckets:** Create two buckets in different AWS regions.
2.  **IAM Role:** Create a role with permissions for `s3:GetObject` (Source), `s3:PutObject` (Dest), and `s3:DeleteObject` (Dest).
3.  **Lambda Setup:** Deploy the code in `src/` to AWS Lambda.
4.  **Triggers:** Configure S3 Event Notifications for `s3:ObjectCreated:*` and `s3:ObjectRemoved:*`.

## 📜 License
This project is open source and available under the MIT License.
© 2025 ATHARVA