from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Mini Shop API',
        'version': '1.0.0',
        'timestamp': str(datetime.now())
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/products')
def products():
    return jsonify([
        {'id': 1, 'name': 'Laptop', 'price': 999},
        {'id': 2, 'name': 'Phone', 'price': 599}
    ])

@app.route('/api/version')
def version():
    return jsonify({
        'version': '1.0.0',
        'build': 'dev'
    })

@app.route('/api/status')
def status():
    return jsonify({
        'api': 'running',
        'version': '1.0.0',
        'endpoints': ['/', '/health', '/products', '/api/version', '/api/status']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
