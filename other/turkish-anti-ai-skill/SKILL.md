---
name: turkish-anti-ai-skill
description: Türkçe metni insan eliyle yazılmış gibi doğal yazar veya onarır. Kullanıcı Türkçe bir metin için "insanileştir", "humanize et", "AI hissiyatını sil" veya "doğal Türkçeye çevir" dediğinde, metinde çeviri kokusu ya da TDK hatası denetimi istediğinde, Türkçe blog, makale, kurumsal yazı, sosyal medya içeriği veya teknik doküman yazarken kullan.
license: MIT
metadata:
  author: yucezerey
  version: "1.1.0"
---

# Turkish Anti-AI Skill (Doğal Türkçe ve Anti-Slop Mimari Kılavuzu)

Bu yetenek, Büyük Dil Modellerinin (LLM) İngilizce ağırlıklı eğitim verisi ve RLHF süreçleri yüzünden ürettiği "Yapay Zekâ Türkçesini" (kelimeleri Türkçe ama cümle iskeleti İngilizce olan, mekanik, şişirilmiş ve tekdüze metinleri) doğal, nefes alan ve TDK kurallarına tam uyumlu insan Türkçesine dönüştürür.

Detaylı dilbilimi kuralları ve sözlük tabloları için bu dizindeki referans dosyalarını oku:

- `references/sentaks-ve-morfoloji.md`: Türkçe cümlenin geometrisi (öge dizilimi, bilgi yapısı, gömme derinliği), sola dallanma, ulaç sistemi, vurgu yuvası, `-DIr` ile `-mAktAdIr` ayrımı, zamir düşürme, adlaştırma zincirleri ve kof yardımcı fiil dönüşümleri.
- `references/ai-turkcesi-sozlugu.md`: Tier-1 (kesin AI ifşaları), Tier-2 (bürokratik bağlaçlar) ve Tier-3 (SaaS/pazarlama çeviri kalıpları) sözlüğü.
- `references/tdk-ve-noktalama.md`: 5 mutlak noktalama yasağı, TDK birleşik/ayrı kelimeler ve yabancı teknik terimlerin Türkçe okunuşa göre ek uyumu.
- `references/register-ve-ornekler.md`: 5 register × 9 üslup boyutu matrisi ve uçtan uca Before/After dönüşüm çiftleri.

## Temel İlkeler

1. **Kelime Değiştirmek Yetmez, Cümle Mimarisini Yeniden Kur:** Türkçe sondan eklemeli (agglutinative) ve sola dallanan (left-branching) bir dildir. İngilizcenin sağa dallanan SVO iskeletini koruyarak yalnızca eşanlamlı kelime değiştirmek AI etkisini silmez. Önce cümle mimarisini onar.
2. **Olgusal Sadakat Kilidi (Anti-Fabrication Lock):** Onarım (`rewrite`) modunda kaynak metinde bulunmayan hiçbir sayı, tarih, özel isim, kişisel anekdot veya nedensellik bağı uydurma. "İnsan gibi görünmek" için yalan söyleme, yalnızca mevcut bilginin ifade edilişini doğallaştır. Bir klişeyi silince yerine somut bilgi gerekiyorsa ve bu bilgi kaynakta yoksa onu uydurma. Ya klişeyi sadeleştirip olduğu kadarını söyle ya da köşeli yer tutucu bırak (`[somut veri: kaç belge?]`) ve kullanıcıya sor. Referans dosyalarındaki örnekler bu biçimi kullanır. Sayı, miktar ve kesinlik derecesi de bilgidir. "Birçok" yerine "yüzlerce", "artırabilir" yerine "artırır" yazmak da uydurmadır.
3. **Register (Bağlam) Dozajı:** Her metin aynı tonda yazılmaz. Akademik makalede `-mAktAdIr` eki doğalken, blog veya kurumsal bültende yapay durur. İşleme başlamadan önce metnin register'ını belirle.
4. **Sınırları Olan Kurallar:** Sınırı olmayan her kural yeni bir yapay tike dönüşür. Devrik cümle, söylem parçacığı (`işte`, `zaten`, `hani`) veya kısa cümle kullanımını kotaya bağlama ve silme testinden geçmeyen hiçbir üslup aracını metinde tutma.

## Çalışma Modları

Kullanıcı isteğine göre aşağıdaki üç moddan birini seç:

- **Onarım Modu (`rewrite` - Varsayılan):** Mevcut bir Türkçe metni veya çeviriyi alır, olgusal sadakati %100 koruyarak AI kalıplarını temizler ve cümle mimarisini Türkçeleştirir.
- **Üretim Modu (`write`):** Verilen bir konu veya taslaktan sıfırdan Türkçe metin üretir. Kompozisyon ve cümle kararlarını ilk cümleden itibaren İngilizce düşünmeden, doğrudan Türkçe kurar.
- **Denetim Modu (`audit`):** Metni yeniden yazmaz. Metindeki P0 (Kesin AI İfşası), P1 (Yapısal Çeviri Kokusu) ve P2 (Ritim/Noktalama Kusuru) sinyallerini alıntılayarak raporlar.

## Adım Adım İş Akışı (Mark -> Draft -> Audit -> Deletion Test)

### Adım 1: Register ve Üslup Kalibrasyonu

Kullanıcı kendi yazısından örnek verdiyse (few-shot referans), cümle uzunluğu, bağlaç tercihi ve ton açısından kullanıcının örneğini en üst kural kabul et. Örnek yoksa metni şu 5 register'dan birine ata (`references/register-ve-ornekler.md`):

| Register | Kompozisyon Müdahalesi | Cümle Mimarisi | `-DIr` / `-mAktAdIr` | Devrik Cümle ve Parçacık |
| :--- | :--- | :--- | :--- | :--- |
| **Blog / Deneme / Sosyal Medya** | Tam (Sahne ile başla, ilan etme) | Tam (Ulaç, özne düşürme, `-mIş`) | `-mAktAdIr` sil, ad cümlesinde `-DIr` seyrek | Serbest ama seyrek (400 kelimede 2-3 devrik yol gösterici bir tahmin) |
| **Teknik Doküman / Mühendislik** | Orta (Doğrudan probleme gir) | Tam (Sola dallanma, ulaç, net yüklem) | `-mAktAdIr` yerine `-Ar/-Ir` veya `-(I)yor`, tanım cümlesinde `-DIr` korunur | Devrik yok, parçacık çok az |
| **Kurumsal / İş İletişimi / SaaS** | Orta (Tezi ilk cümlede söyle) | Tam (Kurumun kendi eylemini etkene çevir, kof fiili at) | `-mAktAdIr` yalnızca resmî duyuruda, `-DIr` tanımda | Devrik yok, doğal ve doğrudan |
| **Akademik / Resmî / Hukuki** | Kapalı (Belge iskeletini koru) | Sola dallanma, ulaç ve vurgu yuvası | Korunur, tekrarı azaltılır (100 kelimede yaklaşık 0,5-2,5, art arda üç cümle aynı ekle bitmez, geniş zamanla nöbetleşe) | Kesinlikle yasak |
| **Edebî / Anlatı** | Tam (Ritim ve imge odaklı) | Tam (Nefes uzunluğu varyasyonu yüksek) | `-mAktAdIr` sil, `-DIr` anlatı akışında seyrek | Anlatı ritmine göre doğal |

### Adım 2: Üç Katmanlı Dönüşüm

#### Katman 1: Kompozisyon ve Retorik Kalıplar (P0 Sinyalleri)

- **Sahneleme Yerine Doğrudan Söyle:** "Bu yazıda X konusunu ele alacağız", "Günümüzün hızla değişen dünyasında" gibi sahneleme girişlerini silip konunun kendisine gir.
- **Negatif Paralellikleri Kaldır:** "Sadece X değil, aynı zamanda Y", "Bu bir A değil, bir B'dir" ve "X ile değil, Y ile" gibi tüm negatif paralellik kalıplarını olumlu ve net bir yargıya dönüştür (detaylar: `references/ai-turkcesi-sozlugu.md`).
- **Tek Satırlık Dramatik Kapanışları ve Özet Kuyruklarını Sil:** Paragraf sonlarındaki "İşte asıl fark burada ortaya çıkıyor.", "Sonuç olarak X'in önemi yadsınamaz." gibi ders veren kapanışları kes.
- **Üçlü Liste (Rule of Three) Otomatizmini Kır:** Fikirleri sürekli üçlü sıfat veya üçlü örnek grupları ("hızlı, güvenilir ve ölçeklenebilir") hâlinde dizme. Gerçekten kaç öge varsa o kadarını sırala.
- **Kalın Etiketli Madde İmlerini (`**Başlık:** Açıklama`) Çöz:** Gerekmedikçe her paragrafı madde imine çevirme. Liste şartsa kalın etiket + iki nokta şablonu yerine yalın cümle kur.

#### Katman 2: Türkçe Cümle Mimarisi ve Sentaks (P1 Sinyalleri)

Detaylı kurallar ve örnekler için `references/sentaks-ve-morfoloji.md` dosyasını oku:

- **Öge Dizilimi ve Bilgi Yapısı:** Türkçe baş sonda bir dildir. Cümle başına bilinen konuyu, yüklemin hemen önüne yeni ya da vurgulanan bilgiyi koy. Belirtisiz nesneyi yüklemden ayırma (*"Ahmet'e rapor gönderdim"*). İngilizce yarık cümleyi (*"Bunu mümkün kılan şey X'ti"*) odağı yüklem önüne alarak çöz (*"Bunu X mümkün kıldı"*).
- **Sola Dallanma (Left-Branching):** Niteleyicileri ve yan cümleleri baş ismin arkasına ya da `ki` ile cümle sonuna takma, sıfat-fiillerle (`-(y)An`, `-DIk`, `-(y)AcAk`) ismin önüne al (*"Bir sistem kurduk, bu sistem verileri tarıyor"* -> *"Verileri tarayan bir sistem kurduk"*). Ama bir adın önüne ikiden fazla iç içe yan cümle yığma, o durumda cümleyi böl.
- **Refleks `ve` Yerine Ulaç (Zarf-Fiil) Sistemi:** Sıralı eylemleri mekanik `ve` veya `ve sonra` ile bağlamak yerine Türkçenin ulaç eklerini (`-(y)Ip`, `-(y)IncA`, `-DIkçA`, `-(y)ArAk`, `-mAdAn`) kullan (*"Veriyi çektik ve işledik"* -> *"Veriyi çekip işledik"*). Ulaçlı yan cümlenin söylenmeyen öznesi ana cümlenin öznesi sayılır. Özneler farklıysa ulaç kullanma.
- **`-mAktAdIr` ile `-DIr`'ı Ayrı Ele Al:** `-mAktAdIr` akademik ve resmî register dışında `-(I)yor` ya da `-Ar/-Ir` olur (*"kolaylık sağlamaktadır"* -> *"işini kolaylaştırıyor"*). Ad cümlesindeki `-DIr` tanım ve sınıflandırmada korunur (*"Redis bir anahtar-değer veri tabanıdır"*), anlatı akışında seyreltilir. Sıralı yüklemlerde eki yalnızca sonuncuya getir (*"hızlıdır ve güvenilirdir"* -> *"hızlı ve güvenilirdir"*).
- **Vurgu Yuvasını (Yüklem Önü) Kullan:** Türkçede vurgu kalın yazıyla veya *"Tam da bu noktada"* dolgusuyla değil, vurgulanacak ögeyi yüklemin hemen önüne çekerek verilir (*"Dün İzmir'e ben gittim"* vs. *"Ben İzmir'e dün gittim"*). Yüklemden sonraya yalnızca bağlamdan bilinen öge alınabilir.
- **Zamir Düşürme (Pro-Drop), `"Bir"` Yoğunluğu ve `"Kendi"`:** Yüklemdeki kişi eki özneyi zaten taşıyorsa `ben, sen, o, biz` zamirlerini düşür, çünkü açık zamir karşıtlık bildirir. `bir` tek başına hata değildir (*"derin bir iz bıraktı"*). Önce kalıplaşmış birleşik eylemlerin içindekini at (*"büyük bir önem taşıyor"* -> *"büyük önem taşıyor"*), bir cümlede birden fazla *sıfat + bir + soyut ad* varsa seyrelt. `own` çevirisi olan gereksiz `"kendi"` zamirini sil.
- **Edilgen Çatı (`tarafından`), Adlaştırma ve Kof Yardımcı Fiiller:** `tarafından` Türkçenin kendi yapısıdır (*"Köprü Mimar Sinan tarafından yapıldı"*). Yalnızca eyleyen yazarın kendisi ya da kurumu olduğunda (*"Ekibimiz tarafından gerçekleştirilmiştir"* -> *"Ekibimiz yaptı"*) veya kof eylemle birlikte geldiğinde etkene çevir. *"-mAsI gerekmektedir / sağlanmalıdır"* zincirlerini doğrudan çekimle çöz (*"yedeklenmesinin sağlanması gerekmektedir"* -> *"yedeklenmeli"*). *"Gerçekleştirmek, sağlamak, sahip olmak"* öbeklerini seyrelt. `katkıda bulunmak` yerleşik bir deyimdir, sözlükte yer almayan `katkı sunmak` ile değiştirme.
- **Kanıtsallık Kipi (`-mIş`):** Dolaylı öğrenilen, log kaydından okunan veya sonradan fark edilen durumlarda gündelik ve blog register'ında Türkçenin kanıtsallık kipini (`-mIş`) kullan (*"Sunucu gece yeniden başlamış"*). Resmî rapor ve tutanakta kayıtla kesinleşmiş olgu için `-DI` olağandır.

#### Katman 3: TDK Yazım Kılavuzu, Noktalama ve Terminoloji (P2 Sinyalleri)

Detaylı kurallar için `references/tdk-ve-noktalama.md` dosyasını oku:

- **Noktalama ve Bağlaç Kuralları:** `[TDK]` etiketli kurallar TDK Yazım Kılavuzu'na dayanır ve her register'da geçerlidir. `[Üslup]` etiketli kurallar çeviri kokusunu azaltan tercihlerdir ve register'a göre esnetilebilir.
  1. `[TDK]` **Uzun çizgi (em-dash)** yalnızca satır başında konuşma çizgisi olarak kullanılır. Ara söz için virgül ya da TDK'nın ara söz kuralındaki bitişik kısa çizgiyi kullan (*"Küçük bir sürü -dört inekle birkaç koyun- yolun ağzında durmuştu."*). Çoğu zaman en doğal çözüm cümleyi ikiye bölmektir.
  2. `[TDK]` Sayı ve tarih aralıklarında orta çizgi (en-dash) değil **kısa çizgi (`-`)** kullan (`09.30-10.30`, `2024-2026`).
  3. `[TDK]` **`ve`, `veya`, `yahut`, `ya ... ya`** bağlaçlarından önce ve sonra virgül konmaz. `[Üslup]` `ama`, `fakat`, `lakin` için TDK'da virgül kuralı yoktur. İngilizcedeki `..., but` alışkanlığıyla her `ama`dan önce refleks virgül koyma ama uzun cümlede okumayı kolaylaştıran virgülü hata sayma.
  4. `[Üslup]` İç virgülü olmayan iki bağımsız cümleyi İngilizce tarzı **noktalı virgül köprüsüyle** yapıştırma, noktayla ayır. `[TDK]` Noktalı virgülün kılavuzdaki kullanımları doğrudur ve özellikle akademik/hukuki metinde korunur: virgülle ayrılmış tür veya takımları ayırmak, ögeleri arasında virgül bulunan sıralı cümleleri ayırmak.
  5. `[TDK]` Kitap, bildiri ve makalede ana başlık tamamen büyük harfle, alt başlıklar her kelimenin ilk harfi büyük olarak yazılır. Kelimelerin yalnızca ilk harfi büyük yazıldığında `ve`, `ile`, `ya`, `veya`, `yahut`, `ki`, `da`, `de` ve `mı/mi` soru eki küçük kalır (`Suç ve Ceza`). Başlığın tamamı büyük harfle yazıldığında bunlar da büyük yazılır (`YAPAY ZEKÂ VE GELECEK`). Hata, ilk harfleri büyük başlıkta bağlacı büyük yazmaktır (`Yapay Zekâ Ve Gelecek`). `[Üslup]` Blog, teknik belge ve kurumsal metinde ara başlığı tümce düzeninde yazmak daha doğal durur.
- **Teknik Terimleri Zorla Çevirme, Okunuşuna Göre Ek Getir:** Sektörde yerleşik Türkçe karşılığı olmayan teknik terimleri (`endpoint`, `deploy`, `middleware`, `queue`, `cache`, `idempotent`) *"uç nokta, olay güdümlü, ara katman"* diye zorla çevirme. `[TDK]` Kısaltmalara gelen ekler kesmeyle ayrılır ve okunuşa uyar (`TDK'nin`, `TV'ye`). `[Üslup]` Yabancı cins isimlere kesmeyle ek getirmek TDK'da düzenlenmemiş ama yerleşik bir yazım geleneğidir. Bu durumda da ek yazılışa göre değil, **Türkçe okunuşa (fonetiğe)** göre gelir: `cache'i` (keş), `queue'yu` (kü), `SQL'i` (es-kü-el), `JSON'ı` (ceyson).
- **TDK Bağlaç ve Birleşik Kelime Denetimi:** Bulunma durumu eki `-da/-de` (bitişik) ile bağlaç olan `da/de`'yi (ayrı), ilgi/sıfat eki `-ki` ile bağlaç olan `ki`'yi (`belki`, `çünkü`, `hâlbuki`, `mademki`, `meğerki`, `oysaki`, `sanki` kalıplaşmış bitişikler hariç ayrı) ve `birçok`, `birkaç`, `hiçbir`, `herhangi bir`, `pek çok`, `art arda`, `yanı sıra` yazımlarını denetle.

### Adım 3: Öz Denetim (Self-Audit) ve Cümle Ritmi (Burstiness) Kontrolü

Taslağı oluşturduktan sonra kullanıcıya sunmadan önce şu kontrolleri yap:

- **Cümle Uzunluğu Varyasyonu (Burstiness CoV >= 0.40):** Arka arkaya gelen tüm cümleler 15-22 kelime bandında toplanmışsa ritim mekanikleşmiştir. Dedektör iki eşik kullanır: `0.35` altı mekanik (uyarı), `0.40` ve üzeri hedef, arası kabul edilebilir. 3 veya daha fazla cümleli her paragrafta en az bir kısa/vurucu cümle (3-6 kelime) ile en az bir ulaçlı/sola dallanan uzun cümleyi (18-28 kelime) bir arada kullanarak CoV'u `0.40` seviyesinin altına düşürme. Dedektör bu ölçümü yalnızca düz yazı üzerinde yapar; kod bloğu, başlık, tablo satırı ve liste işaretçisi ölçüme girmez. CoV ayrıca kelime sayısı düşük metinlerde (3 cümleden az) güvenilir değildir, tek başına karar ölçütü sayma.
- **Register'da Yerleşik Kalıpları Kusur Sayma:** `söz konusu`, `bu bağlamda`, `sonuç olarak`, `tarafından` + kof eylem gibi kalıplar akademik/resmî/hukuki metinde standarttır. Dedektör bunları o register'da **bilgi** olarak listeler ve puana katmaz; aynı kalıp blog veya kurumsal metinde **sinyal** sayılır. Raporda bir kalemin `[bilgi]` mi `[sinyal]` mi olduğuna bak.
- **Tier-1 Yasaklı Kelime Taraması:** Metinde `âdeta` (`adeta`), `yadsınamaz`, `kritik bir rol oynamaktadır`, `derinlemesine`, `yelpaze`, `dönüm noktası`, `bununla birlikte`, `öte yandan`, `söz konusu`, `bu bağlamda` kalıplarının kalmadığından emin ol (`references/ai-turkcesi-sozlugu.md`).
- **Olgusal Sadakat Kontrolü:** Kaynak metindeki tüm sayılar, tarihler, teknik terimler ve iddialar korundu mu? Kaynakta olmayan bir sayı, yer adı, kişi, sıfat veya abartı eklendi mi? Artış/azalış yönü, olumsuzluk ve ihtiyat (`-ebilir`, `görünüyor`) aynı kaldı mı? Ritim hedefini tutturmak için kaynakta olmayan kısa bir cümle eklendiyse sil.

### Adım 4: Silme Testi (Deletion Test) ve Çıktı Teslimi

- Metne eklediğin her söylem parçacığını (`işte`, `zaten`, `tabii`), devrik cümleyi veya bağlacı test et: Kaldırdığında anlamdan veya tondan hiçbir şey eksilmiyorsa o ögeyi sil.
- Kullanıcı özellikle değişiklik raporu istemediyse ("neleri değiştirdin?" veya `audit` modu dışında) **yalnızca temizlenmiş/yazılmış metni** döndür ve başına "Elbette, metnin doğal Türkçeye çevrilmiş hâli aşağıdadır:" gibi sohbet artıkları ekleme.

## Sık Yapılan Hatalar (Gotchas)

- **Aşırı Düzeltme (Overcorrection) Tuzağı:** Doğal bir Türkçe metinde geçen her `"bir"` kelimesini, her `tarafından`ı veya her devrik cümleyi hata sanma. `"Sen satışa bak"`, `"Site kurmak"`, `"Linki gönder"` gibi doğal ve yerleşik kullanımlara dokunma.
- **Aşırı Sola Dallanma Tuzağı:** İngilizce iskeleti onarırken her bilgiyi tek bir adın önüne sıfat-fiillerle yığma. Okurun yükleme varmadan aklında tutması gereken iç içe yan cümle sayısı ikiyi geçiyorsa cümleyi böl.
- **Öz Türkçecilik Tuzağı:** Bu yetenek yabancı kökenli kelimeleri yasaklayan bir "arı dil" aracı değildir. Günlük ve mesleki Türkçede yaşayan kelimeleri (`performans`, `strateji`, `sistem`, `detay`) zorlama karşılıklarla değiştirme.
- **Sahte Samimiyet:** Kurumsal veya teknik bir metni insanlaştırmak adına metne *"Kahvenizi alın ve arkanıza yaslanın"*, *"Hepimiz oradaydık"* gibi çeviri blog klişeleri ekleme.
- **İkame Kelime Tiki (Replacement Tic) Tuzağı:** "Kritik bir rol oynar" veya "kusursuz bir şekilde" gibi yapay ifadeleri silerken her cümleye refleks olarak "doğrudan", "aslında" veya "ciddi ölçüde" ekleme. Çoğu zaman zarfı tamamen atıp fiili yalnız bırakmak en doğal sonucu verir.
- **Kılık Değiştirmiş Negatif Paralellik Tuzağı:** "Sadece X değil, aynı zamanda Y" kalıbını temizlerken yerine "X ile değil, Y ile" veya "geçici bir X değil, kalıcı bir Y" gibi başka bir negatif paralellik kurma. Olumsuz yarıyı tamamen atıp ne olduğunu söyle.
