#!/usr/bin/env python3
"""
Darth Vader Threat Generator
Flask app that displays Imperial threats from the Dark Side

Entry point for the Darth Vader threat generator application.
"""

from flask import Flask, jsonify, render_template
import os
import sys
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

# Import your modules here
from core import get_random_threat, get_threat_count
from utils import get_timestamp

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "vader_threat_generator",
        "timestamp": get_timestamp()
    })

@app.route('/')
def home():
    """Main threat display page"""
    threat_data = get_random_threat()
    return render_template('index.html', 
                         threat=threat_data['threat'],
                         threat_count=get_threat_count())

@app.route('/api/threat')
def api_threat():
    """API endpoint for getting a random threat"""
    return jsonify(get_random_threat())

@app.route('/api/threat/count')
def api_threat_count():
    """API endpoint for threat count"""
    return jsonify({
        "total_threats": get_threat_count(),
        "service": "vader_threat_generator"
    })

@app.route('/api')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        "name": "Darth Vader Threat Generator API",
        "version": "0.1.0",
        "description": "Imperial threat delivery system",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Main threat display page"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api/threat", "method": "GET", "description": "Get random threat"},
            {"path": "/api/threat/count", "method": "GET", "description": "Get threat count"},
            {"path": "/api", "method": "GET", "description": "API documentation"}
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"⚫ Starting Darth Vader Threat Generator on port {port}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"🔍 Health check: http://localhost:5000/health")
    print(f"⚔️ Threat API: http://localhost:5000/api/threat")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
