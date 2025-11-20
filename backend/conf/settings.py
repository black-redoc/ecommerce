import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.environ.get("DATABASE_URL", ":memory:")
IS_DEV = os.environ.get("IS_DEV", False)
