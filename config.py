import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    """Base configuration class"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", False)
    TESTING = False

    raw_user = os.getenv("DB_USER") or os.getenv("DB_USERNAME") or os.getenv("MYSQL_USER") or ""
    raw_password = os.getenv("DB_PASSWORD") or os.getenv("DB_PASS") or os.getenv("DB_PASSWORD") or ""
    raw_db = os.getenv("DB_NAME") or os.getenv("DB_DATABASE") or os.getenv("MYSQL_DATABASE") or "test"

    def _clean(val: str) -> str:
        return val.strip().strip('"').strip("'") if isinstance(val, str) else val

    DB_USER = _clean(raw_user)
    DB_PASSWORD = _clean(raw_password)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "4000")
    DB_NAME = _clean(raw_db)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "connect_args": {
            "ssl": {
                "ssl_cert_reqs": "NONE",
                "ssl_check_hostname": False
            },
            "charset": "utf8mb4"
        }
    }

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "pdf"}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

FLASK_ENV = os.getenv("FLASK_ENV", "development")
active_config = config.get(FLASK_ENV, config["default"])

if __name__ == "__main__":
    print(f"✓ Active Config: {FLASK_ENV}")
    print(f"✓ Database Host: {active_config.DB_HOST}")
    print(f"✓ Database Port: {active_config.DB_PORT}")
    print(f"✓ Database Name: {active_config.DB_NAME}")
    ssl_enabled = "ssl" in active_config.SQLALCHEMY_ENGINE_OPTIONS.get("connect_args", {})
    print(f"✓ SSL Enabled: {ssl_enabled}")