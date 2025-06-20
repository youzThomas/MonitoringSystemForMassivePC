from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/set-reservation', methods=['POST'])
def set_reservation():
    data = request.get_json()
    with open("reservation.json", "w") as f:
        json.dump(data, f)
    return jsonify({"status": "saved"})

if __name__ == '__main__':
    app.run(port=5000)
