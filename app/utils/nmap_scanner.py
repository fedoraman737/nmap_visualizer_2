import subprocess
import xml.etree.ElementTree as ET
import tempfile
import os
import json

class NmapScanner:
    """
    A class to handle running nmap scans and parsing results
    """
    
    @staticmethod
    def run_scan(target, scan_type="basic"):
        """
        Run an nmap scan and return structured results
        
        Args:
            target (str): IP or hostname to scan
            scan_type (str): Type of scan to run (basic, service, os)
            
        Returns:
            dict: Structured scan results
        """
        # Create temporary file for XML output
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp:
            xml_output = tmp.name
            
        try:
            # Build nmap command based on scan type
            if scan_type == "basic":
                cmd = ["nmap", "-sn", "-oX", xml_output, target]
            elif scan_type == "service":
                cmd = ["nmap", "-sV", "-oX", xml_output, target]
            elif scan_type == "os":
                cmd = ["nmap", "-O", "-oX", xml_output, target]
            else:
                cmd = ["nmap", "-oX", xml_output, target]
                
            # Run the nmap command
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            # Parse the XML output
            results = NmapScanner.parse_xml(xml_output)
            
            # Return structured results
            return {
                "status": "success" if process.returncode == 0 else "error",
                "message": "Scan completed successfully" if process.returncode == 0 else stderr.decode('utf-8'),
                "data": results
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": str(e),
                "data": {}
            }
        finally:
            # Clean up the temporary file
            if os.path.exists(xml_output):
                os.remove(xml_output)
    
    @staticmethod
    def parse_xml(xml_file):
        """
        Parse nmap XML output into structured format
        
        Args:
            xml_file (str): Path to XML file
            
        Returns:
            dict: Structured data from the XML
        """
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Extract hosts information
            hosts = []
            
            for host in root.findall('./host'):
                host_info = {"ports": []}
                
                # Get address
                address = host.find('./address')
                if address is not None and address.get('addrtype') == 'ipv4':
                    host_info['ip'] = address.get('addr')
                
                # Get hostname if available
                hostname_elem = host.find('./hostnames/hostname')
                if hostname_elem is not None:
                    host_info['hostname'] = hostname_elem.get('name')
                    
                # Get status
                status = host.find('./status')
                if status is not None:
                    host_info['status'] = status.get('state')
                
                # Get ports and services
                for port in host.findall('./ports/port'):
                    port_info = {
                        'port': int(port.get('portid')),
                        'protocol': port.get('protocol')
                    }
                    
                    # Get port state
                    state = port.find('./state')
                    if state is not None:
                        port_info['state'] = state.get('state')
                    
                    # Get service if available
                    service = port.find('./service')
                    if service is not None:
                        port_info['service'] = service.get('name')
                        if service.get('product'):
                            port_info['product'] = service.get('product')
                        if service.get('version'):
                            port_info['version'] = service.get('version')
                    
                    host_info['ports'].append(port_info)
                
                hosts.append(host_info)
            
            return {"hosts": hosts}
        
        except Exception as e:
            return {"hosts": [], "error": str(e)}

    @staticmethod
    def get_dummy_data():
        """
        Return dummy data for testing when nmap isn't available
        """
        return {
            "hosts": [
                {
                    "ip": "192.168.1.1",
                    "hostname": "router.local",
                    "status": "up",
                    "ports": [
                        {"port": 80, "protocol": "tcp", "state": "open", "service": "http"},
                        {"port": 443, "protocol": "tcp", "state": "open", "service": "https"},
                        {"port": 53, "protocol": "udp", "state": "open", "service": "domain"}
                    ]
                },
                {
                    "ip": "192.168.1.2",
                    "hostname": "desktop.local",
                    "status": "up",
                    "ports": [
                        {"port": 22, "protocol": "tcp", "state": "open", "service": "ssh"},
                        {"port": 3389, "protocol": "tcp", "state": "closed", "service": "ms-wbt-server"}
                    ]
                },
                {
                    "ip": "192.168.1.3",
                    "hostname": "laptop.local",
                    "status": "up",
                    "ports": [
                        {"port": 22, "protocol": "tcp", "state": "open", "service": "ssh"},
                        {"port": 8080, "protocol": "tcp", "state": "open", "service": "http-proxy"}
                    ]
                }
            ]
        } 