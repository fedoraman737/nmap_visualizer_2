import nmap
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
        try:
            # Initialize the nmap scanner
            nm = nmap.PortScanner()
            
            # Build arguments based on scan type
            if scan_type == "basic":
                arguments = "-sn"  # Ping scan
            elif scan_type == "service":
                arguments = "-sV"  # Service detection
            elif scan_type == "os":
                arguments = "-O"   # OS detection
            else:
                arguments = ""
            
            # Run the scan
            nm.scan(hosts=target, arguments=arguments)
            
            # Parse results to our desired format
            hosts = []
            
            for host in nm.all_hosts():
                host_info = {
                    "ip": host,
                    "status": nm[host].state(),
                    "ports": []
                }
                
                # Add hostname if available
                if 'hostnames' in nm[host] and nm[host]['hostnames']:
                    hostnames = nm[host]['hostnames']
                    if isinstance(hostnames, list) and hostnames:
                        host_info['hostname'] = hostnames[0]['name']
                    elif isinstance(hostnames, dict) and 'name' in hostnames:
                        host_info['hostname'] = hostnames['name']
                
                # Add port information if available
                if 'tcp' in nm[host]:
                    for port, port_data in nm[host]['tcp'].items():
                        port_info = {
                            'port': int(port),
                            'protocol': 'tcp',
                            'state': port_data['state']
                        }
                        
                        if 'name' in port_data:
                            port_info['service'] = port_data['name']
                        if 'product' in port_data:
                            port_info['product'] = port_data['product']
                        if 'version' in port_data:
                            port_info['version'] = port_data['version']
                            
                        host_info['ports'].append(port_info)
                
                # Do the same for UDP if available
                if 'udp' in nm[host]:
                    for port, port_data in nm[host]['udp'].items():
                        port_info = {
                            'port': int(port),
                            'protocol': 'udp',
                            'state': port_data['state']
                        }
                        
                        if 'name' in port_data:
                            port_info['service'] = port_data['name']
                        if 'product' in port_data:
                            port_info['product'] = port_data['product']
                        if 'version' in port_data:
                            port_info['version'] = port_data['version']
                            
                        host_info['ports'].append(port_info)
                
                hosts.append(host_info)
            
            return {
                "status": "success",
                "message": "Scan completed successfully",
                "data": {"hosts": hosts}
            }
            
        except nmap.PortScannerError as e:
            return {
                "status": "error", 
                "message": str(e),
                "data": {}
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": str(e),
                "data": {}
            }
    
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