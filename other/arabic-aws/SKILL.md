---
name: arabic-aws
name_ar: أمازون ويب سيرفيسز
description: Master AWS cloud services in Arabic
description_ar: إتقان خدمات سحابة أمازون ويب سيرفيسز بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان استخدام خدمات AWS السحابية باللغة العربية.

## الخدمات الأساسية

### ١. الحوسبة (Compute)

| الخدمة | الوصف | الاستخدام |
|--------|-------|----------|
| **EC2** | خوادم افتراضية | تطبيقات ويب، قواعد بيانات |
| **Lambda** | حوسبة بدون خادم | أحداث، معالجة ملفات |
| **ECS/EKS** | إدارة حاويات | Docker، Kubernetes |
| **Elastic Beanstalk** | نشر تطبيقات | نشر تلقائي |

### ٢. التخزين (Storage)

| الخدمة | الوصف | الاستخدام |
|--------|-------|----------|
| **S3** | تخزين كائنات | ملفات، نسخ احتياطي |
| **EBS** | تخزين كتل | أقراص EC2 |
| **EFS** | تخزين ملفات | مشاركة ملفات |
| **Glacier** | أرشفة | بيانات نادرة الوصول |

### ٣. قواعد البيانات (Database)

| الخدمة | الوصف | النوع |
|--------|-------|-------|
| **RDS** | قواعد علائقية | MySQL, PostgreSQL, Oracle |
| **DynamoDB** | NoSQL | سريعة، قابلة للتوسع |
| **ElastiCache** | تخزين مؤقت | Redis, Memcached |
| **Redshift** | مستودع بيانات | تحليلات |

### ٤. الشبكات (Networking)

| الخدمة | الوصف | الاستخدام |
|--------|-------|----------|
| **VPC** | شبكة خاصة | عزل موارد |
| **CloudFront** | CDN | توزيع محتوى |
| **Route 53** | DNS | توجيه نطاقات |
| **API Gateway** | بوابة API | إدارة APIs |

### ٥. الأمان (Security)

| الخدمة | الوصف | الاستخدام |
|--------|-------|----------|
| **IAM** | إدارة هوية | مستخدمين، صلاحيات |
| **KMS** | إدارة مفاتيح | تشفير |
| **WAF** | جدار حماية ويب | حماية تطبيقات |
| **Shield** | حماية DDoS | منع هجمات |

## أوامر AWS CLI

```bash
# إعداد CLI
aws configure

# عرض مثيلات EC2
aws ec2 describe-instances

# إنشاء دلو S3
aws s3 mb s3://my-bucket

# رفع ملف
aws s3 cp file.txt s3://my-bucket/

# عرض سجلات CloudWatch
aws logs tail /aws/lambda/my-function
```

## أمثلة عملية

### ١. Launch EC2 Instance

```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-key \
  --security-group-ids sg-123456 \
  --subnet-id subnet-123456
```

### ٢. Lambda Function

```python
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('مرحباً من AWS Lambda!')
    }
```

### ٣. S3 Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```

## أفضل الممارسات

✅ استخدام IAM Roles بدلاً من Access Keys
✅ تفعيل MFA للحسابات
✅ استخدام VPC للعزل
✅ تفعيل CloudTrail للتدقيق
✅ استخدام Tags للتنظيم
✅ إعداد Budget Alerts

❌ لا تستخدم root account إلا للضرورة
❌ لا تترك security groups مفتوحة
❌ لا تخزن أسرار في الكود

---

## الكلمات المفتاحية

عربي: "AWS", "سحابة", "EC2", "Lambda", "S3"
English: "AWS arabic", "cloud computing", "amazon web services"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
