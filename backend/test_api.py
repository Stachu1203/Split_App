import requests
import json

url = 'http://127.0.0.1:5000/api/splitapp'


mock_data = [
    {
        "id": 1,
        "payer": "Anna",
        "total_amount": 150.0,
        "borrowers": [
            { "name": "Bartek", "owes": 100.0 },
            { "name": "Michal", "owes": 50.0 }
        ]
    },
    {
        "id": 2,
        "payer": "Bartek",
        "total_amount": 60.0,
        "borrowers": [
            { "name": "Anna", "owes": 60.0 }
        ]
    }
]


print("Wysyłam zapytanie do API...")
response = requests.post(url, json=mock_data)


print("Status Code:", response.status_code)
print("Wynik (transakcje):")
print(json.dumps(response.json(), indent=4))