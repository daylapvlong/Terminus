#!/usr/bin/env python3
"""Simple Flask server for port mapping test."""

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Application configuration
PORT = 5000
HOST = '0.0.0.0'

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'port': PORT,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def home():
    """Home endpoint."""
    return jsonify({
        'message': 'Server is running',
        'port': PORT
    })

@app.route('/api/info')
def info():
    """API info endpoint."""
    return jsonify({
        'service': 'demo-api',
        'version': '1.0.0',
        'port': PORT
    })

if __name__ == '__main__':
    print(f'Starting server on {HOST}:{PORT}...')
    app.run(host=HOST, port=PORT, debug=False)