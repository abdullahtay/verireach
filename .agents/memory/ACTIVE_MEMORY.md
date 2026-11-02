# Active Memory: Hibe, Cascade Funding & Otomasyon Operasyonları

**Son Güncelleme:** 2026-11-02 14:37:00 (+03:00)  
**Kullanıcı Profili:** Abdullah TAY (`abdullahtay@gmail.com` | `+90 532 206 61 68`)  
**Unvan / Rol:** Head of Digital & Full Stack Web Developer / Lead Systems Architect  
**Tüzel Kişilik:** Dijifabrik (SME / Startup, İstanbul, Türkiye)  
**Portföy:** [abdullahtay.com](https://www.abdullahtay.com) | [GitHub: abdullahtay](https://github.com/abdullahtay) | [LinkedIn: abdullahtay](https://www.linkedin.com/in/abdullahtay/)

---

## 1. Tamamlanan Projeler & Kod Tabanları

### A. VeriReach (NLnet Hibe Başvurusu - Tamamlandı & Gönderildi)
* **Kapsam:** PURL ve OpenVEX tabanlı açık kaynak statik reachability ve transitif bağımlılık güvenlik açığı doğrulama motoru.
* **Depo:** [github.com/abdullahtay/verireach](https://github.com/abdullahtay/verireach.git)
* **Test Durumu:** 17/17 birim testi geçiyor.
* **Fonlama:** NLnet Foundation (`nlnet.nl/propose/`) — 50.000 € hissesiz hibe.

### B. EdgeGuard-AI (Horizon Europe Cascade Funding / FSTP)
* **Kapsam:** Uç IoT sensörlerinde gürültülü ve çekişmeli verileri <50µs gecikmeyle filtreleyen, dinamik 8-bit kuantalama (>20.000 çıkarım/sn, <15MB RAM) ve EU AI Act Article 15 kriptografik kanıt (SHA-256/HMAC) üreten doğrulanabilir edge AI çalışma zamanı.
* **Kod Tabanı:** `edgeguard/` (Python & C-ABI mimarisi). 23/23 birim testi geçiyor.
* **Teknik Dokümantasyon:** [`FSTP_CASCADE_PROJESI.md`](file:///Users/tugsahbilge/001UYGULAMALAR/hibe/FSTP_CASCADE_PROJESI.md) (WP1-WP4 iş paketleri, 50.000 € bütçe dökümü).
* **Resmi Başvuru PDF:** [`Annex_2_Technical_Proposal_EdgeGuard_AI.pdf`](file:///Users/tugsahbilge/001UYGULAMALAR/hibe/Annex_2_Technical_Proposal_EdgeGuard_AI.pdf) (238 KB, headless Chrome ile üretildi).

---

## 2. F6S Profil Senkronizasyonu & Güçlendirme (`f6s.com/abdullahtay`)
* Kullanıcı CV'sine göre profil %100 güncellendi:
  * Headline: `Head of Digital & Full Stack Web Developer`
  * Aktif İş: Dijifabrik Ads Agency (Ekim 2021 – Günümüz, Head of Digital)
  * Eğitim: Anadolu Üniversitesi (Çalışma Ekonomisi ve Endüstri İlişkileri, 2010–2015), İTÜ Girişimcilik
  * Yetenekler: General Engineer, Back End Dev, Mobile Dev, Python, Software Development
  * Profil Gücü: %86+ (Full Strength barajı aşıldı).

---

## 3. NOSTRADAMUS Open Call #1 Başvurusu (f6s.com/nostradamus-open-call-1) - [TAMAMLANDI & GÖNDERİLDİ]
* **Durum:** ✅ **FINALIZED & SUBMITTED** (2 Kasım 2026, 14:34)
* **Çağrı Künyesi:** Horizon Europe Grant Agreement No. 101134888 (Data Cube and Copernicus data for Food Security and European Independence).
* **Bütçe:** 50.000 € (%100 Hissesiz / Lump-Sum Hibe).
* **Hedef Konu (Topic):** `T5 - Integrated, cross-domain decision-support applications combining at least two of the above areas`
  * **Alt Konular:** `T2 - Nutrient and soil health management` & `T3 - Water resource efficiency and drought resilience`
* **Başvuru Sahibi:** Dijifabrik (SME / Tek Başvuru Sahibi / Lead Beneficiary).
* **Eklenen PDF Belgesi:** [`Annex_2_Technical_Proposal_EdgeGuard_AI.pdf`](file:///Users/tugsahbilge/001UYGULAMALAR/hibe/Annex_2_Technical_Proposal_EdgeGuard_AI.pdf)
* **Form Seçimleri & Yanıtlar:**
  * **Raising Money:** `No`
  * **Amount Raised from Investors:** `0`
  * **Investors & Equity Holders:** `Abdullah TAY (Founder - 100% Bootstrapped / abdullahtay@gmail.com)`
  * **Runway:** `12 Months`
  * **Customer Type:** `B2B`
    * *Developers:* `Edge AI runtime & sensor verification SDK`
    * *Enterprises:* `Smart agriculture IoT security & sensor data integrity`
  * **Product Interaction:** `API`, `Server software (ie, databases)`, `Hardware-non-wearable`
* **Doğrulama Ekranı:** `f6s.com/nostradamus-open-call-1/discuss` ("You finalized your application")

---

## 4. Çözülen Kritik Sürtünme Noktaları (Frictions & Solutions)
1. **F6S Kilitli Form (Padlock 🔒 Sorunu):** F6S, SME ve konsorsiyum çağrılarında bireysel profil ile doğrudan başvuruya izin vermiyordu. Dijifabrik / EdgeGuard-AI şirket sayfası oluşturularak formun düzenleme kilidi kaldırıldı.
2. **AppleScript Multiline String & Sandbox İzinleri:** Uzun JS kodlarının AppleScript içine gömülmesi syntax hatalarına (-2741) yol açıyordu; Python üzerinden Base64 encode edilip `eval(atob(...))` ile tarayıcıda çalıştırılarak güvenli ve hatasız kılındı.
3. **F6S Özel DOM Bileşenleri (Mootools / Custom Dropdown):** Standart `.value` atamaları F6S iç mimarisini tetiklemediği için `aria-controls` listbox'ları simüle edilerek `.click()` ile ve bitBox etiketleri doğrudan container'a enjekte edilerek dropdown/autocomplete senkronizasyonu sağlandı.
4. **Karakter Sınırları Uyum:** Proje özeti F6S'in 1500 karakterlik tavan sınırına (1493 karakter) ve şirket farklılık alanı 140 karakter sınırına (135 karakter) hassas şekilde optimize edildi.
