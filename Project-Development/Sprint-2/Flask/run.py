from dotenv import load_dotenv
from os import environ, system

load_dotenv(".env")
DEBUG = environ.get("DEBUG", False)

if __name__ == "__main__":
    if DEBUG:
        system("flask run")
    else:
        system("gunicorn app:app")
