import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    TESTING = False

    # ===============================
    # DATABASE CONFIGURATION
    # ===============================

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        DB_USER = os.getenv("DB_USER", "")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "4000")
        DB_NAME = os.getenv("DB_NAME", "test")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "connect_args": {
            "charset": "utf8mb4"
        },
    }

    # ===============================
    # CLOUDINARY
    # ===============================

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # ===============================
    # RESEND
    # ===============================

    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    # ===============================
    # FILE UPLOAD
    # ===============================

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "pdf"}


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

FLASK_ENV = os.getenv("FLASK_ENV", "development")

active_config = config.get(FLASK_ENV, config["default"])


if __name__ == "__main__":
    print(f"Environment : {FLASK_ENV}")
    print(f"Database    : {active_config.SQLALCHEMY_DATABASE_URI}")
