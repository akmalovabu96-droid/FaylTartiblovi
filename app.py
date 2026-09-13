import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from config import load_rules_from_json, save_rules_to_json


# Импортируем наши созданные модули
from rules import SortingRule
from scanner import FileScanner
from config import load_rules_from_json



class RetroOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Настройки окна в духе утилит конца 90-х
        self.title("RetroOrganizer v1.0 — Tartib Dvijogi")
        self.geometry("650x460")
        self.configure(bg="#d9d9d9")  # Тот самый серый цвет окон

        # Ретро-шрифты
        self.retro_font = ("Arial", 9)
        self.retro_font_bold = ("Arial", 9, "bold")

        # Стейт приложения
        self.source_dir = tk.StringVar(value="Tanlanmagan...")
        self.status_text = tk.StringVar(value="Dastur amaliyotga tayyor.")

        # Инициализация дефолтного набора правил
        self.rules = load_rules_from_json()

        # Инициализация объекта сканера (передаем функции-колбэки)
        self.scanner = FileScanner(
            rules=self.rules,
            on_log_callback=self._write_log,
            on_progress_callback=self._update_progress,
            on_finish_callback=self._finalize_scan
        )

        # Отрисовка интерфейса
        self._create_widgets()

    def _create_widgets(self):
        # 1. Рамка выбора директории (Top)
        top_frame = tk.LabelFrame(self, text=" Tozalash uchun asl jild ",
                                  bg="#d9d9d9", font=self.retro_font_bold,
                                  relief=tk.GROOVE, bd=2)
        top_frame.pack(fill="x", padx=10, pady=5)

        lbl_dir = tk.Label(top_frame, text="Yo'l:", bg="#d9d9d9", font=self.retro_font)
        lbl_dir.pack(side="left", padx=5, pady=5)

        self.entry_dir = tk.Entry(top_frame, textvariable=self.source_dir,
                                  font=self.retro_font, bg="white",
                                  relief=tk.SUNKEN, bd=2, state="readonly")
        self.entry_dir.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        btn_browse = tk.Button(top_frame, text="Tanlash...", font=self.retro_font,
                               command=self._browse_folder, bg="#d9d9d9",
                               relief=tk.RAISED, bd=2)
        btn_browse.pack(side="right", padx=5, pady=5)

        # 2. Ретро-консоль логирования (Center)
        log_frame = tk.LabelFrame(self, text=" Jarayonning bajarilishi (Log) ",
                                  bg="#d9d9d9", font=self.retro_font_bold,
                                  relief=tk.GROOVE, bd=2)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, font=("Courier New", 9),
                                                  bg="black", fg="#00ff00",
                                                  relief=tk.SUNKEN, bd=3)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        self._write_log("RetroOrganizer tizimi tayyor. Qoidalar bazasi muvaffaqiyatli yuklandi.")

        # ----------------------------------------------------
        # 3. Кнопки управления (Bottom) — ИСПРАВЛЕНО
        # ----------------------------------------------------
        control_frame = tk.Frame(self, bg="#d9d9d9")
        control_frame.pack(fill="x", padx=10, pady=5)

        # Переносим width и height внутрь tk.Button.
        # Внимание: для tk.Button на Windows width и height задаются в ХАРАКТЕРАХ текста (знакоместах), а не в пикселях!
        self.btn_start = tk.Button(control_frame, text="SARALASH",
                                   font=self.retro_font_bold, bg="#d9d9d9",
                                   command=self._start_sorting, relief=tk.RAISED, bd=3,
                                   width=20, height=1)  # <- ПЕРЕНЕСЕНО СЮДА
        self.btn_start.pack(side="left", pady=5)

        self.btn_stop = tk.Button(control_frame, text="BEKOR QILISH",
                                  font=self.retro_font_bold, fg="darkred", bg="#d9d9d9",
                                  command=self._stop_sorting, relief=tk.RAISED, bd=2,
                                  state="disabled",
                                  width=12, height=1)  # <- ПЕРЕНЕСЕНО СЮДА
        self.btn_stop.pack(side="right", pady=5)

        self.btn_rules = tk.Button(control_frame, text="Qoidalar...",
                                   font=self.retro_font, bg="#d9d9d9",
                                   command=self._open_rules_editor, relief=tk.RAISED, bd=2,
                                   width=12, height=1)
        self.btn_rules.pack(side="left", padx=10, pady=5)

        # 4. Честный StatusBar (Самый низ)
        self.status_bar = tk.Label(self, textvariable=self.status_text,
                                   font=self.retro_font, bd=1, relief=tk.SUNKEN,
                                   anchor="w", bg="#d9d9d9", padx=5, pady=3)
        self.status_bar.pack(side="bottom", fill="x")

    # --- Колбэки для взаимодействия со сканером ---

    def _write_log(self, text):
        """Вызывается сканером для вывода строки в консоль"""
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f">> {text}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def _update_progress(self, current, total, filename):
        """Вызывается сканером для обновления StatusBar"""
        # Обрезаем имя файла для статус-бара, если оно слишком длинное
        short_name = filename if len(filename) < 30 else f"{filename[:27]}..."
        self.status_text.set(f"Qayta ishlov: {current} {total} dan [{short_name}]")

    def _finalize_scan(self, final_status):
        """Вызывается сканером при завершении или отмене процесса"""
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.status_text.set(final_status)

    # --- Логика элементов управления GUI ---
    def _browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_dir.set(folder)
            self._write_log(f"Faol katalog tanlandi: {folder}")
            self.status_text.set("Papka skanerlanishiga tayyor.")

    def _start_sorting(self):
        src = self.source_dir.get()
        if src == "Tanlanmagan..." or not os.path.exists(src):
            messagebox.showwarning("Diqqat", "Iltimos, saralash uchun mavjud papkani tanlang!")
            return

        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")

        # Запускаем метод сканера в отдельном фоновом Thread, чтобы интерфейс не зависал
        scan_thread = threading.Thread(target=self.scanner.run_scan, args=(src,), daemon=True)
        scan_thread.start()

    def _stop_sorting(self):
        self.scanner.stop()
        self.status_text.set("Jarayonning to'xtatilishi... Iltimos, kutib turing.")

    def _open_rules_editor(self):
        """Открывает классическое дополнительное ретро-окно для управления правилами"""
        editor = tk.Toplevel(self)
        editor.title("Saralash Qoidalar Boshqaruvi")
        editor.geometry("450x300")
        editor.configure(bg="#d9d9d9")
        editor.transient(self)  # Окно привязано к главному
        editor.grab_set()  # Блокирует главное окно, пока открыт редактор

        # Заголовок списка
        lbl_info = tk.Label(editor, text="Avtomatizatsiyalash bo'yicha faol qoidalar ro'yxati:",
                            bg="#d9d9d9", font=self.retro_font_bold)
        lbl_info.pack(anchor="w", padx=10, pady=5)

        # Контейнер для списка и скроллбара
        list_frame = tk.Frame(editor, bg="#d9d9d9")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Классический Listbox для выбора элементов списка
        self.rules_listbox = tk.Listbox(list_frame, font=self.retro_font,
                                        yscrollcommand=scrollbar.set, relief=tk.SUNKEN, bd=2)
        self.rules_listbox.pack(fill="both", expand=True, side="left")
        scrollbar.config(command=self.rules_listbox.yview)

        # Заполняем Listbox названиями текущих правил
        self._refresh_rules_listbox()

        # Правая/Нижняя панель действий
        btn_frame = tk.Frame(editor, bg="#d9d9d9")
        btn_frame.pack(fill="x", padx=10, pady=10)

        btn_delete = tk.Button(btn_frame, text="Qoidani o'chirib tashlash", font=self.retro_font,
                               command=self._delete_selected_rule, relief=tk.RAISED, bd=2)
        btn_delete.pack(side="left", padx=5)

        btn_close = tk.Button(btn_frame, text="Yopish", font=self.retro_font,
                              command=editor.destroy, relief=tk.RAISED, bd=2, width=10)
        btn_close.pack(side="right", padx=5)

    def _refresh_rules_listbox(self):
        """Обновляет элементы внутри Listbox"""
        self.rules_listbox.delete(0, tk.END)
        for rule in self.rules:
            self.rules_listbox.insert(tk.END,
                                      f"{rule.name} -> {rule.extensions if rule.extensions else 'RegEx/Keywords'}")

    def _delete_selected_rule(self):
        """Удаляет выбранное правило из памяти приложения и сохраняет изменения в JSON"""
        try:
            selected_idx = self.rules_listbox.curselection()[0]
            rule_name = self.rules[selected_idx].name

            # Удаляем из нашего списка правил в памяти
            del self.rules[selected_idx]

            # Сохраняем обновленный список в rules.json через config.py
            save_rules_to_json(self.rules)

            # Обновляем визуальный список и пишем в лог
            self._refresh_rules_listbox()
            self._write_log(f"OK: '{rule_name}' qoidasi muvaffaqiyatli o'chirib tashlandi.")

            # Синхронизируем правила в самом сканере
            self.scanner.rules = self.rules

        except IndexError:
            messagebox.showwarning("Diqqat", "Iltimos, ushbu amal uchun avval qoidalardan birini tanlang!")

if __name__ == "__main__":
    app = RetroOrganizerApp()
    app.mainloop()
