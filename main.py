import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

WHITELIST_FILE = "/data/coolify/services/i0480osk0ggo0kkg884ow4oc/minecraft-data/whitelist.json"

@app.route('/whitelist', methods=['POST'])
def add_to_whitelist():
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({"error": "Username is required"}), 400

        if os.path.exists(WHITELIST_FILE):
            with open(WHITELIST_FILE, 'r') as file:
                whitelist = json.load(file)
        else:
            whitelist = []

        if any(entry['name'] == username for entry in whitelist):
            return jsonify({"message": f"{username} is already whitelisted"}), 200

        new_entry = {"uuid": "unknown", "name": username}
        whitelist.append(new_entry)

        with open(WHITELIST_FILE, 'w') as file:
            json.dump(whitelist, file, indent=4)

        os.system("docker exec -it mc-i0480osk0ggo0kkg884ow4oc rcon-cli whitelist reload")

        return jsonify({"message": f"{username} added to the whitelist"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)