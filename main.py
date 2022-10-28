import datetime
import requests


def nutritionix():
    nutritionix_app_id = "7fc6a9c1"
    nutritionix_api_key = "7655eb45295200a1c012a21ea8ff038b"
    nutritionix_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    nutritionix_headers = {
        "x-app-id": nutritionix_app_id,
        "x-app-key": nutritionix_api_key
    }
    nutritionix_params = {
        "query": query,
        "gender": GENDER,
        "weight_kg": WEIGHT,
        "height_cm": HEIGHT,
        "age": AGE
    }

    nutritionix_response = requests.post(url=nutritionix_exercise_endpoint, json=nutritionix_params,
                                         headers=nutritionix_headers)
    nutritionix_response.raise_for_status()
    result = nutritionix_response.json()

    return result["exercises"][0]


# --------------- CONSTANTS --------------- #
DATE = datetime.datetime.now().strftime("%d/%m/%Y")
TIME = datetime.datetime.now().strftime("%X")

GENDER = "male"
WEIGHT = "73"
HEIGHT = "165"
AGE = "28"

SHEETY_ENDPOINT = "https://api.sheety.co/f1810fe8ae8de2f741a0e4c58034e85c/workoutTracker/workouts"
SHEETY_AUTH = ("zoul", "#72rv+vaesj7t#")

# --------------- MAIN --------------- #
start = input("Do you want to add or delete workout? ").lower()

if start == "add":
    query = input("Tell me which exercise you did: ")

    sheety_params = {
        "workout": {
            "date": DATE,
            "time": TIME,
            "exercise": nutritionix()["name"].title(),
            "duration": nutritionix()["duration_min"],
            "calories": nutritionix()["nf_calories"],
        }
    }

    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_params, auth=SHEETY_AUTH)
    print("Workout added")

elif start == "delete":
    sheety_response_get = requests.get(url=SHEETY_ENDPOINT, auth=SHEETY_AUTH).json()
    try:
        object_id = sheety_response_get["workouts"][-1]["id"]
    except IndexError:
        print("No more entries to delete")
    else:
        sheety_response = requests.delete(url=f"{SHEETY_ENDPOINT}/{object_id}", auth=SHEETY_AUTH)
        print("Workout deleted")

