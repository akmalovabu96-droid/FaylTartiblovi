# import os
# import re
#
# class SortingRule:
#     def __init__(self, name, target_dir, extensions=None, keywords=None):
#         self.name = name  # Название правила (напр., "Документы по работе")
#         self.target_dir = target_dir  # Куда перемещать (напр., "D:/Work/Docs")
#         self.extensions = [ext.lower() for ext in extensions] if extensions else []  # ['.pdf', '.docx']
#         self.keywords = [kw.lower() for kw in keywords] if keywords else []  # ['отчет', 'счет', 'invoice']
#
#     def match(self, file_path):
#         """Fayl ushbu qoidaga mos kelishi yo kelmasligini tekshiradi"""
#         filename = os.path.basename(file_path).lower()
#         _, ext = os.path.splitext(filename)
#
#         # 1. Kengaytma bo'yicha tekshiruv
#         if self.extensions and ext in self.extensions:
#             return True
#
#         # 2. Fayl nomidagi kalit so'zlar bo'yicha tekshiruv
#         if self.keywords:
#             for kw in self.keywords:
#                 if kw in filename:
#                     return True
#
#         return False

import os
import re
from datetime import datetime


class SortingRule:
    def __init__(self, name, target_dir,
                 extensions=None, keywords=None, is_regex=False,
                 min_size_mb=None, max_size_mb=None,
                 created_after=None, date_grouping=None):
        """
        :param name: Qoida nomi (masalan, "Video Gigantlar")
        :param target_dir: Asosiy mo'ljallangan jild (masalan, "D:/Media")
        :param extensions: Kengaytmalar ro'yxati ([’.mp4’, ’.mkv’])
        :param keywords: Kalit so'zlar yoki RegEx shablonlari (['.final.' 'draft'])
        :param is_regex: Agar True bo'lsa, kalit so'zlar muntazam ifodalar sifatida talqin qilinadi.
        :param min_size_mb: Megabaytdagi Minimal fayl hajmi (ixtiyoriy)
        :param max_size_mb: Megabaytdagi Maksimal fayl hajmi (ixtiyoriy)
        :param created_after: "YYYY-OO-KK" sana qatori. Faqat shu sanadan yangiroq fayllarni qayta ishlash
        :param date_grouping: Dinamik ichki jild formati (masalan, "%Y-%m" "2026-09" jildini yaratadi)
        """
        self.name = name
        self.target_dir = target_dir
        self.extensions = [ext.lower() for ext in extensions] if extensions else []
        self.keywords = keywords if keywords else []
        self.is_regex = is_regex

        self.min_size = min_size_mb * 1024 * 1024 if min_size_mb else None
        self.max_size = max_size_mb * 1024 * 1024 if max_size_mb else None

        self.created_after = datetime.strptime(created_after, "%Y-%m-%d") if created_after else None
        self.date_grouping = date_grouping

    def get_dynamic_target_dir(self, file_path):
        """Возвращает финальный путь с учетом группировки по датам"""
        if not self.date_grouping:
            return self.target_dir

        # Берем время последнего изменения файла (самое надежное на всех ОС)
        mtime = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(mtime)

        # Формируем подпапку, например "D:/Media/2026-09"
        subfolder = file_date.strftime(self.date_grouping)
        return os.path.join(self.target_dir, subfolder)

    def match(self, file_path):
        """Проверяет файл по всем честным ретро-критериям. Все условия должны совпасть (AND)"""
        filename = os.path.basename(file_path)
        filename_lower = filename.lower()
        _, ext = os.path.splitext(filename_lower)

        try:
            stat = os.stat(file_path)
        except OSError:
            return False  # Если файл заблокирован системой

        # 1. Проверка по расширению
        if self.extensions and ext not in self.extensions:
            return False

        # 2. Проверка по размеру (в байтах)
        if self.min_size and stat.st_size < self.min_size:
            return False
        if self.max_size and stat.st_size > self.max_size:
            return False

        # 3. Проверка по дате изменения
        if self.created_after:
            file_date = datetime.fromtimestamp(stat.st_mtime)
            if file_date < self.created_after:
                return False

        # 4. Проверка по ключевым словам или RegEx
        if self.keywords:
            matched_keyword = False
            for kw in self.keywords:
                if self.is_regex:
                    if re.search(kw, filename, re.IGNORECASE):
                        matched_keyword = True
                        break
                else:
                    if kw.lower() in filename_lower:
                        matched_keyword = True
                        break
            if not matched_keyword:
                return False

        # Если файл не отсеялся ни на одном этапе — значит, это наш клиент!
        return True

