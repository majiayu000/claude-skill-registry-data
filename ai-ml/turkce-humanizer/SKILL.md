---
name: turkce-humanizer
description: Türkçe metinlerden AI-üretimi yazım imzalarını temizler ve metnin registeri uygunsa insan Türkçesinin ritim imzalarını yerleştirir. "Türkçeleştir," "AI kokusunu at," "bu Türkçe metni doğallaştır," "humanize et" gibi ifadelerle veya AI-üretimi görünen Türkçe paragraf sunulduğunda tetiklenir.
---

# Türkçe Humanizer

Bu skill iki fazlı çalışır. **Faz 1** metinden AI-üretimi yazım imzalarını çıkarır. Koşulsuzdur, her metne uygulanır. **Faz 2** metnin registeri uygunsa insan Türkçesinin ritim imzalarını yerleştirir. Koşulludur, metnin türüne göre değişir.

İki faz birlikte metni AI-steril olmaktan çıkarır ve canlı hâle getirir. Amaç sadece AI kokusunu atmak değil, insan yazısının nefesini geri vermek. Ama metnin türü izin verdiği ölçüde. Bir KVKK sözleşmesine konuşma dili girmez, bir gazete yazısına girer.

## İŞLEM BAŞLAMADAN ÖNCE — Zorunlu İlk Adımlar

**BU BÖLÜM ATLANAMAZ.** Skill herhangi bir sinyal tarama veya temizleme işlemine başlamadan önce şu iki adımı **sırayla** uygular. Skill'in ana akışına girmeden önce bu iki adım tamamlanmalı.

### Adım 1 — Register Teşhisi

Metni oku, hangi register'da olduğunu belirle (beş kategoriden biri, aşağıda tanımlı). Kullanıcı baştan register belirtmişse ("bu blog yazısı," "bu akademik metin") bu adımı atla. Belirtmemişse teşhisini kullanıcıya bildir:

> "Bu metni [register adı] olarak görüyorum. Onaylıyor musun?"

Kullanıcı düzeltirse kabul et.

### Adım 2 — Profil Sorgusu (Sohbet-İçi)

Register teşhisi netleştikten sonra, **temizleme işlemine başlamadan önce**, profil sorgusunu yap.

**Register profil-uyumsuz (hukuki-idari, akademik-kurumsal):** Bu adımı atla, Adım 3'e geç. Profil sorulmaz.

**Register profil-uyumlu (analitik-gazetecilik, deneme-blog, edebi-yaratıcı):** BU SORUYU MUTLAKA SOR, atlanamaz.

Sohbette bu soru daha önce sorulmadıysa:

> "Bu metin profil uygulamaya uygun bir register'da. Senin yazım ritmini de katmamı istersen kendi yazdığın 2-3 kısa metin paylaş, profilini bu sohbet boyunca kullanayım. İstemiyorsan devam edebilirim."

Kullanıcının cevabını bekle. Cevaba göre:

- **Kullanıcı örnek metin yapıştırırsa:** Verilen örneklerden yazarın nefes uzunluğunu, kavram üretme kalıplarını, tercih ettiği bağlaçları ve ritmi analiz et. Bu analizi kendi hafızanda tut (sohbet bağlamında). Sonra Adım 3'e geç, temizleme sırasında bu profili uygula.

- **Kullanıcı "istemiyorum" veya benzeri derse:** Profilsiz devam et, Adım 3'e geç.

**KRİTİK MİMARİ NOT:** Bu skill Claude Desktop'ın sandbox ortamında da çalışır. Dosya sistemine erişim gerekmez. Profil dosya olarak saklanmaz, sadece o sohbet boyunca hafızada tutulur. Yeni sohbette baştan sorulur — bu tasarım gereğidir, hata değildir.

### Adım 3 — İşleme Başla

Adım 1 ve 2 tamamlandıktan sonra Faz 1 ve Faz 2 uygulanır.

## Beş Mutlak Yasak (Register-Bağımsız)

Bu beş yasak her metinde, her register'da, her koşulda uygulanır. TDK'ya uygun olsa bile uygulanır. Faz 1'den önce, Faz 2'den önce, her şeyden önce.

**1. Uzun çizgi yasak.** Cümle içinde uzun çizgi (—) kullanılmaz. Ara söz için virgül kullanılır ya da cümle bölünür. Konuşma çizgisi olarak diyalog başında bile bu skill'in çıktısında yer almaz. Uzun çizgi Türkçe AI çıktısının en belirgin imzalarından biridir.

**2. Noktalı virgül yasak.** Hiçbir yerde noktalı virgül kullanılmaz. TDK'ya göre doğru bir kullanım olsa bile kullanılmaz. Noktalı virgül gördüğün her yerde cümleyi iki ayrı cümleye böl. Noktalı virgül AI'nin İngilizce "; also / ; however" mantığını Türkçe'ye zorla çevirdiği yerdir.

**3. Yarım cümle yasak.** Fragment cümle üretmez. "Bitti." "Kalakaldı." tarzı tek kelimelik veya yarım hissi veren cümleler yazmaz. Cümle her zaman özne ve yüklem yapısını taşır. Kısa cümle üretebilir, ama tam cümle olarak.

Tam cümle örneği (izinli): "İtibarı da bu tutumdan geldi."
Yarım cümle örneği (yasak): "Bu tutumdan."

**4. Bağlaçla açılan izole cümle yasak.** "Ama şu oldu." "Ancak durum farklıdır." gibi bağlaçla açılıp tek başına duran cümleler üretmez. Bağlaç ya cümlenin içinde kalır ya da iki cümle birleştirilir.

Yasak örneği: "Türkiye savaşa girmedi. Ama savaşın ekonomisini yaşadı."
İzinli hâli: "Türkiye savaşa girmedi ama savaşın ekonomisini yaşadı."

**5. Karşıtlık bağlaçlarından önce virgül yasak.** "Ama," "ancak," "fakat," "lakin," "yalnız" (bağlaç anlamında) gibi karşıtlık bağlaçlarından *önce* virgül konulmaz. Bu İngilizce'nin "but" ve "however" öncesi zorunlu virgül kuralının Türkçe'ye zorla çevirisidir. TDK'ya göre de yanlıştır. AI çıktısının en belirgin sözdizim imzalarından biridir.

Yasak örneği: "Plan hazırdı, ancak uygulamada aksadı."
İzinli hâli: "Plan hazırdı ancak uygulamada aksadı."

Yasak örneği: "Türkiye reform yaptı, ama sonuç sınırlı kaldı."
İzinli hâli: "Türkiye reform yaptı ama sonuç sınırlı kaldı."

Bu beş yasağın hiçbiri register'a bağlı değildir. Her metne uygulanır. Detaylı TDK gerekçeleri için `docs/tdk-referanslari.md` dosyasına bakılır (ama skill bu dosyaya bakmadan da yasakları uygular).

## Pozitif Yön — Güçlü Cümle Hedefi

Skill kısaltıcı değil, güçlendiricidir. Hedef Türk edebiyatının ve akademisinin yerleşik cümle mimarisidir. Örnek referanslar `examples/guclu-cumleler.md` dosyasında tutulur.

Güçlü cümlenin üç niteliği:

- **Bir şey iddia eder.** Cümle bittiğinde okur bir şey biliyor olmalı. AI cümleleri kaçamaklı biter, güçlü cümle durur. "İnsan ruhunun yarası dikiş tutmaz." (Ahmet Ümit) — cümle bittiğinde bir iddia elimizde.
- **Tam bir yapıdadır.** Özne ve yüklem yerindedir. Uzunluk önemli değil, tamlık önemli. Kısa da olabilir uzun da.
- **Ritmi vardır.** Cümlenin içinde bir nefes akışı vardır. Bu ritim virgül sayısıyla ölçülmez, cümlenin okuma sesiyle ölçülür.

Referans yazarlar: Ahmet Hamdi Tanpınar, Ayfer Tunç, Barış Bıçakçı, Ahmet Ümit, İlber Ortaylı, Kemal Karpat, Çağlar Keyder. Akademik ritim için ek referans: Marcus, Aksoy. Skill bir cümle üretirken bu yazarların cümle mimarisine bakar. Zorlama taklit değil, kalıp öğrenimi.

## Yapı Koruma

Metnin yapısını değiştirme. Bu beş yasaktan sonra, her şeyden önce uygulanır.

- Madde listeleri liste olarak kalır. Paragrafa çevirme.
- Başlık hiyerarşisi korunur.
- Tablolar tablo olarak kalır.
- Blok alıntılar blok olarak kalır.
- Kod blokları kod olarak kalır.
- Belge şablonuna ait yapısal alanlar yerinde bırakılır.

Skill'in işi cümle içi ve paragraf içi dil düzeltmesi. Belge iskeletine dokunma. Kullanıcı açıkça "yapıyı da değiştir" veya "paragrafa çevir" demedikçe.

## Register Teşhisi

Metni işlemeden önce hangi ailede olduğunu belirle. Beş register kategorisi:

| Register | Örnek metin türleri | Faz 2 uygulaması | Profil sorgusu |
|----------|--------------------|--------------------|-----------------|
| **Hukuki-idari** | Sözleşme, KVKK, tebliğ, kanun taslağı | Yok | Yok |
| **Akademik-kurumsal** | Tez, akademik makale, resmi rapor | Kısıtlı: sadece cümle varyansı ve öz-düzeltme | Yok |
| **Analitik-gazetecilik** | Haber, analiz, brifing, düşünce kuruluşu raporu | Tam, konuşma bağlaçları hariç | Var |
| **Deneme-blog** | Deneme, köşe yazısı, blog, sosyal medya uzun formatı | Tam | Var |
| **Edebi-yaratıcı** | Roman, öykü, denemeye yakın anlatı | Tam artı duyusal detay ve zaman kipi | Var |

Metni okuduğunda ilk seçim skill'e ait değil, kullanıcıya doğrulatılır (İşlem Başlamadan Önce, Adım 1'e bakılır). Sınır durumlarda (analitik-gazetecilik ile deneme-blog arasında sıkışan metinler gibi) detaylı ayrım için `docs/register-detayli.md` dosyasına bakılabilir.

## Yazar Profili Sistemi

Register profil-uyumluysa (analitik-gazetecilik, deneme-blog, edebi-yaratıcı), skill yazarın kendi imzasını da hesaba katar. Profil sorgusu işlem başında yapılır (İşlem Başlamadan Önce, Adım 2'ye bakılır).

### Sohbet-içi profil (v3.2 mimarisi)

Profil bir dosyada saklanmaz. Kullanıcı sohbetin başında (skill sorunca) kendi yazdığı 2-3 kısa metni yapıştırır. Skill bu örneklerden şunları analiz eder:

- **Nefes uzunluğu:** yazarın tipik cümle uzunluğu, kısa-uzun varyansı.
- **Bağlaç tercihleri:** "ama" mı "ancak" mı, "yani" mı "diğer bir ifadeyle" mi.
- **Kavram üretme kalıpları:** yazar kendi kavramları üretiyor mu (mesela "masada kazanılan egemenlik" gibi), yoksa yerleşik terimler mi kullanıyor.
- **Ritim imzaları:** cümle sonu kararlılığı, öznenin cümle içi konumu, devrik cümle sıklığı.
- **Karakteristik kelime seçimleri:** yazarın sık kullandığı bağlaçlar, geçişler, yer tutucular.

Bu analiz o sohbetin hafızasında kalır. Skill sonraki metinleri temizlerken bu profili göz önünde tutar.

### Sohbet-içi profilin kapsamı

Profil oluşturulduktan sonra o sohbetteki **tüm profil-uyumlu metinlerde** kullanılır. Kullanıcı yeni metin attığında tekrar profil sorulmaz — mevcut profil kullanılır.

Yeni sohbette (yeni bir Claude penceresi/konuşması) profil sıfırlanır. Baştan sorulur. Bu tasarım gereğidir çünkü Claude Desktop sohbetler arası kalıcı hafıza tutmaz.

### Yazar imzası koruma

Profil aktifse, skill AI-sinyali ile yazar-imzası ayrımını profil örneklerine bakarak yapar. Örnek: yazar profil örneklerinde sık kavram üretimi gösteriyorsa, skill bu tür ifadeleri AI-sinyali sanıp temizlemez. Yazar "ancak" tercih ediyorsa skill "yalnızca" yerine "ancak" kullanır.

### Profil yoksa ne olur

Kullanıcı "istemiyorum" derse skill profilsiz devam eder. Bu durumda skill genel Türkçe akademik-analitik ritim referanslarını (Tanpınar, Ortaylı, Karpat gibi) kullanır. Sonuç yine iyi olur, sadece kullanıcının kendi imzası korunmaz — genel iyi Türkçe hedefine göre çalışır.

## Kullanıcıya Danışma Protokolü

Skill kendi kararının sınırında olduğu her yerde kullanıcıya açık soru sorar. Üç durumda:

- Bir sinyalin AI-imzası mı yoksa yazar tercihi mi olduğu belirsiz.
- Bir bağlaç veya kalıp register'da sınırda. Örnek: "Ne var ki" analitik-gazetecilik register'ının sınırında bir bağlaçtır. Skill "bu register'da 'Ne var ki' mi 'Ama' mı tercih edersin?" diye sorar.
- Metonim ile eş anlamlı rotasyonu ayrımı belirsiz. Örnek: "Türkiye / Ankara / cumhuriyet" aynı özne için farklı adlar değildir, metonimdir (Türkiye = ülke, Ankara = hükümet merkezi, cumhuriyet = rejim). Skill emin değilse sorar.

Sorular kısa ve tek seçim olur. Kullanıcı "hepsini sen bilirsin" derse skill kendi varsayılan kararını uygular.

## Faz 1 — AI Dokunuşlarını Çıkarma (Koşulsuz)

Faz 1 üç katmandan oluşur: **mutlak yasaklar** (yukarıda tanımlı), **baskın sinyaller** ve **ikincil sinyaller**. Baskın sinyaller Türkçe AI metninin en belirgin fenotipleridir. Üçü veya daha fazlası bir metinde varsa metin ağır AI-imzalıdır. İkincil sinyaller destekleyici işaretlerdir.

### Baskın Sinyaller

#### Sinyal 1 — Noktalama Enflasyonu

Türkçe noktalama TDK'ya göre kısıtlıdır. AI, İngilizce noktalama mantığını Türkçe'ye zorla çevirir.

**1a. Uzun tire.** Mutlak yasak (yukarıda tanımlı). Cümle içi uzun tire virgüle çevrilir veya cümle bölünür.

**1b. Noktalı virgül.** Mutlak yasak. TDK-uygun olsa bile kaldırılır. Cümle ikiye bölünür (bağlaçla açılan izole cümle üretmeden).

**1c. İki nokta üst üste açıklama modu.** Cümle içi mini açıklama için iki nokta kullanma. AI "X: Y" yapıları üretir. Türkçe'de iki nokta örnek/açıklama gerektiren cümle sonuna veya konuşma öncesine gelir.

- Alarm eşiği: bir paragrafta iki veya daha fazla cümle-içi iki nokta.
- Onarım: iki nokta üst üsteyi kaldır, iki cümle yap veya virgülle bağla.

**1d. Bağlaç "ki" bitişik yazma.** "bu ki," "şu ki," "durum şu ki" yapıları ayrı yazılır. Sadece kalıplaşmış "belki, çünkü, mademki, meğerki, oysaki, sanki, hâlbuki" bitişiktir.

- Onarım: bitişik "ki"leri ayır.

**1e. Slash-ayırıcı.** "kullanıcı/müşteri/istemci" yapısı Türkçe değildir. Virgül ve "veya" ile değiştirilir.

- Alarm eşiği: metinde iki veya daha fazla slash-ayırıcı.
- Onarım: "A, B veya C" yapısına çevir.

**1f. Karşıtlık bağlacı öncesi virgül.** Mutlak yasak 5 (yukarıda tanımlı). "Ama," "ancak," "fakat," "lakin," "yalnız" bağlaçlarından önce virgül gördüğün her yerde kaldır. İngilizce "but/however" öncesi zorunlu virgül kuralının Türkçe'ye zorla çevirisidir.

- Alarm eşiği: metinde bir örnek yeter.
- Onarım: bağlaç öncesindeki virgülü sil, cümle bütün olarak akmaya bıraksın.

#### Sinyal 2 — Cümle Monotonluğu

İnsan yazısı burstiness taşır. Kısa, orta ve uzun cümleler karışıktır, ritim nefes alır. AI Türkçesi ise orta uzunlukta cümlelerde takılır — hepsi 18-25 kelime arası, arada kısa tam cümle yok, arada uzun analitik yok.

- Alarm eşiği: paragrafta cümle uzunluğu standart sapması düşük (%30 altı) ve ortalama 22+ kelime.
- Diğer sinyal: hiç 8 kelimeden kısa tam cümle yok.

**Onarım:** En uzun cümleyi böl, ortasına kısa bir tam cümle yerleştir. Yarım cümle üretme (mutlak yasak 3). Kısa cümle özne ve yüklem taşır.

#### Sinyal 3 — Kalıp Tekrarı

AI belirli yapıları tekrar tekrar kullanır. Üç alt kalıp:

**3a. "-mektedir/-maktadır" salgını.** Bir paragrafta dört veya daha fazla "-mektedir/-maktadır" yüklem varsa alarm. Doğal Türkçe akademik yazı bu eki %20-25 oranında kullanır, diğer zaman kipleriyle karışık.

- Onarım: yüklem çeşitliliği ekle — geçmiş zaman ("oldu, çıktı"), geniş zaman ("olur, çıkar"), aktif ses.

**3b. Bürokratik bağlaç yığını.** "Bu bağlamda," "söz konusu," "öte yandan," "bunun yanı sıra," "bu doğrultuda," "bu çerçevede" — bir metinde toplam üç veya daha fazla kullanım alarm.

- Onarım: bürokratik bağlaçları gerçek mantıksal bağlarla değiştir ("Çünkü," "Nitekim," "Oysa"). Ama bağlaçlar cümle içinde kalır, izole cümle açmaz (mutlak yasak 4).

**3c. AI kapanış klişeleri.** "Kritik bir rol oynamaktadır," "hayati bir önem taşımaktadır," "önemli bir rol üstlenmektedir," "vazgeçilmez bir hale gelmiştir" — bir metinde iki veya daha fazla kullanım alarm. Özellikle paragraf sonlarında.

- Onarım: boş kapanışları sil, paragraf bir önceki cümlede bitsin.

#### Sinyal 4 — "Sadece X Değil, Aynı Zamanda Y" Ailesi

İngilizce'nin "It's not just X, it's Y" retorik hamlesi Türkçe'ye zorla çevrilmiş. AI'nin en belirgin retorik imzalarından biri.

Varyantlar:
- "Sadece X değil, aynı zamanda Y"
- "Yalnızca X söz konusu değildir; Y de..."
- "X olmakla birlikte, Y niteliğini de taşımaktadır"
- "X'in ötesinde, Y boyutu göz ardı edilmemelidir"
- "Salt X değil; bir Y meselesi"
- "değil, yalnızca Y"
- "değil, sadece Y"
- "değil, sırf Y"
- "X değil Y" (kısa form, aynı retorik)

Alarm eşiği: bir metinde bir örnek.

**Onarım:** Gerçek mantıksal bağı bul. Üç seçenek:
- "Hem X hem Y" yapısına çevir (bu daha doğal Türkçe)
- İki bağımsız cümle yap (ikinci cümle bağlaçla açılmasın, mutlak yasak 4)
- Bağı tamamen kaldır, sadece Y'yi bırak (X gereksizse)

#### Sinyal 5 — Boş Övgü ve Boş Kapanış

**5a. Boş değerlendirici sıfat kümesi:** "eşsiz," "benzersiz," "paha biçilmez," "zengin bir mozaik," "çok boyutlu," "hayati," "kritik," "adeta bir zaman kapsülü," "vazgeçilmez bir ritüel."

- Alarm eşiği: bir paragrafta iki veya daha fazla örnek.
- Onarım: sıfatı sil, isim başlı kalsın. Veya somut örnekle değiştir.

**5b. Boş değerlendirici kapanış:** Paragraf sonu bilgi taşımayan bir değerlendirmeyle biter.

- Alarm eşiği: her paragrafın bu tür klişeyle bitmesi.
- Onarım: boş kapanışları çıkar, paragraf bir önceki cümlede bitsin.

### İkincil Sinyaller

Bu sinyaller tek başına AI-imzası kanıtı değildir ama baskın sinyallerle birlikte görüldüğünde şüpheyi güçlendirir.

**Sinyal 6 — "Adeta" ve "sanki" bağımlılığı.** Somut örnek eksikliğini vague benzetmeyle örtme.
- Onarım: benzetmeyi somut örnekle değiştir. Somut örnek yoksa cümleyi sil.

**Sinyal 7 — Zorlama üçlü liste.** Üç öğe arasında gerçek fark yoksa dolgu.
- Onarım: bir öğeye indir veya üçünden en spesifik olanı seç.

**Sinyal 8 — Devrik cümle yokluğu.** Doğal Türkçe kimi zaman devrik kurar, LLM Türkçesi hiç kurmaz.
- Onarım: uygun bir cümlede yüklemi öne çek. Zorlama yapma.

**Sinyal 9 — Register kayması.** Aynı paragrafta teknik/bürokratik başlayıp aniden estetik-emotif kelimelere kayma.
- Onarım: baştaki register'ı belirle, o katmanda kal.

**Sinyal 10 — Somut anchor eksikliği.** İnsan yazarlar soyut iddiayı hemen somut örnek, tarih, isim ile takip eder.
- Onarım: soyut iddiaya somut örnek ekle (kullanıcıdan iste veya cümleyi sil). Uydurma anchor ekleme.

**Sinyal 11 — Pasif yapı bağımlılığı.** Cümlelerin çoğu pasif çatıda.
- Onarım: mümkün olan yerde aktif çatıya çevir.

**Sinyal 12 — İngilizce vurgu-doldurucuları ve Türkçe AI-vurgusu.** Türkçe cümle yapısı vurguyu dizilim ve tonlama ile yapar, kelime eklemekle değil.

Aile:
- "tam da" (İng. precisely)
- "tam anlamıyla" (İng. literally, truly)
- "gerçekten de" (İng. indeed)
- "aslında da" (İng. in fact)
- "kesinlikle" (dolgu olarak, İng. definitely)
- "esasen" (İng. essentially)
- "nihayetinde" (İng. ultimately)
- "bir bakıma" (İng. in a way)
- "gerçek anlamda" (İng. in a real sense)
- "işte" (cümle başında dolgu olarak)
- "işte tam da"
- "işte bu" (cümle başında dolgu olarak)
- "böylece" (mantık bağı taşımıyorsa)
- "sonuç olarak" (özet değil dolgu ise)

- Alarm eşiği: metinde iki veya daha fazla örnek.
- Onarım: sil. Cümlenin anlamı zaten korunuyor.

**Sinyal 13 — Eş anlamlı rotasyonu.** AI aynı özneye tek paragrafta üç ayrı ad verir.
- Alarm eşiği: bir paragrafta aynı özneye üç veya daha fazla ayrı ad.
- Onarım: bir ad seç, o adı kullan.
- Not: Metonim (Türkiye / Ankara / cumhuriyet gibi) eş anlamlı değildir. Ayrım belirsizse kullanıcıya sor.

**Sinyal 14 — Fragment cümle bağımlılığı.** Mutlak yasak 3 ile örtüşür. AI cümleyi iki noktayla açıp fragment liste veya fragment tanım bırakır.
- Onarım: fragment'ı tam cümleye tamamla.

#### Sinyal 23 — Şudur/Budur Açıklama Kalıbı

AI Türkçe çıktısı "X şudur: Y" veya "Kesin olan tek şey şudur: Y" gibi açıklama kalıpları üretir. Bu İngilizce "The thing is: X" veya "What is certain is: X" kalıplarının zorla çevirisi. Türkçe akademik ve edebi gelenek bu kalıbı yaygın kullanmaz; bunun yerine tümce-içi yeniden yapılandırma yapar.

Varyantlar:
- "X şudur: Y"
- "Kesin olan tek şey şudur: Y"
- "Anlaşılan şey şudur: Y"
- "Ortaya çıkan tablo şudur: Y"
- "Söylenmesi gereken şudur: Y"
- "Bir soru ısrarla beklemekte: [soru]" (soru varyantı)
- "Şu soru gündemde: [soru]" (soru varyantı)

- Alarm eşiği: bir metinde bir örnek yeter.
- Onarım: iki nokta üst üsteyi kaldır, cümleyi "Y olan X" yapısına çevir. Türkçe'de bu yapı klasik akademik ritmin bir hamlesidir (Ortaylı, Karpat sık yapar).

Örnek onarım:
- Yasak: "Kesin olan tek şey şudur: Üçgen, eski geometrisine bir daha dönmeyecek."
- İzinli: "Üçgenin eski geometrisine dönmeyeceği kesin olan tek şey."

Soru varyantı onarımı:
- Yasak: "Yine de bir soru ısrarla beklemekte: Tahran ile Washington'ı, birbirlerini doğrudan vurmaktan kırk beş yıl boyunca alıkoyan neydi?"
- İzinli: "Tahran ile Washington'ın, birbirlerini doğrudan vurmaktan kırk beş yıl boyunca alıkoyanın ne olduğu sorusu ısrarla beklemekte."

## Faz 2 — İnsan Ritmi Enjeksiyonu (Koşullu)

Bu faz register uygunsa çalışır. Her sinyalin yanında hangi register'da aktif olduğu belirtilmiştir.

**Faz 2'nin mantığı Faz 1'in tersidir.** Faz 1'in kuralı: "eğer varsa çıkar." Faz 2'nin kuralı: "eğer yoksa yerleştir." Steril metne insan nefesi enjekte etmek için. Ama yerleştirme mutlak yasakları ihlal edemez — özellikle yarım cümle ve izole bağlaç yasağı Faz 2 sinyallerinde de geçerlidir.

### Sinyal 15 — Cümle Uzunluğu Varyansı

**Register:** Akademik-kurumsal ve üstü.

Uzun paragrafta ritim monotonsa, orta uzunlukta bir cümle daha kısa bir cümleye dönüştürülür. Kısa cümle **tam cümle** olur. Yarım cümle üretme (mutlak yasak 3).

### Sinyal 16 — Konuşma Bağlaçları

**Register:** Analitik-gazetecilik ve üstü.

"Ama," "Zaten," "Oysa," "Ne var ki," "Meğer," "Nitekim," "Hem de" — bunlar gerçek Türkçenin nefes bağları. Bürokratik "bu bağlamda / söz konusu / dolayısıyla" yerine bunlar konur. Bağlaçlar cümle içinde kalır (mutlak yasak 4).

**Profil aktifse:** Yazarın tercih ettiği bağlaç varsa (mesela yazar "ancak" kullanıyorsa) skill "yalnızca" yerine "ancak" tercih eder. Bu sohbet-içi profilin en önemli işlerinden biridir.

### Sinyal 17 — Retorik Soru

**Register:** Deneme-blog ve üstü.

Anlatıcının okura veya kendine soru sorması. İddia etmenin alternatifi.

### Sinyal 18 — Öz-düzeltme ve Yeniden İfade

**Register:** Akademik-kurumsal ve üstü.

Yazar kendi cümlesini düzeltir, geri alır, yeniden söyler.

**Öz-düzeltme sözcüklerinin yerleşimi:**

"Daha doğrusu," "aslında," "işin doğrusu," "belki de," "hayır" gibi öz-düzeltme sözcükleri iki farklı biçimde yerleştirilebilir:

1. **Ara söz olarak virgüllerle sarma:** Konuşma diline yakındır.
2. **Yeni cümle başı olarak yerleştirme:** Akademik-analitik registerde tercih edilir.

**Akademik-kurumsal ve analitik-gazetecilik registerlerinde ikinci hamle tercih edilir** — öz-düzeltme sözcüğü yeni cümle başı olur.

### Sinyal 19 — Duyusal Somut Detay

**Register:** Edebi-yaratıcı.

İnsan yazısı koku, dokunma, ses taşır. AI yazısı sadece görsel-soyut kalır. Duyusal detay skill tarafından üretilmez, kullanıcıya sorulur.

### Sinyal 20 — Zaman Kipi Kayması

**Register:** Edebi-yaratıcı.

İnsan yazısı şimdiki, geçmiş, geniş zamanı akışkan geçer.

### Sinyal 21 — Diyalog İzi

**Register:** Edebi-yaratıcı.

Anlatı içinde karakterin sesi geçer.

### Sinyal 22 — Birinci Çoğul Kullanımı

**Register:** Akademik-kurumsal ve üstü (analitik metinlerde), edebi'de hariç.

"Sanıyoruz," "görüyoruz," "araştırdığımızda." Okuru düşünme sürecine dahil eder.

## Uzun Belge Davranışı

Çok paragraflı belge (üç veya daha fazla paragraf) geldiğinde şu maker/checker deseni uygulanır:

1. **Tara.** Belgeyi paragraf paragraf oku, her paragraf için baskın sinyal yoğunluğunu ölç.
2. **Sınıflandır.** Paragrafları yüksek, orta, temiz olarak ayır.
3. **Rapor sun.** Kullanıcıya genel tablo ver, register teşhisi ve profil durumu belirt.
4. **Seçenek sun.** Tümü / bloklar halinde / sadece yüksek AI-imzalılar.
5. **Uygula ve işaretle.** Her paragrafın hangi sinyallerine dokunduğunu kısa notlarla belirt.

## Çıktı Formatı (Atlanamaz)

Skill'in her çıktısı beş bölümden oluşur. Hiçbiri atlanamaz.

**1. Tespit Raporu.** Metinde hangi baskın ve ikincil sinyaller görüldü, konumlarıyla.

**2. Sinyal Yoğunluğu.** 100 kelimeye normalize:
> "Önce: 8.4 sinyal/100 kelime. Sonra: 1.2. İyileşme: %86."

**3. Onarılmış Versiyon.** Tam metin.

**4. Değişiklik Özeti.** Kullanıcı onayı bekler.

**5. Notlar.**
- Kasıtlı tercih olabilir, dokunmadım: [varsa]
- Register kısıtı nedeniyle muhafazakâr davrandım: [varsa]
- Faz 2 uygulandı: [liste]
- **Profil durumu:** [aktif / soruldu-reddedildi / uyumsuz-register]
- **YOK olduğu için not düştüğüm şeyler:** metinde bulunması beklenip bulunmayan sinyaller.

Bu son satır bir editör hoşnutluğu ifadesidir. Yazar temiz bir metin yazmışsa bu tanınmalı.

## Sınırlar ve Etik

- Bu skill **kelime değiştirici değil, yapı değiştiricidir**.
- AI detektör atlatmak birincil amaç değil. **Doğal Türkçe** birincil amaç.
- **Yazar-özgü stilistik tercihlere saygı göster.** Profil aktifse profile bak, profil yoksa kullanıcıya sor.
- **Ağır biçimsel metinlerde tam temizleme yerine yoğunluk düşürme uygula.**
- **Metnin bilgi içeriği korunmalı.**
- **Yapı bütünlüğüne dokunma.**
- **Mutlak yasakların hiçbirinden taviz verilmez.** Uzun çizgi, noktalı virgül, yarım cümle, bağlaçla açılan izole cümle, karşıtlık bağlacı öncesi virgül skill çıktısında yer almaz.

## Referans

Türkçe noktalama kararlarında TDK Yazım Kuralları esas alınır. Ama TDK'nın izin verdiği bazı yapılar bu skill'de yasaktır (uzun çizgi, noktalı virgül). Ayrıca skill TDK'nın yanlış saydığı yapıları da yasaklar (karşıtlık bağlaçları öncesi virgül).

İnsan ritmi sinyalleri Türk edebiyatının ve akademisinin yerleşik yazarlarından çıkarıldı. Edebi referans: Tanpınar, Ayfer Tunç, Barış Bıçakçı, Ahmet Ümit. Akademik referans: Ortaylı, Karpat, Keyder, Marcus, Aksoy.

Örnek cümleler: `examples/guclu-cumleler.md`.
Detaylı gerekçeler: `docs/tdk-referanslari.md`, `docs/register-detayli.md`, `docs/mimari-kararlar.md`.

Nicel metrik ASD-STE100 standardından esinlendi. Genel humanizer mimarisi harshaneel/humanize ve makotofalcon/humanizer-ja projelerinden ilham aldı.

---

**Sürüm:** v3.2 (Ağustos 2026)

## v3.2 Değişiklik Notları

v3.1'den v3.2'ye geçişte yapılan tek büyük mimari değişiklik:

**Profil sistemi dosya-tabanlıdan sohbet-içi hale getirildi.**

v3.1'de profil `~/.claude/skills/turkce-humanizer/profiles/ben.md` dosyasında tutuluyordu. Bu Claude Code CLI'da çalışıyor ama Claude Desktop'ın sandbox ortamında çalışmıyordu — skill dosya sistemine erişemediği için profil sorgusunu atlıyordu.

v3.2'de profil dosya olarak saklanmaz. Kullanıcı sohbetin başında (skill sorunca) 2-3 kısa örnek metin yapıştırır. Skill bu örnekleri sohbet boyunca hafızasında tutar, tüm profil-uyumlu metinlerde kullanır. Yeni sohbette baştan sorulur.

Bu değişiklik skill'i Desktop, CLI ve Claude.ai platformlarının hepsinde çalışır hale getirir.

Ek olarak Sinyal 23'e soru cümlesi varyantı eklendi ("Bir soru ısrarla beklemekte: [soru]" kalıbı).
