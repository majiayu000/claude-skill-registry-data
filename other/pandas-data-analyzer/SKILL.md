---
name: pandas-data-analyzer
description: >
  Pandas kütüphanesi kullanarak veri analizi, veri temizleme, keşifsel veri analizi (EDA) ve 
  görselleştirme işlemlerini gerçekleştirir. Kullanıcı .csv, .xlsx, .json dosyaları paylaştığında 
  veya "veri analizi yap", "pandas kullan", "dataframe oluştur" gibi komutlar verdiğinde bu yeteneği kullanın.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Pandas Veri Analizi Uzmanı

Bu yetenek, Python ve Pandas kütüphanesini kullanarak karmaşık veri setlerini analiz etmenize, temizlemenize ve anlamlı içgörüler çıkarmanıza yardımcı olur.

## Analiz İş Akışı

### 1. Veri Yükleme ve İlk İnceleme

Veri yüklendikten sonra her zaman şu adımları izleyin:

- Verinin ilk 5 satırını görüntüleyin (`df.head()`).
- Veri tiplerini ve eksik değerleri kontrol edin (`df.info()`).
- Temel istatistiksel özetleri çıkarın (`df.describe()`).
- Sütun isimlerini ve veri formatlarını doğrulayın.

### 2. Veri Temizleme (Data Cleaning)

Analize başlamadan önce veriyi normalize edin:

- Eksik verileri (NaN) stratejik olarak doldurun veya temizleyin.
- Yinelenen satırları kaldırın.
- Veri tiplerini düzeltin (örneğin: tarih dizelerini datetime nesnesine dönüştürme).
- Aykırı değerleri (outliers) tespit edin ve raporlayın.

### 3. Keşifsel Veri Analizi (EDA)

Verideki kalıpları bulun:

- `groupby()` ve `pivot_table()` kullanarak veriyi özetleyin.
- Değişkenler arasındaki korelasyonu inceleyin.
- Önemli trendleri ve sapmaları belirleyin.

### 4. Görselleştirme

Bulguları görselleştirirken `matplotlib` veya `seaborn` kullanın:

- Dağılımlar için Histogram veya Box Plot.
- İlişkiler için Scatter Plot.
- Zaman serileri için Line Plot.
- Kategorik karşılaştırmalar için Bar Plot.

## Uygulama Kuralları

- **Türkçe Raporlama:** Analiz sonuçlarını ve yorumları her zaman Türkçe olarak sunun.
- **Kod Kalitesi:** Yazılan Python kodlarının temiz, yorumlanmış ve PEP 8 kurallarına uygun olmasını sağlayın.
- **Performans:** Büyük veri setleri için vektörel operasyonları tercih edin, `for` döngülerinden kaçının.
- **Hata Yönetimi:** Dosya okuma veya veri tipi dönüşümlerinde `try-except` blokları kullanarak hataları yönetin.

## Örnek Kullanım

### Senaryo: Satış Verisi Analizi

Kullanıcı bir `sales.csv` dosyası verdiğinde:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Veriyi Yükle
df = pd.read_csv('sales.csv')

# 2. Temel Bilgiler
print(df.info())

# 3. Analiz: Aylık Toplam Satış
df['Date'] = pd.to_datetime(df['Date'])
monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()

# 4. Görselleştirme
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='bar')
plt.title('Aylık Toplam Satışlar')
plt.show()
```

## Dikkat Edilmesi Gerekenler

- Bellek sınırlarını zorlamamak için çok büyük dosyalarda `chunksize` kullanmayı değerlendirin.
- Veri setinde gizli kalmış (hidden) eksik değerleri (boş stringler, "NULL" metinleri vb.) kontrol edin.
- Analiz sonunda mutlaka yönetici özeti (Executive Summary) niteliğinde 3-4 maddelik Türkçe içgörü paylaşın.
