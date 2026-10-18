import requests

url = "https://wenmarkagudon.onrender.com/greet"

response = requests.get(url, params={"name": "Wen"})

if response.status_code == 200:
    data = response.json()

    print("Name:", data["name"])
    print("Program:", data["program"])
    print("Section:", data["section"])
    print("Year:", data["year"])
    print("Student ID:", data["student_id"])
else:
    print("Request failed.")
    print("Status Code:", response.status_code)
