---
name: arabic-gcp
name_ar: جوجل كلاود
description: Master Google Cloud Platform in Arabic
description_ar: إتقان منصة جوجل السحابية بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان خدمات Google Cloud Platform باللغة العربية.

## الخدمات الأساسية

### ١. الحوسبة

| الخدمة | الوصف |
|--------|-------|
| **Compute Engine** | VMs افتراضية |
| **App Engine** | PaaS |
| **Cloud Functions** | Functions as a Service |
| **GKE** | Kubernetes Engine |
| **Cloud Run** | حاويات managed |

### ٢. التخزين

| الخدمة | الوصف |
|--------|-------|
| **Cloud Storage** | تخزين كائنات |
| **Filestore** | تخزين ملفات |
| **Persistent Disk** | أقراص VMs |
| **Archive** | أرشفة باردة |

### ٣. قواعد البيانات

| الخدمة | الوصف |
|--------|-------|
| **Cloud SQL** | MySQL/PostgreSQL/SQL Server |
| **Firestore** | NoSQL |
| **Bigtable** | NoSQL كبير |
| **Memorystore** | Redis/Memcached |
| **BigQuery** | Data Warehouse |

### ٤. الذكاء الاصطناعي

| الخدمة | الوصف |
|--------|-------|
| **Vertex AI** | منصة ML |
| **Vision AI** | معالجة صور |
| **Natural Language** | معالجة نص |
| **Speech-to-Text** | تحويل صوت لنص |
| **Translation** | ترجمة |

## gcloud Commands

```bash
# مصادقة
gcloud auth login

# إعداد مشروع
gcloud config set project PROJECT_ID

# إنشاء VM
gcloud compute instances create my-vm \
  --machine-type e2-micro \
  --image-family debian-11

# إنشاء GKE cluster
gcloud container clusters create my-cluster \
  --num-nodes 3

# Deploy تطبيق
gcloud app deploy

# عرض logs
gcloud logging read "resource.type=gce_instance"
```

## أفضل الممارسات

✅ استخدم Projects للعزل
✅ استخدم Service Accounts
✅ فعل Cloud Monitoring
✅ استخدم IAM بحد أدنى
✅ راقب التكلفة

---

## الكلمات المفتاحية

عربي: "جوجل كلاود", "GCP", "سحابة"
English: "gcp arabic", "google cloud", "cloud platform"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
