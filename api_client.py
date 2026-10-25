
import requests
import json

API_URL = "http://127.0.0.1:5000/api/students"


def main():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        students = response.json()

        print("STUDENT RECORDS FROM MY API")
        print(json.dumps(students, indent=4))

    except requests.RequestException as error:
        print("Could not connect to the API.")
        print("Make sure app.py is running.")
        print("Details:", error)


if __name__ == "__main__":
    main()
