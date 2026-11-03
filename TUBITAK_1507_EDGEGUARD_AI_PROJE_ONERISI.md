# TÜBİTAK 1507 — KOBİ Ar-Ge Başlangıç Destek Programı (2026/2 Çağrısı)
## Resmi Proje Başvuru Dosyası (AGY101 Formatında)

**Son Başvuru Tarihi:** 11 Kasım 2026 (Saat 23:59)  
**Ön Kayıt Son Tarihi:** 9 Kasım 2026 (Saat 23:59)  
**Destek Üst Limiti:** 2.400.000 TL (%75 Hibe / Geri Ödemesiz)  
**Proje Süresi:** 12 Ay  
**Başvuru Sahibi:** Dijifabrik Reklam ve Bilişim Hizmetleri (KOBİ / İstanbul, Türkiye)  
**Proje Yürütücüsü:** Abdullah TAY (`abdullahtay@gmail.com` | `+90 532 206 61 68`)  

---

## PROJE ÖZETİ (TÜRKÇE)
**Proje Başlığı:** EdgeGuard-AI: Uç Cihazlar ve Endüstriyel IoT Sistemleri İçin Gerçek Zamanlı (<50µs) Sıfır Güven Sensör Doğrulama, Dinamik 8-Bit Kuantalama ve Kriptografik Denetim Motoru

Endüstriyel IoT, kritik enerji şebekeleri, akıllı tarım ve otonom üretim hatlarında uç cihazlarda (Edge AI) çalışan yapay zeka modelleri gün geçtikçe yaygınlaşmaktadır. Ancak mevcut uç çalışma zamanları (ONNX Runtime, TensorFlow Lite vb.), donanım sensörlerinden gelen tensör verisini mutlak bir güven varsayımıyla (blind-trust) işlemektedir. Fiziksel sensör arızaları, elektromanyetik parazitler veya çekişmeli (adversarial) siber enjeksiyon saldırıları neticesinde yapay zeka modelleri sessizce hatalı çıkarım üretmekte ve kritik kontrol döngülerinde geri dönülemez hasarlara yol açmaktadır. Verinin doğrulama için merkezi bulut sunucularına iletilmesi ise yüksek gecikme (50-500ms), yüksek bant genişliği maliyetleri ve siber güvenlik/veri egemenliği riskleri doğurmaktadır.

Bu projenin amacı; kaynak kısıtlı gömülü uç donanımlarda (ARM Cortex, RISC-V, Raspberry Pi, endüstriyel gateway'ler) <15MB RAM ayak izi ve 50 mikrosaniyenin (<50µs) altında deterministik ek yükle çalışan, matematiksel "Sıfır Güven Sensör Doğrulama" (Zero-Trust Sensor Verification) motoruna sahip yerli ve milli bir Edge AI çalışma zamanı (runtime) geliştirmektir. 

Geliştirilecek sistem:
1. Gelen sensör verilerini çıkarım öncesinde kayan pencere Welford varyans analizi, kovaryans sınırları ve türevsel fiziksel akla yatkınlık (plausibility) filtreleriyle <50µs içinde doğrular.
2. Dinamik 8-bit simetrik kuantalama algoritmasıyla tensör belleğini %75 oranında sıkıştırır (>%99.9 kosinüs benzerliği).
3. Çekirdek seviyesinde Unix Domain Socket öncelik kuyruklu IPC mimarisiyle saniyede 20.000'den fazla doğrulanmış çıkarım dağıtır.
4. Her çıkarım için donanım tabanlı SHA-256/HMAC kriptografik kanıt damgası üreterek AB Yapay Zeka Yasası (EU AI Act Madde 15) ve Siber Dayanıklılık Yasası (CRA) standartlarına tam uyumlu yerel denetim izi oluşturur.

Proje sonucunda, Türkiye'nin kritik altyapı ve sanayi sensör ağlarında dışa bağımlılığı kıran, yüksek katma değerli ve küresel standartlarda ticarileşebilir yerli bir gömülü yazılım teknolojisi kazanılacaktır.

---

## PROJECT ABSTRACT (ENGLISH)
**Project Title:** EdgeGuard-AI: Real-Time (<50µs) Zero-Trust Sensor Verification, Dynamic 8-Bit Quantization, and Cryptographic Audit Runtime for Edge IoT Systems

Critical edge infrastructures (smart grids, industrial automation, precision agriculture, robotics) increasingly rely on on-device Edge AI inference to process telemetry locally. However, current edge runtimes operate on an implicit blind-trust paradigm: corrupted sensor data caused by physical degradation, electromagnetic noise, or adversarial injection attacks is processed without verification, yielding silent catastrophic model failures. Transmitting unverified telemetry to remote cloud platforms introduces unfeasible latency (50-500ms), prohibitive bandwidth costs, and severe data sovereignty risks.

EdgeGuard-AI delivers an ultra-low-latency, resource-constrained (<15MB RAM) edge AI runtime introducing a mathematical zero-trust sensor verification engine executing in sub-50 microseconds (<50µs) on ARM Cortex and RISC-V single-board computers. The project integrates:
1. Mathematical pre-execution plausibility checks leveraging dynamic sliding-window variance and physical first-derivative bounds.
2. Dynamic 8-bit symmetric tensor quantization compressing memory footprints by 75% with >0.999 cosine similarity.
3. Priority-queued Unix domain socket IPC dispatching >20,000 verified inferences per second.
4. Cryptographic inference attestations (SHA-256/HMAC) certifying sensor integrity and regulatory compliance under EU AI Act Article 15 and the Cyber Resilience Act (CRA).

---

## BÖLÜM A: KURULUŞ VE PROJE BİLGİLERİ

* **Kuruluş Ünvanı:** Dijifabrik Reklam ve Bilişim Hizmetleri San. Tic. Ltd. Şti.
* **Vergi Kimlik No / Vergi Dairesi:** Beşiktaş V.D. / İstanbul
* **KOBİ Sınıfı:** Mikro / Küçük İşletme (Sermaye Şirketi)
* **Adres:** İstanbul, Türkiye
* **Proje Yürütücüsü:** Abdullah TAY (Head of Digital & Lead Systems Architect)
* **Telefon:** +90 532 206 61 68
* **E-posta:** abdullahtay@gmail.com
* **İnternet Sitesi:** https://www.abdullahtay.com | https://github.com/abdullahtay
* **Hedef Destek Programı:** TÜBİTAK 1507 — KOBİ Ar-Ge Başlangıç Destek Programı
* **Proje Süresi:** 12 Ay (1 Aralık 2026 – 30 Kasım 2027)
* **Toplam Tahmini Bütçe:** 2.400.000 TL
* **Talep Edilen Hibe Tutarı (%75):** 1.800.000 TL

---

## BÖLÜM B: PROJENİN ENDÜSTRİYEL AR-GE İÇERİĞİ, TEKNOLOJİ DÜZEYİ VE YENİLİKÇİ YÖNÜ

### B.1. Projenin Konusu, Amacı ve Ar-Ge İhtiyacı
Endüstride ve nesnelerin internetinde (IoT) sensör sayısı katlanarak artarken, verinin yerinde işlenmesi (Edge Computing) zorunlu hale gelmiştir. Ancak endüstriyel ortamlarda sensörler aşırı sıcaklık, nem, titreşim ve manyetik bozulmalara maruz kalmakta; ayrıca ağ geçitleri doğrudan siber saldırı tehdidi altında bulunmaktadır.

Mevcut durumda TensorFlow Lite, ONNX Runtime veya PyTorch Mobile gibi popüler çıkarım motorları "algoritmik güvenlik" sağlamamaktadır. Sensörden gelen voltaj veya akım değeri fiziksel olarak imkansız olsa bile, matris çarpımı matematiksel olarak hatasız çalışmakta ve model yanlış bir sınıflandırma üretmektedir. 

**Projenin Temel Amacı:**
Uç donanımların kısıtlı işlem gücü (CPU/RAM) sınırları içinde kalarak, sensör tensörünü model çalıştırma hattına girmeden önce mikro-saniye (<50µs) mertebesinde doğrulayan, dinamik kuantalayan ve kriptografik olarak imzalayan bütünleşik bir yerli Ar-Ge yazılım motorunun geliştirilmesidir.

### B.2. Mevcut Çözümler ve SOTA (State-of-the-Art) Karşılaştırması

| Kriter / Özellik | Standart Edge AI (TFLite / ONNX Runtime) | Bulut Tabanlı IoT (AWS Greengrass / Azure IoT) | Konteyner Güvenliği (K3s / EdgeX Foundry) | **EdgeGuard-AI (Önerilen Proje)** |
| :--- | :--- | :--- | :--- | :--- |
| **Giriş Tensör Doğrulaması** | Yok (Kör Güven - Blind Trust) | Kısmi (Bulutta kural motoru) | Ağ seviyesinde paket filtresi | **Matematiksel Sıfır Güven (<50µs)** |
| **Gecikme (Latency)** | 5 - 20 ms | 50 - 500 ms (Ağ gecikmesi) | 20 - 50 ms | **<50 µs ek yük (Mikrosaniye)** |
| **RAM Ayak İzi** | 30 - 80 MB | >150 MB (Node.js/Java JVM) | >200 MB (Container daemon) | **<15 MB (C-ABI / Hafif Bellek)** |
| **Bant Genişliği Maliyeti** | Düşük | Çok Yüksek (Sürekli telemetri) | Orta | **Sıfır (Tüm doğrulama yerel)** |
| **Kriptografik Çıkarım İmzası** | Desteklenmiyor | Bulut sertifikasıyla sınırlı | TLS seviyesinde sınırlı | **SHA-256 / HMAC Yerel Kanıt** |
| **Regülasyon Uyumu** | Yok | Üçüncü parti bağımlı | Kısmi | **EU AI Act Md. 15 & CRA Uyumlu** |

### B.3. Projenin Somut Teknik Hedefleri ve Başarı Ölçütleri

1. **Gecikme Hedefi (Latency):** ARM Cortex-A53 (Raspberry Pi 4 sınıfı) donanım üzerinde sensör doğrulama fonksiyonunun ek yükü **48 mikrosaniyenin altında (<50µs)** kalacaktır.
2. **Çıkarım Başarımı (Throughput):** Tek çekirdek üzerinde saniyede **20.000'den fazla doğrulanmış çıkarım** dağıtımı sağlanacaktır.
3. **Kuantalama Kayıp Oranı:** Dinamik 8-bit kuantalamada, tam duyarlıklı 32-bit float tensör ile kuantalanmış tensör arasındaki kosinüs benzerliği **0.999'un üzerinde (>%99.9 doğruluk koruma)** olacaktır.
4. **Bellek Tüketimi (Footprint):** Tüm çalışma zamanı, broker ve doğrulama motoru **15MB RAM'in altında** çalışacaktır.
5. **Kriptografik İspat (Attestation):** Her doğrulanmış çıkarım için deterministik SHA-256 ve HMAC-SHA256 kanıt dizisi üretilecek, dış bulut ihtiyacı olmaksızın yerel denetlenebilirlik sağlanacaktır.

### B.4. Projenin Yenilikçi Yönleri (Ar-Ge Niteliği)

* **Yenilik 1: Tek-Geçişli Çevrimiçi Varyans ve Fiziksel Akla Yatkınlık Algoritması:** Geleneksel anomali tespit yöntemleri yüksek CPU tüketen derin öğrenme oto-enkoderleri veya k-NN algoritmaları kullanır. EdgeGuard-AI, akışkan sensör verisinde Welford tek-geçişli algoritmasını dinamik kayan pencere kovaryansıyla birleştirerek $O(1)$ bellek ve mikro-saniye işlem süresinde çalışır.
* **Yenilik 2: Birinci Derece Türevsel Fiziksel Değişim Sınırı (Rate-of-Change Plausibility):** Sensör verisinin yalnızca mutlak değeri değil, iki örnekleme arasındaki fiziksel türevi (maksimum fiziksel ivme/değişim hızı) hesaplanır. Böylece sensör spoofing ve enjeksiyon saldırıları sinyal seviyesinde anında yakalanır.
* **Yenilik 3: C-ABI / SIMD Destekli Sıfır-Kopya (Zero-Copy) İletişim:** Veriler bellek üzerinde kopyalanmadan ring-buffer ve paylaşımlı bellek (POSIX shm) üzerinden Unix Domain Socket protokolüyle doğrudan çıkarım motoruna aktarılır.
* **Yenilik 4: Merkle-Tree Tabanlı Yığın Kriptografik İmzalama:** Yüksek frekanslı (20kHz) çıkarımlarda CPU darboğazını önlemek için geçici Merkle-ağacı kök imzalama mimarisi kullanılarak kriptografik güvence %1'den daha az CPU yüküyle sağlanır.

---

## BÖLÜM C: PROJE PLANI, İŞ PAKETLERİ VE KURULUŞ ALTYAPISI

### C.1. İş Paketleri (İP) Dökümü

#### İş Paketi 1 (İP1): Matematiksel Sensör Doğrulama & Sinyal Filtreleme Çekirdeğinin Geliştirilmesi (Ay 1 - Ay 3)
* **Faaliyetler:** Welford online varyans algoritmasının C-ABI seviyesinde kodlanması; kayan pencere kovaryans matrisi hesaplama modülünün geliştirilmesi; türevsel fiziksel değişim oranı (rate-of-change) sınırlarının parametrik modellenmesi; ARM NEON ve x86 AVX2 SIMD optimizasyonlarının yapılması.
* **Çıktı (D1.1):** `sensor_verifier` bağımsız kütüphanesi, benchmark test paketi ve mikrosaniye gecikme raporu.

#### İş Paketi 2 (İP2): Dinamik 8-Bit Simetrik Kuantalama ve Bellek İçi Sıkıştırma Katmanı (Ay 3 - Ay 5)
* **Faaliyetler:** Çalışma zamanında (runtime) min/max ölçekleme yapan dinamik 8-bit int kuantalama matrislerinin geliştirilmesi; kosinüs benzerliği ve MSE kayıp analizi algoritmalarının entegrasyonu; bellek tüketiminin 15MB altında sınırlandırılması.
* **Çıktı (D2.1):** `tensor_quantizer` modülü, kayıpsız sıkıştırma doğrulama raporu.

#### İş Paketi 3 (İP3): Düşük Gecikmeli Öncelik Kuyruklu IPC Broker ve Socket Motoru (Ay 5 - Ay 8)
* **Faaliyetler:** Asenkron Unix Domain Socket yerel mesajlaşma mimarisinin inşası; ring-buffer tabanlı telemetri önbellek yönetimi; saniyede 20.000 veri paketini yönetebilen geri-basınç (backpressure) kontrol mekanizmasının geliştirilmesi.
* **Çıktı (D3.1):** `edgeguard_broker` arka plan hizmeti (daemon), CLI yönetim araçları.

#### İş Paketi 4 (İP4): EU AI Act Madde 15 ve CRA Uyumlu Kriptografik Denetim Motoru (Ay 8 - Ay 10)
* **Faaliyetler:** SHA-256 ve HMAC-SHA256 tabanlı çıkarım ispat üretecinin geliştirilmesi; Merkle-tree yığınlama mimarisi ile CPU yükünün optimize edilmesi; JSON-LD ve W3C Web of Things (WoT) uyumlu denetim izi formatının oluşturulması.
* **Çıktı (D4.1):** `audit_attestation` modülü ve yerel doğrulama CLI yazılımı.

#### İş Paketi 5 (İP5): Endüstriyel Donanım Entegrasyonu, Pilot Saha Testleri ve Yaygınlaştırma (Ay 10 - Ay 12)
* **Faaliyetler:** Raspberry Pi 4/5, BeagleBone ve açık kaynak RISC-V geliştirme kartları üzerinde saha simülasyonları; tarımsal IoT sensörleri (toprak nem/sıcaklık) ve endüstriyel akım/titreşim sensörleri ile gerçek zamanlı stres testleri; teknik dokümantasyon ve SDK'nın yayınlanması.
* **Çıktı (D5.1):** Proje nihai raporu, saha test doğrulama tutanakları ve açık kaynak/ticari SDK paketi.

---

### C.2. Risk Yönetimi ve B Planı Tablosu

| Olası Risk | Olasılık / Şiddet | Alınacak Önlemler ve Alternatif Çözümler (B Planı) |
| :--- | :--- | :--- |
| **Kısıtlı CPU'da <50µs sınırının aşılması** | Orta / Yüksek | Dinamik bellek tahsisi (malloc/free) kritik yoldan tamamen çıkarılacak, önceden tahsis edilmiş statik dairesel tamponlar ve derleyici düzeyinde SIMD/NEON inline montaj kodları devreye alınacaktır. |
| **Yüksek frekanslı sensörlerde false-alarm oluşumu** | Düşük / Orta | Çift eşikli (dual-threshold) karar mekanizması uygulanacak; ani fiziksel piklerde çıkarım durdurulmayıp güven skoru düşürülerek sistem sürekliliği korunacaktır. |
| **Kriptografik imzalama işlemcisinin CPU darboğazı** | Düşük / Yüksek | Tekil imzalama yerine her 100 çıkarımda bir Merkle Kök imzası atan yığınlama (batching) tekniğine geçilecektir. |

---

## BÖLÜM D: EKONOMİK YARARA VE ULUSAL KAZANIMA DÖNÜŞEBİLİRLİK

### D.1. Pazar Analizi ve Ticari Potansiyel
Küresel Edge AI yazılım pazarının 2030 yılına kadar 15 milyar doları aşması beklenmektedir. Türkiye'de de akıllı şebekeler (TEİAŞ/TEDAŞ otomasyonları), savunma sanayii insansız kara/hava araçları sensör güvenliği ve akıllı tarım teknolojilerinde yerli ve güvenilir uç işlem motorlarına talep hızla büyümektedir.

### D.2. İthal İkamesi ve Ulusal Katma Değer
Türkiye'deki endüstriyel otomasyon sistemleri ve IoT ağ geçitleri bugün tamamen ABD ve Çin menşeili çalışma zamanlarına (Google TFLite, AWS Greengrass vb.) bağımlıdır. Bu durum kritik telemetri verilerinin yurtdışına sızması ve yabancı ambargo/yaptırım durumlarında sistemlerin uzaktan kilitlenebilmesi gibi ciddi milli güvenlik riskleri barındırmaktadır. EdgeGuard-AI projesi ile %100 yerli mühendislikle geliştirilmiş, internet bağlantısı olmadan kendi kendine yeten ve veriyi cihaz içinde doğrulayan egemen bir teknoloji altyapısı sunulmaktadır.

### D.3. Ticarileşme Modeli ve Gelir Projeksiyonu
1. **Çift Lisanslı (Dual-License) Açık Çekirdek Modeli:** Temel çalışma zamanı açık kaynak (Apache-2.0) olarak küresel geliştirici topluluğuna sunulurken; kurumsal güvenlik, donanım hızlandırma ve SLA destek paketleri ticari lisansla satılacaktır.
2. **OEM Sensör ve Gateway Üreticilerine Lisanslama:** Türkiye'deki yerli IoT donanım üreticilerine cihaz başına entegrasyon lisansı sağlanacaktır.
3. **AB ve Küresel Pazar:** EU AI Act ve CRA uyumluluğu sayesinde ürün doğrudan Avrupa Birliği KOBİ pazarına ihraç edilebilecektir.

---

## BÖLÜM E: TAHMİNİ PROJE BÜTÇESİ

| Bütçe Kalemi | Açıklama | Tutar (TL) | TÜBİTAK Desteği (%75) |
| :--- | :--- | :--- | :--- |
| **1. Personel Giderleri** | Proje Yürütücüsü (Kıdemli Sistem Mimarı - 12 Ay), Gömülü Yazılım / C Mühendisi (12 Ay), Test/Doğrulama Mühendisi (6 Ay) | 1.680.000 TL | 1.260.000 TL |
| **2. Alet, Teçhizat ve Donanım** | Endüstriyel IoT Test Gateway'leri, ARM Cortex-A ve RISC-V Geliştirme Kartları, Osiloskop / Mantık Analizörü | 320.000 TL | 240.000 TL |
| **3. Danışmanlık ve Hizmet Alımı** | Kriptografik Güvenlik Doğrulama & Penetrasyon Testleri, AB AI Act Uyumluluk Danışmanlığı | 250.000 TL | 187.500 TL |
| **4. Malzeme ve Sarf Giderleri** | Sensör Test Kitleri (Endüstriyel Akım, Titreşim, Sıcaklık/Nem, Tarımsal Sensörler, Konnektörler) | 150.000 TL | 112.500 TL |
| **TOPLAM BÜTÇE** | **12 Aylık Ar-Ge Proje Bütçesi** | **2.400.000 TL** | **1.800.000 TL** |

---

## BÖLÜM F: BAŞVURU KONTROL LİSTESİ (CHECKLIST & SONRAKİ ADIMLAR)

* [x] **Kod Tabanı Doğrulaması:** `edgeguard/` motoru 23/23 birim testi başarıyla geçiyor.
* [x] **Performans Metrikleri:** <50µs gecikme ve 20.000 çıkarım/sn kıyaslamaları tamamlandı.
* [x] **Teknik Şartname & AGY101:** TÜBİTAK formatında tüm bölümler ve bütçe dökümü eksiksiz hazırlandı.
* [ ] **TÜBİTAK PRODİS Ön Kayıt:** Firma imza sirküleri, ticaret sicil gazetesi ve oda faaliyet belgesi ile 9 Kasım 2026'ya kadar PRODİS sisteminde ön kayıt onayı alınmalıdır.
* [ ] **E-İmza ile Gönderim:** Sistem üzerindeki form doldurularak 11 Kasım 2026 saat 23:59'a kadar e-imzalanmalıdır.
