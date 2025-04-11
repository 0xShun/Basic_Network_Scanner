from scapy.all import *
import socket
import ipaddress
from typing import List, Dict, Optional, Union
import time

class NetworkScanner:
    def __init__(self, timeout: int = 2):
        self.timeout = timeout

    def icmp_scan(self, target: str) -> bool:
        """
        Perform ICMP echo request (ping) scan on a target IP
        Returns True if host is up, False otherwise
        """
        try:
            # Create ICMP packet
            packet = IP(dst=target)/ICMP()
            # Send packet and wait for response
            response = sr1(packet, timeout=self.timeout, verbose=0)
            return response is not None
        except Exception as e:
            print(f"Error during ICMP scan: {str(e)}")
            return False

    def tcp_scan(self, target: str, ports: List[int]) -> Dict[int, str]:
        """
        Perform TCP SYN scan on specified ports
        Returns dictionary of port:status
        """
        results = {}
        for port in ports:
            try:
                # Create TCP SYN packet
                packet = IP(dst=target)/TCP(dport=port, flags="S")
                # Send packet and wait for response
                response = sr1(packet, timeout=self.timeout, verbose=0)
                
                if response is None:
                    results[port] = "filtered"
                elif response.haslayer(TCP):
                    if response.getlayer(TCP).flags == 0x12:  # SYN-ACK
                        results[port] = "open"
                        # Send RST to close connection
                        rst_packet = IP(dst=target)/TCP(dport=port, flags="R")
                        send(rst_packet, verbose=0)
                    elif response.getlayer(TCP).flags == 0x14:  # RST-ACK
                        results[port] = "closed"
                else:
                    results[port] = "filtered"
            except Exception as e:
                print(f"Error scanning port {port}: {str(e)}")
                results[port] = "error"
        return results

    def arp_scan(self, network: str) -> List[Dict[str, str]]:
        """
        Perform ARP scan on a network
        Returns list of dictionaries containing IP and MAC addresses
        """
        try:
            # Validate network format
            if "/" not in network:
                network = f"{network}/24"  # Default to /24 subnet
            
            # Create ARP request packet
            arp = ARP(pdst=network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            # Send packet and get responses
            result = srp(packet, timeout=self.timeout, verbose=0)[0]
            
            clients = []
            for sent, received in result:
                clients.append({
                    'ip': received.psrc,
                    'mac': received.hwsrc
                })
            return clients
        except Exception as e:
            print(f"Error during ARP scan: {str(e)}")
            return []

    def validate_ip(self, ip: str) -> bool:
        """
        Validate IP address format
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def validate_network(self, network: str) -> bool:
        """
        Validate network format (IP with subnet)
        """
        try:
            ipaddress.ip_network(network, strict=False)
            return True
        except ValueError:
            return False

    def scan_network(self, target: str, scan_type: str = "all", ports: Optional[List[int]] = None) -> Dict:
        """
        Perform comprehensive network scan
        scan_type: "all", "icmp", "tcp", or "arp"
        """
        results = {
            "icmp": None,
            "tcp": None,
            "arp": None
        }

        try:
            # Validate target format
            if not (self.validate_ip(target) or self.validate_network(target)):
                raise ValueError(f"Invalid IP address or network format: {target}")
            
            if scan_type in ["all", "icmp"]:
                results["icmp"] = self.icmp_scan(target)
            
            if scan_type in ["all", "tcp"]:
                if ports is None:
                    print("Warning: No ports specified for TCP scan")
                else:
                    results["tcp"] = self.tcp_scan(target, ports)
            
            if scan_type in ["all", "arp"]:
                results["arp"] = self.arp_scan(target)
            
            return results
        except ValueError as e:
            print(f"Error: {str(e)}")
            return results
        except Exception as e:
            print(f"Error during network scan: {str(e)}")
            return results 