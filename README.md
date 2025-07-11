# 🔄 Self-Hosted Dynamic DNS + S3 Access Control  
**A Secure, Containerized DDNS System Using AWS Route 53 & S3**

This project updates a Route 53 DNS record with your machine's current public IP and securely updates an S3 bucket policy to allow access only from that IP. It's packaged in a Docker container and designed to run continuously via Kubernetes or Docker.

---

## 🧰 Tech Stack

- **Python 3.13** — Main logic (DDNS + S3 policy)
- **AWS Route 53** — DNS record updates
- **AWS S3** — IP-restricted access via dynamic policy
- **Docker** — Containerization
- **Kubernetes** — Deployment and orchestration
- **Bash** — Runtime script and log management

---

## 🛠 Features

- 🔄 **Automatic DNS updates** to Route 53 when public IP changes
- 🔒 **S3 access control** — Updates bucket policy to restrict access by IP
- 🐳 **Dockerized** for clean and portable deployment
- 📜 **Log rotation** inside container using a Bash loop
- 📦 **Deployable to Kubernetes** (Raspberry Pi-compatible)
- ✅ **Retry logic** for both DNS and S3 updates with 15 attempts and 10s delay

---

## ⚙️ Configuration

Configure AWS credentials and runtime variables via Kubernetes secrets or a `.env` file.

### Required AWS IAM Permissions

- `route53:ListResourceRecordSets`
- `route53:ChangeResourceRecordSets`
- `s3:GetBucketPolicy`
- `s3:PutBucketPolicy`

### Kubernetes Example: Secret and Pod

```yaml
# aws-credentials secret
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID: your-access-key
  AWS_SECRET_ACCESS_KEY: your-secret-key
  AWS_REGION: us-east-1
