from os import environ

API_KEY = environ.get("API_KEY")
API_HOST = environ.get("API_HOST")
SECRET_KEY = environ.get("SECRET_KEY")
DB_URL = environ.get("DB_URL")


API_URL = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
API_HEADERS = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": API_HOST
}