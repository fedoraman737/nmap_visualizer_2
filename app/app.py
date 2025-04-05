from flask import Flask, render_template, request, jsonify
import os
import json
from utils.nmap_scanner import NmapScanner

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def run_scan():
    """Run nmap scan based on user input and return results"""
    target = request.form.get('target', '')
    scan_type = request.form.get('scan_type', 'basic')
    
    # Check if target is provided
    if not target:
        return jsonify({
            "status": "error",
            "message": "Target IP or hostname is required",
            "data": {}
        })
    
    try:
        # For development/testing, you can use dummy data
        # Uncomment this and comment out the real scan for testing without nmap
        # result = {"status": "success", "message": "Test scan complete", "data": NmapScanner.get_dummy_data()}
        
        # Run the actual nmap scan
        result = NmapScanner.run_scan(target, scan_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error running scan: {str(e)}",
            "data": {}
        })

if __name__ == '__main__':
    app.run(debug=True) 