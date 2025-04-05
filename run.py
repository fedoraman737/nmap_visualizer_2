#!/usr/bin/env python
import os
import sys

def main():
    # Change to the app directory
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    os.chdir(app_dir)
    
    try:
        # Try to import the Flask app
        sys.path.insert(0, app_dir)
        from app import app
        
        # Run the app
        app.run(debug=True, host='127.0.0.1', port=5000)
    except ImportError as e:
        print(f"Error importing Flask app: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 