# FaylTartiblovi

# 💾 RetroOrganizer v1.0

**RetroOrganizer** — bu kataloglaringizni avtomatik ravishda tartibga solish uchun yengil va moslashuvchan vositadir. Utilita *Windows 95 / XP* davridagi muhandislik dasturiy ta’minotining lampali, nostalgik interfeysini va zamonaviy ko‘p oqimli intellektual fayllarni saralash dvigatelini o‘zida mujassam etgan.

Loyiha old school dasturiy ta’minoti estetikasini qadrlaydigan, ammo raqamli tartibsizlik muammolarini hal qilishga muhtoj bo‘lgan (Yuklanmalar papkasini tozalash, ishlab chiqish keshini saralash, hujjatlarni tizimlashtirish) ishqibozlar uchun yakka dasturchi tomonidan yaratilgan.

---

## 🎨 Xususiyatlar (Features)

*   **💾 Qulay retro-interfeys:** Zamonaviy mavzulardan foydalanilmagan, klassik `tkinter` kutubxonasi asosida yaratilgan toza grafik interfeys. Hajmdor ramkalar, bo‘rtma tugmalar va yorqin yashil rangdagi log-monitor old school dasturlari muhitini yaratadi.
*   **🧵 Ko‘p oqimlilik:** Fayllarni skanerlash va ko‘chirish alohida fon oqimida (`threading`) amalga oshiriladi. Interfeys hech qachon qotib qolib, *"Javob bermayapti(Not Responding/Не отвечает)"* holatiga o‘tmaydi — loglar va StatusBar uzluksiz yangilanib turadi.
*   **🧠 Aqlli qoidalar mexanizmi:** Fayllarni faqat kengaytmasiga qarab emas, balki murakkab mezonlar asosida ham saralaydi: fayl hajmi, o‘zgartirilgan sana, kalit so‘zlarni qidirish hamda muntazam ifodalar (`RegEx`) qo‘llab-quvvatlanadi.
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
   cd RetroOrganizer
   ```
2. `app.py`, `scanner.py`, `rules.py` va `config.py` fayllarini bitta ishlaydigan direktoriyaga joylang.

3. Bosh faylini ishga tushiring:
   ```bash
   python app.py
   ```

---

## 🔧 `rules.json` orqali qoidalarni sozlash

Dastur birinchi marta ishga tushirilganda rules.json konfiguratsiya faylini avtomatik ravishda yaratadi. O'z qoidalaringizni to‘g‘ridan-to‘g‘ri dastur interfeysi orqali qo‘shishingiz yoki JSON faylini qo‘lda tahrirlashingiz mumkin.

Murakkab qoida tuzilishiga misol:
```json
{
    "name": "Katta hajmli filmlar",
    "target_dir": "D:/Movies",
    "extensions": [".mkv", ".mp4"],
    "keywords": [],
    "is_regex": false,
    "min_size_mb": 1000,
    "max_size_mb": null,
    "created_after": null,
    "date_grouping": "%Y-%m"
}
```

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

