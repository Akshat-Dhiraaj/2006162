import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/register_company',methods=['POST'])
def register():
    data = {
        "companyName": "Train Central",
        "ownerName":"Rahul",
        "rollNo": "1",
        "ownerEmail": "rahul@abc.edu",
        "accessCode":"FKDLjg"
    }
    response = requests.post('http://20.244.56.144/train/register',json=data)
    if response.ok:
        return jsonify(response.json()),200
    else:
        return jsonify({'error': 'registration failed'}), response.status_code
    
@app.route('/get_token', methods=['POST'])
def get_token():
    data = {
    "companyName": "Train Central",
    "clientID": "b46118f0-fbde-4b16-a4b1-6ae6ad718b27",
    "ownerName":"Rahul",
    "ownerEmail": "rahul@abc.edu",
    "rollNo":"1",
    "clientSecret": "XOyo10RPasKWOdAN"

    }
    response = requests.post('http://20.244.56.144/train/auth/',json=data)
    if response.ok:
        return jsonify(response.json()),200
    else:
        return jsonify({'error': 'Token authorization failed'}), response.status_code
        
@app.route('/trains', methods=['GET'])
def get_trains():
    data = {
    "trainName": "Chennai Exp",
    "trainNumber": "2344",
    "departureTime":{
        "Hours":21,
        "Minutes":35,
        "Seconds":0
    },
    "seatsAvailable": {
        "sleeper":3,
        "AC":1
    },
    "price": {
        "sleeper":2,
        "AC":5
    },
    "delayedBy": 25
    },
    {
    "trainName": "Hyderabad Exp",
    "trainNumber": "2341",
    "departureTime":{
        "Hours":23,
        "Minutes":55,
        "Seconds":0
    },
    "seatsAvailable": {
        "sleeper":6,
        "AC":7
    },
    "price": {
        "sleeper":554,
        "AC":1854
    },
    "delayedBy": 5
    }

    token_response = requests.post('http://20.244.56.144/train/trains', json=data)
    
    if not token_response.ok:
        return jsonify({'error': 'Token retrieval failed'}), token_response.status_code   
    authorization_token = token_response.json().get('token')

    headers = {
        'Authorization': f'Bearer {authorization_token}'
    }

    reponse = requests.get('http://20.244.56.144/train/trains', headers=headers)
    if reponse.ok:
        sorted_trains = sort_and_filter_trains(response.json())
        return jsonify(sorted_trains),200
    else:
        return jsonify({'error': 'Train data retrieval failed'}), response.status_code

@app.route('/train', methods=['GET'])
def get_train():
    data = {
    "trainName": "Delhi Door Hai Exp",
    "trainNumber": "2343",
    "departureTime":{
        "Hours":9,
        "Minutes":45,
        "Seconds":0
    },
    "seatsAvailable": {
        "sleeper":32,
        "AC":1
    },
    "price": {
        "sleeper":1,
        "AC":723
    },
    "delayedBy": 3
    }

    token_response = requests.post('http://20.244.56.144:80/interview/trains/2344', json=data)
    
    if not token_response.ok:
        return jsonify({'error': 'Token retrieval failed'}), token_response.status_code
    authorization_token = token_response.json().get('token')

    headers = {
        'Authorization': f'Bearer {authorization_token}'
    }

    reponse = requests.get('http://20.244.56.144:80/interview/trains/2344', headers=headers)
    if reponse.ok:
        sorted_trains = sort_and_filter_trains(response.json())
        return jsonify(sorted_trains),200
    else:
        return jsonify({'error': 'Train data retrieval failed'}), response.status_code
if __name__ == '__main__':
    app.run(debug=True)