import os
import json
from rules import SortingRule

CONFIG_FILE = "rules.json"


def load_rules_from_json():
    """Загружает правила из JSON файла. Если файла нет, создает дефолтный."""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Если файла конфигурации нет, генерируем базовый набор (наш успешный локальный тест)
    if not os.path.exists(CONFIG_FILE):
        default_rules = [
            {
                "name": "Tasvirlar",
                "target_dir": os.path.join(current_dir, "SINOV_TASVIRLARI"),
                "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "keywords": [], "is_regex": False, "min_size_mb": None,
                "max_size_mb": None, "created_after": None, "date_grouping": None
            },
            {
                "name": "Kitoblar va Hujjatlar",
                "target_dir": os.path.join(current_dir, "SINOV_HUJJATLARI"),
                "extensions": [".pdf", ".docx", ".doc", ".xlsx", ".txt", ".fb2"],
                "keywords": [], "is_regex": False, "min_size_mb": None,
                "max_size_mb": None, "created_after": None, "date_grouping": None
            },
            {
                "name": "Arxivlar",
                "target_dir": os.path.join(current_dir, "SINOV_ARXIVLARI"),
                "extensions": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "keywords": [], "is_regex": False, "min_size_mb": None,
                "max_size_mb": None, "created_after": None, "date_grouping": None
            }
        ]
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_rules, f, ensure_ascii=False, indent=4)

    # Читаем правила из JSON и превращаем их в объекты Python
    rules_objects = []
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                rule = SortingRule(
                    name=item["name"],
                    target_dir=item["target_dir"],
                    extensions=item.get("extensions"),
                    keywords=item.get("keywords"),
                    is_regex=item.get("is_regex", False),
                    min_size_mb=item.get("min_size_mb"),
                    max_size_mb=item.get("max_size_mb"),
                    created_after=item.get("created_after"),
                    date_grouping=item.get("date_grouping")
                )
                rules_objects.append(rule)
    except Exception as e:
        print(f"JSON konfiguratsiyasini o'qishdagi xatolik: {e}")

    return rules_objects

def save_rules_to_json(rules_list):
    """
    Принимает список объектов SortingRule и перезаписывает rules.json
    """
    data_to_save = []
    for rule in rules_list:
        # Переводим байты обратно в мегабайты для красоты в JSON
        min_size_mb = int(rule.min_size / (1024 * 1024)) if rule.min_size else None
        max_size_mb = int(rule.max_size / (1024 * 1024)) if rule.max_size else None

        rule_dict = {
            "name": rule.name,
            "target_dir": rule.target_dir,
            "extensions": rule.extensions,
            "keywords": rule.keywords,
            "is_regex": rule.is_regex,
            "min_size_mb": min_size_mb,
            "max_size_mb": max_size_mb,
            "created_after": rule.created_after.strftime("%Y-%m-%d") if rule.created_after else None,
            "date_grouping": rule.date_grouping
        }
        data_to_save.append(rule_dict)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

