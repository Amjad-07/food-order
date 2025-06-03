from flask import Flask, send_file, request, jsonify, redirect, render_template
import requests

app = Flask(__name__)

# 🔁 Backend API behind internal load balancer
BACKEND_URL = "http://internal-instance-ll-rr-1942256296.ap-south-1.elb.amazonaws.com:8080"

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/get-data')
def get_data():
    return send_file('get_data.html')

@app.route('/delete')
def delete():
    return send_file('delete.html')

@app.route('/submitteddata')
def submitted():
    return send_file('submitteddata.html')

@app.route('/data')
def data():
    return send_file('data.html')

# 🔁 Forward order form to backend
@app.route('/submit', methods=['POST'])
def proxy_submit():
    form_data = request.form.to_dict(flat=True)
    
    # If there are multiple addons, handle them as list
    addons = request.form.getlist("addons")
    form_data['addons'] = addons  # This will be JSON-encoded if backend expects it

    try:
        response = requests.post(f"{BACKEND_URL}/submit", json=form_data)
        response.raise_for_status()
        return redirect('/submitteddata')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submitteddata")
def submitted_data():
    try:
        response = requests.get(f"{BACKEND_URL}/submitteddata")
        response.raise_for_status()
        orders = response.json()
    except Exception as e:
        orders = []
    return render_template("submitteddata.html", users=orders)

@app.route('/get-data/<int:order_id>', methods=['GET'])
def proxy_get_data(order_id):
    try:
        response = requests.get(f"{BACKEND_URL}/get-data/{order_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<int:order_id>', methods=['DELETE'])
def proxy_delete(order_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/delete/{order_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
