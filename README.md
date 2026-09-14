# FaylTartiblovi

# 💾 RetroOrganizer v1.0

**RetroOrganizer** — bu kataloglaringizni avtomatik ravishda tartibga solish uchun yengil va moslashuvchan open-source(ochiq manbai kodli) vositadir. Ushbu utilita *Windows 95 / XP* davridagi muhandislik dasturiy ta’minotining lampali, nostalgik interfeysini va zamonaviy ko‘p oqimli intellektual fayllarni saralash dvigatelini o‘zida mujassam etgan.

Bu loyiha old school dasturiy ta’minoti estetikasini qadrlaydigan, ammo raqamli tartibsizlik muammolarini hal qilishga muhtoj bo‘lgan (Yuklanmalar papkasini tozalash, ishlab chiqish keshini saralash, hujjatlarni tizimlashtirish) ishqibozlar uchun yakka dasturchi tomonidan yaratilgan.

---

## 🎨 Xususiyatlar (Features)

*   **💾 Qulay retro-interfeys:** Zamonaviy mavzulardan foydalanilmagan, klassik `tkinter` kutubxonasi asosida yaratilgan toza grafik interfeys. Hajmdor ramkalar, bo‘rtma tugmalar va yorqin yashil rangdagi log-monitor old school dasturlari muhitini yaratadi.
*   **🧵 Ko‘p oqimlilik:** Fayllarni skanerlash va ko‘chirish alohida fon oqimida (`threading`) amalga oshiriladi. Interfeys hech qachon qotib qolib, *"Javob bermayapti(Not Responding/Не отвечает)"* holatiga o‘tmaydi — loglar va StatusBar uzluksiz yangilanib turadi.
*   **🧠 Aqlli qoidalar mexanizmi:** Fayllarni faqat kengaytmasiga qarab emas, balki murakkab mezonlar asosida ham saralaydi: fayl hajmi, o‘zgartirilgan sana, kalit so‘zlarni qidirish hamda muntazam ifodalar (`RegEx`) qo‘llab-quvvatlanadi (Batafsilroq: `rules.json` **orqali qoidalarni sozlash bo'limida**.
*   **📂 Sana bo‘yicha guruhlash:** Fayllarni dinamik ichki kataloglarga avtomatik ravishda ajratish imkoniyati. Masalan, fotosuratlar yoki hisobotlarni oylar bo'yicha `2026-09/` kabi kataloglarga guruhlash mumkin.
*   **⚙️ Interaktiv boshqaruv:** Avtomatlashtirish qoidalarini bevosita dastur ichidagi **"Qoidalar..."** paneli orqali boshqaring — konfiguratsiyani dastur ishlayotgan paytda o‘chiring yoki sozlang.
*   **📦 Bog‘liqliklarsiz:** Dastur faqat Python standart kutubxonasidan foydalanadi. Hech qanday `pip install` talab qilinmaydi — yuklab oling va ishga tushiring.

---

## 🚀 Tezkor ishga tushirish (Quick Start)

### Talablar
*   **Python 3.10 yoki undan yuqori** (amaldagi 3.13+ versiyalarida sinovdan o'tkazilgan)
*   Operatsion tizim: Windows, macOS, Linux.

### O'rnatish
1. Repozitoriyni nusxalab oling va IDE'ingizga joylang:
   ```bash
   git clone https://github.com
   cd FaylTartiblovi
   ```
2. Bosh faylini ishga tushiring:
   ```bash
   python Tartiblovchi.py
   ```

---

## 🔧 `rules.json` orqali qoidalarni sozlash

Dastur birinchi marta ishga tushirilganda rules.json konfiguratsiya faylini avtomatik ravishda yaratadi. O'z qoidalaringizni sozlash uchun JSON faylini qo‘lda tahrirlashingiz mumkin.

Murakkab qoida tuzilishiga misol:
```json
{
    "name": "Katta hajmli filmlar",
    "target_dir": "D:/Movies",
    "extensions": [".mkv", ".mp4"],
    "keywords": [],
    "is_regex": false,
    "min_size_mb": null,
    "max_size_mb": null,
    "created_after": null,
    "date_grouping": "null"
}
```
### ⚠️ Filtrlarni sozlash bo‘yicha muhim eslatma (`null` qiymati)
E’tibor bering, standart bo‘yicha oxirgi 4-ta parametrlar **`null`** qiymatiga ega. Bu shuni anglatadiki, **filtr o‘chirilgan** va dvijok uni e’tiborsiz qoldiradi:

* **Sana asosida avtomatik guruhlashni** yoqish uchun, albatta `"date_grouping": null` ni sana formatiga almashtiring, masalan: `"%Y-%m"` (fayllarni yili va oyiga qarab `2026-09/` jildlarga ajratadi) yoki `"%Y"` (faqat yiliga qarab taxlaydi).
* **Hajm bo‘yicha cheklov** (faqat og'ir fayllar, masalan`"max_size_mb": 5`): dastur kichik fayllarni o‘tkazib yuboradi va faqat 5 Megabaytdan kattalarini ko‘chiradi.
* **Yaratilgan/o‘zgartirilgan sana bo‘yicha filtr**: agar `"created_after": `dagi `null` `2026-01-01` ga o'zgartirilsa, ushbu utilita 2026'dan eski fayllarni butunlay e’tiborsiz qoldiradi va faqat 2026-yil boshidan beri o‘zgartirilgan fayllarni qayta ishlab, ko'chiradi.
* **Kalit so‘zlar bo‘yicha filtr**: masalan, faqat `"keywords": ["work". "invoice"]` kabi kalit so'zlarni o'z ichiga olgan va kengaytmasiga mos kelgan fayllarnigina ko'chiradi. Aytaylik, sizda `"extensions": [."pdf"]` va `"keywords": ["invoice"]` sozlangan, bu vaziyatda `invoice_photo.jpg` nomli fayl ko‘chirilmaydi, chunki kengaytma mos kelmadi. Masalan, `.pdf` li `invoice_part.pdf` kabi fayllar esa bemalol ko'chiriladi.

* Agar barchasi `null` holatida qoldirilsa, dastur fayllarni *faqat* standartli `extensions` kengaytmalari ro‘yxati bo‘yicha filtrlaydi.

---

## 🏛️ Loyiha arxitekturasi

Loyiha OOP tamoyillari asosida ishlab chiqilgan va bir-biridan mustaqil modullarga ajratilgan:
*   `app.py` — Taqdimot qatlami (View / GUI). Oynalar, tugmalar, log-konsol va StatusBar uchun javob beradi.
*   `scanner.py` — Boshqaruv qatlami (Core Engine). Fayllarni fonda tahlil qilish va ko‘chirish jarayonini boshqaradi.
*   `rules.py` — Ma'lumotlar modeli qatlami (Rules Engine). Fayllarning berilgan filtrlarga mosligini tekshiradi.
*   `config.py` — Ma'lumotlar bilan ishlash qatlami (Storage). Obyektlarni JSON formatiga seriyalash va undan qayta tiklashni amalga oshiradi.
---

## 📜 Litsenziya (License)

Loyiha **MIT** litsenziyasi asosida tarqatiladi. Litsenziya shartlariga rioya qilingan holda dasturdan erkin foydalanish, uni o'zgartirish, tarqatish va tijorat maqsadlarida foydalanishga ruxsat beriladi. 

Qiziquvchan tomonidan qiziquvchilar uchun chin dildan yaratildi! ☕ ☕

