from flask import Flask, send_file, request, jsonify, redirect
import requests

app = Flask(__name__)

# Internal backend API behind AWS internal load balancer
BACKEND_URL = "http://internal-food-internal-1544954247.ap-south-1.elb.amazonaws.com:8080"

@app.route('/', methods=['GET', 'POST'])
def handle_root():
    if request.method == 'GET':
        return send_file('index.html')
    elif request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data['addons'] = request.form.getlist("addons")
        try:
            # Forward the form as JSON to the backend `/submit` endpoint
            response = requests.post(f"{BACKEND_URL}/submit", json=form_data)
            response.raise_for_status()
            return redirect('/')
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Catch-all route to support frontend routing (e.g., React/Angular/Vue SPA)
@app.route('/<path:path>')
def catch_all(path):
    return send_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
