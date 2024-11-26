import os
import json
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

WHITELIST_FILE = "/data/coolify/services/i0480osk0ggo0kkg884ow4oc/minecraft-data/whitelist.json"

@app.route('/whitelist', methods=['POST'])
def add_to_whitelist():
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({"error": "Username is required"}), 400

        command = [
            "docker", "exec", "-it", "mc-i0480osk0ggo0kkg884ow4oc",
            "rcon-cli", "whitelist", "add", username
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 500

        return jsonify({
            "message": f"{username} added to the whitelist",
            "whitelist": True
        }), 200


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)