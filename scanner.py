import os
import shutil
import time
from rules import SortingRule


class FileScanner:
    def __init__(self, rules, on_log_callback=None, on_progress_callback=None, on_finish_callback=None):
        """
        Класс фонового сканера и организатора файлов.

        :param rules: Fayllarni tekshirish uchun SortingRule obyektlari ro'yxati
        :param on_log_callback: Grafik interfeysda log hisobotini chiqarish funksiyasi (qator qabul qiladi)
        :param on_progress_callback: StatusBarni yangilash funksiyasi (joriy indeks, jami fayllar va fayl nomini qabul qiladi)
        :param on_finish_callback: Oqim ishini tugatish funksiyasi (yakuniy holat qatorini qabul qiladi)
        """
        self.rules = rules
        self.on_log = on_log_callback
        self.on_progress = on_progress_callback
        self.on_finish = on_finish_callback
        self._is_running = False

    def stop(self):
        """Сигнал для принудительной остановки сканирования пользователем"""
        self._is_running = False

    def log(self, message):
        """Вспомогательный метод безопасного вызова логирования"""
        if self.on_log:
            self.on_log(message)

    def run_scan(self, source_dir):
        """
        Основной рабочий метод. Должен запускаться внутри threading.Thread,
        чтобы не блокировать главный GUI-поток.
        """
        self._is_running = True
        self.log(f"Katalog tahlili boshlandi: {source_dir}")

        # Проверяем существование папки
        if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
            self.log("XATOLIK: Belgilangan papka mavjud emas.")
            if self.on_finish:
                self.on_finish("XATOLIK: Papka topilmadi.")
            return

        try:
            # Читаем только файлы, находящиеся в корне исходной папки (не лезем в подпапки)
            all_items = os.listdir(source_dir)
            files_to_process = [
                os.path.join(source_dir, f)
                for f in all_items
                if os.path.isfile(os.path.join(source_dir, f))
            ]
        except Exception as e:
            self.log(f"Papkaga yetishishdagi xatolik: {str(e)}")
            if self.on_finish:
                self.on_finish("Papkani o'qishdagi xatolik.")
            return

        total_files = len(files_to_process)
        self.log(f"Tahlil uchun jami fayllar: {total_files}")

        moved_count = 0

        # Поцикловый разбор каждого файла
        for idx, file_path in enumerate(files_to_process, start=1):
            # Проверяем, не нажал ли пользователь "ОТМЕНА"
            if not self._is_running:
                self.log("Jarayon majburan to'xtatildi.")
                if self.on_finish:
                    self.on_finish("Amal bekor qilindi.")
                return

            filename = os.path.basename(file_path)

            # Отправляем данные для честного StatusBar в UI
            if self.on_progress:
                self.on_progress(idx, total_files, filename)

            # Перебираем правила по очереди
            matched = False
            for rule in self.rules:
                if rule.match(file_path):
                    matched = True
                    dest_dir = rule.get_dynamic_target_dir(file_path)

                    # Создаем целевую папку, если ее еще нет на диске
                    try:
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_file_path = os.path.join(dest_dir, filename)

                        # Безопасное перемещение файла
                        shutil.move(file_path, dest_file_path)
                        self.log(f"[MATCH] '{rule.name}': {filename} -> {dest_dir}")
                        moved_count += 1
                    except Exception as error:
                        self.log(f"[KO'CHIRISHDAGI XATOLIK] Fayl {filename}: {str(error)}")

                    # Файл обработан — прерываем цикл правил для этого файла
                    break

            if not matched:
                # Если файл не подошел ни под одно правило, оставляем его на месте без лога
                pass

            # Искусственная микрозадержка (50 мс), чтобы логи бежали красиво, а не мгновенно вспыхивали
            time.sleep(0.05)

        # Финальные аккорды работы
        self.log(f"Muvaffaqiyatli joylashtirildi: {moved_count} {total_files} fayllardan.")
        if self.on_finish:
            self.on_finish("Saralash muvaffaqiyatli yakunlandi!")
