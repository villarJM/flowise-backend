import os


class Config:
  POSTGRES_DB: str = os.getenv("POSTGRES_DB")
  POSTGRES_USER: str = os.getenv("POSTGRES_USER")
  POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
  POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
  POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

  SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
  SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

  SECRET_KEY: str = os.getenv("SECRET_KEY")
  JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

class DevelopmentConfig(Config):
  DEBUG: bool = True
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///dev.db")
  SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

class ProductionConfig(Config):
  DEBUG: bool = False
  DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/flowise_prod")
  SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

class TestingConfig(Config):
  TESTING: bool = True
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///:memory:")
  SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

config = {
  "development": DevelopmentConfig,
  "production": ProductionConfig,
  "testing": TestingConfig,
}

def get_config(env: str) -> Config:
  return config[env]
