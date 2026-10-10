import os

SECRET_KEY = os.environ.get("JUICE_LAB_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
DATABASE_URL = os.environ.get("JUICE_LAB_DB", "sqlite:///./juicelab.db")
