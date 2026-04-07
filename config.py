import ast
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '.config')


def _load_config():
    config = {}
    if not os.path.exists(CONFIG_FILE):
        return config

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if '=' not in line:
                continue

            key, _, raw_value = line.partition('=')
            key = key.strip()
            if not key:
                continue

            value_text = raw_value.strip()
            try:
                config[key] = ast.literal_eval(value_text)
            except Exception:
                config[key] = value_text.strip("'\"")

    return config


def get_config_value(key, default=None):
    config = _load_config()
    return config.get(key, default)


def get_db_dir():
    db_path = get_config_value('DB', get_config_value('DB_PATH', 'Db'))
    if not isinstance(db_path, str):
        db_path = str(db_path)

    db_dir = os.path.join(os.path.dirname(__file__), db_path)
    os.makedirs(db_dir, exist_ok=True)
    return db_dir
