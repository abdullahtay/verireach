# StandICT.eu 2029 — Open Call 4 Bireysel Fellowship Başvuru Dosyası
## European ICT Standardisation Fellowship Proposal (100% Lump-Sum Grant)

**Hedef Fon:** StandICT.eu 2029 (Horizon Europe Grant Agreement No. 101069694)  
**Çağrı:** Open Call 4 (Ekim – Aralık 2026)  
**Destek Türü:** Bireysel Uzman Desteği (Fellowship for Natural Persons / ICT Specialists)  
**Hibe Modeli:** **10.000 €** (%100 Geri Ödemesiz Hissesiz Lump-Sum / Götürü Bedel)  
**Cepten Harcama (Eş Finansman):** **0 € (%0 Eş Finansman / Sıfır Maliyet)**  
**Başvuru Sahibi:** Abdullah TAY (Bireysel Yazılım Mühendisi & Sistem Mimarı / Natural Person)  
**Ülke:** Türkiye (Horizon Europe Asosiye Ülkesi - %100 Uygun)  
**İletişim:** `abdullahtay@gmail.com` | `+90 532 206 61 68`  
**Portföy:** [abdullahtay.com](https://www.abdullahtay.com) | [GitHub: abdullahtay](https://github.com/abdullahtay)  

---

## 1. PROPOSAL OVERVIEW (BAŞVURU KÜNYESİ)

* **Proje Başlığı:** Standardised Zero-Trust Sensor Verification and Cryptographic Attestation Schemas for Resource-Constrained Edge AI under EU AI Act (Article 15) and W3C Web of Things
* **Akronim:** `TrustEdge-STD`
* **Destek Kategorisi:** Long-Term (LT) Contribution (6 Aylık Bireysel Katkı)
* **Talep Edilen Hibe:** **10.000 €** (Lump-sum, tek ödeme veya 2 aşamalı hibe)
* **Hedef Standart Geliştirme Kuruluşları (SDO):**
  1. **CEN-CENELEC JTC 21 (Artificial Intelligence):** EU AI Act standardizasyon mandası (M/593) kapsamında "Article 15: Accuracy, robustness and cybersecurity" teknik şartnameleri.
  2. **W3C Web of Things (WoT) Working Group:** Uç cihaz tensör telemetri doğrulama ve Thing Description (TD) JSON-LD uzantıları.
  3. **ETSI ISG SAI (Securing Artificial Intelligence):** Uç cihazlarda çekişmeli saldırılara (adversarial attacks) ve sensör gürültüsüne karşı donanım-bağımsız savunma standartları.

---

## 2. EXCELLENCE & TECHNICAL OBJECTIVES (TEKNİK MÜKEMMELİYET)

### 2.1. Standartlaşma İhtiyacı ve Problem Tanımı
Avrupa Birliği Yapay Zeka Yasası (EU AI Act - Madde 15), yüksek riskli yapay zeka sistemlerinin tüm yaşam döngüleri boyunca "yeterli düzeyde doğruluk, sağlamlık ve siber güvenlik" sergilemesini zorunlu kılmaktadır. Ancak endüstriyel IoT, akıllı tarım ve enerji şebekelerinde çalışan uç yapay zeka (Edge AI) modelleri için standart bir girdi doğrulama protokolü bulunmamaktadır.

Mevcut durumda:
* Sensör donanımı aşınması, elektromanyetik bozulma veya çekişmeli (adversarial) veri enjeksiyonları uç AI modellerinde sessizce hatalı sonuçlara yol açmaktadır.
* Gömülü uç cihazlarda (<15MB RAM, ARM Cortex, RISC-V) çalışabilecek hafif (<50µs gecikmeli) matematiksel akla yatkınlık (plausibility) ve kriptografik çıkarım kanıtı üretecek açık bir veri standardı tanımlanmamıştır.

### 2.2. Bireysel Uzman Olarak Sunulacak Katkı
Bu fellowship kapsamında, bağımsız bir yazılım mühendisi ve sistem mimarı olarak geliştirmiş olduğum `EdgeGuard-AI` açık kaynak mimarisinden elde edilen algoritmik ve ampirik bulgular doğrultusunda:
1. **JSON-LD Tabanlı Doğrulanabilir Telemetri İspatı Şeması (Verifiable Inference Attestation Schema):** W3C Web of Things standartlarına uygun, SHA-256 / HMAC kriptografik zincirine sahip açık format taslağı hazırlanacaktır.
2. **CEN-CENELEC JTC 21 ve ETSI SAI Çalışma Gruplarına Katkı:** EU AI Act Article 15 kapsamında mikro-saniye gecikmeli sıfır güven sensör doğrulaması için Teknik Rapor (TR) ve Standart Taslak Önerisi (NWIP) sunulacaktır.
3. **Açık Kaynak Referans Uygulaması (Apache-2.0):** Standart şemanın herhangi bir tescilli donanıma bağımlı olmadan bağımsız olarak test edilebilmesi için açık kaynak test aparatı (conformance test suite) sağlanacaktır.

---

## 3. IMPACT ON EUROPEAN COMPETITIVENESS & AUTONOMY (ETKİ VE AVRUPA VERİ EGEMENLİĞİ)

1. **Avrupa Standartlaşma Liderliği:** Kritik altyapılarda kullanılan uç yapay zeka sistemlerinde Çin ve ABD menşeili tescilli bulut protokollerine (AWS IoT, Azure Sphere) olan bağımlılığı kırarak, Avrupa'nın açık ve doğrulanabilir uç zeka standartlarına liderlik etmesi sağlanacaktır.
2. **KOBİ ve Açık Kaynak Toplulukları İçin Erişilebilirlik:** Büyük teknoloji tekellerinin ağır ve maliyetli lisansları yerine, bağımsız geliştiricilerin ve KOBİ'lerin ücretsiz entegre edebileceği hafif, telifsiz bir standart ortaya konacaktır.
3. **Regülasyon Uyum Maliyetinin Düşürülmesi:** Avrupa'daki donanım üreticileri ve IoT yazılımcıları, EU AI Act ve CRA uyumluluğunu bu açık standart şeması sayesinde sıfır ek lisans maliyetiyle belgeleyebilecektir.

---

## 4. WORK PLAN, DELIVERABLES & MILESTONES (İŞ PLANI VE KİLOMETRE TAŞLARI)

Proje süresi: 6 Ay (Part-time bireysel uzman emeği - Toplam 200 Saat).

| Kilometre Taşı | Süre | Yapılacak Faaliyetler | Teslim Edilecek Çıktı (Deliverable) |
| :--- | :--- | :--- | :--- |
| **Milestone 1 (M1)** | Ay 1 - Ay 2 | W3C WoT ve CEN-CENELEC JTC 21 mevcut taslaklarının incelenmesi; Edge AI tensör doğrulama gereksinimlerinin haritalandırılması. | **D1.1:** State-of-the-art Standartlaşma Boşluk Analizi Raporu (Gap Analysis Document). |
| **Milestone 2 (M2)** | Ay 3 - Ay 4 | W3C Web of Things uyumlu JSON-LD Telemetri İspat Şeması ve EU AI Act Md. 15 Doğrulama Parametreleri taslak metninin yazılması; ilgili çalışma grubu toplantılarına katılım. | **D2.1:** Resmi Standart Katkı Metni (Contribution Paper / NWIP Draft). |
| **Milestone 3 (M3)** | Ay 5 - Ay 6 | Açık kaynak referans doğrulama kütüphanesi ve uyumluluk test paketinin (conformance test suite) yayınlanması; nihai fellowship raporunun teslimi. | **D3.1:** Açık Şema GitHub Deposu + StandICT.eu Nihai Değerlendirme Raporu. |

---

## 5. BUDGET BREAKDOWN (BÜTÇE DÖKÜMÜ - 100% GÖTÜRÜ HİBE)

* **Talep Edilen Tutar:** **10.000 €**
* **Maliyet Modeli:** Person-Month / Expert Hours Lump-sum.
  * 200 Uzman Mühendislik Saati × 50 €/saat = 10.000 €
* **Cepten Harcama:** 0 €
* **Eş Finansman İhtiyacı:** %0 (Geri ödemesiz, masraf belgeleme ve fatura ibrazı gerektirmeyen gotürü bedel/lump-sum hibe).

---

## 6. APPLICANT TRACK RECORD (BİREYSEL UZMAN PROFİLİ)

* **Adı Soyadı:** Abdullah TAY
* **Pozisyon:** Lead Systems Architect & Senior Full Stack Engineer (10+ Yıl Deneyim)
* **Yetkinlikler:** Sistem programlama (Python, C-ABI, Linux IPC, POSIX), veri yapıları, IoT uç sistemler, açık standartlar (PURL, OpenVEX, SBOM).
* **Mevcut Çalışmalar:**
  * `EdgeGuard-AI`: Sub-50µs doğrulanabilir uç yapay zeka çalışma zamanı ve sensör doğrulayıcısı (23/23 birim testi geçen çalışan prototip).
  * `VeriReach`: PURL (ECMA-427) ve OpenVEX tabanlı yazılım tedarik zinciri açığı doğrulama motoru.
* **Bağımsızlık:** Bireysel araştırmacı ve yazılım uzmanı olarak tam teknik yetkinliğe ve zaman taahhüdüne sahiptir.

---

## 7. BAŞVURU ADIMLARI (PORTAL İŞLEMLERİ)
1. `standict.eu` adresine gidilerek bireysel hesap ile giriş yapılır (EU Login veya yerel kayıt).
2. **Grants / Open Call 4** başvuru alanına girilir.
3. Yukarıda hazırlanan 6 bölüm (Overview, Excellence, Impact, Work Plan, Budget, Track Record) ilgili form alanlarına yapıştırılır.
4. Bireysel CV ve GitHub linki (`https://github.com/abdullahtay`) eklenerek gönderilir.
