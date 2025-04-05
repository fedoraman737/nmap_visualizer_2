from flask import Flask, render_template, request, jsonify
import os
import json
import time
from utils.nmap_scanner import NmapScanner

app = Flask(__name__)

# Simple in-memory cache for scan results
scan_cache = {}
CACHE_EXPIRY = 300  # Cache results for 5 minutes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def run_scan():
    """Run nmap scan based on user input and return results"""
    target = request.form.get('target', '')
    scan_type = request.form.get('scan_type', 'basic')
    use_cache = request.form.get('use_cache', 'true') == 'true'
    
    # Check if target is provided
    if not target:
        return jsonify({
            "status": "error",
            "message": "Target IP or hostname is required",
            "data": {}
        })
    
    try:
        # Check cache first if allowed
        cache_key = f"{target}:{scan_type}"
        if use_cache and cache_key in scan_cache:
            cached_result, timestamp = scan_cache[cache_key]
            # Check if cache is still fresh
            if time.time() - timestamp < CACHE_EXPIRY:
                cached_result["message"] = "Results from cache. " + cached_result["message"]
                return jsonify(cached_result)
        
        # For development/testing, you can use dummy data
        # Uncomment this and comment out the real scan for testing without nmap
        # result = {"status": "success", "message": "Test scan complete", "data": NmapScanner.get_dummy_data()}
        
        # Run the actual nmap scan
        result = NmapScanner.run_scan(target, scan_type)
        
        # Cache successful results
        if result["status"] == "success":
            scan_cache[cache_key] = (result, time.time())
            
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error running scan: {str(e)}",
            "data": {}
        })

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    """Clear the scan cache"""
    global scan_cache
    scan_cache = {}
    return jsonify({"status": "success", "message": "Cache cleared"})

if __name__ == '__main__':
    app.run(debug=True) 