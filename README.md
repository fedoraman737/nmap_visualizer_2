# Nmap Network Visualizer

A web-based visualization tool for nmap network scans.

## Features

- Run nmap scans directly from the web interface
- Visualize network topology with D3.js
- Support for different scan types (basic, service detection, OS detection)
- Interactive network graph with node details on hover

## Requirements

- Python 3.7+
- Nmap installed on your system
- Web browser with JavaScript enabled

## Installation

1. Make sure you have nmap installed on your system:
   - Windows: Download and install from [nmap.org](https://nmap.org/download.html)
   - Linux: `sudo apt-get install nmap` (Ubuntu/Debian) or `sudo yum install nmap` (CentOS/RHEL)
   - macOS: `brew install nmap` (using Homebrew)

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/nmap_visualizer.git
   cd nmap_visualizer
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```
   cd app
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

3. Enter an IP address or range (e.g., `192.168.1.0/24`) in the target field

4. Select the scan type and click "Run Scan"

5. View the network visualization and scan results

## Notes

- Running nmap scans may require administrative/root privileges
- For testing without nmap, you can uncomment the dummy data line in app.py
- This tool is for educational and network administration purposes only

## Development

This project was developed with assistance from Claude 3.7 Sonnet AI, which helped generate the initial codebase structure, visualization components, and nmap integration, because for obvious reasons, I need to git gud at doing this myself.

## License

MIT