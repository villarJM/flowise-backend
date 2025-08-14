import os


class Config:
  SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
  JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

class DevelopmentConfig(Config):
  DEBUG: bool = True
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///dev.db")

class ProductionConfig(Config):
  DEBUG: bool = False
  DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/flowise_prod")

class TestingConfig(Config):
  TESTING: bool = True
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///:memory:")

config = {
  "development": DevelopmentConfig,
  "production": ProductionConfig,
  "testing": TestingConfig,
}

def get_config(env: str) -> Config:
  return config[env]
