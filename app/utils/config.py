import os


def _get(var: str, default: str = "", required=True) -> str:
    env_var = os.getenv(key=var)
    if required and not env_var:
        raise SystemExit(f"missing environment variable ({var}) exiting...")
    return env_var or default


DATABASE_HOST = _get("DATABASE_HOST")
DATABASE_NAME = _get("DATABASE_NAME")
DATABASE_PASS = _get("DATABASE_PASS")
DATABASE_USER = _get("DATABASE_USER")
DATABASE_URL = f"mysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:3306/{DATABASE_NAME}"
DEBUG = bool(int(_get("DEBUG", default="0", required=False)))
ENVIRONMENT = _get("ENVIRONMENT")
KAGGLE_DATASET = _get("KAGGLE_DATA")
KAGGLE_DATASET_PATH = _get("KAGGLE_DATA_PATH")
KAGGLE_KEY = _get("KAGGLE_KEY")
KAGGLE_USERNAME = _get("KAGGLE_USERNAME")
LOG_LEVEL = _get("LOG_LEVEL", default="DEBUG", required=False)
LOG_FORMAT = _get(
    "LOG_FORMAT",
    default="%(levelname)s:%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
    required=False,
)
