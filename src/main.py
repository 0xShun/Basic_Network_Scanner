#!/usr/bin/env python3

import argparse
from scanner import NetworkScanner
import sys
from typing import List
import ipaddress

def parse_ports(ports_str: str) -> List[int]:
    """Parse port string into list of integers"""
    ports = []
    try:
        for part in ports_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                if not (0 <= start <= 65535 and 0 <= end <= 65535):
                    raise ValueError("Port numbers must be between 0 and 65535")
                if start > end:
                    raise ValueError("Start port must be less than or equal to end port")
                ports.extend(range(start, end + 1))
            else:
                port = int(part)
                if not 0 <= port <= 65535:
                    raise ValueError("Port numbers must be between 0 and 65535")
                ports.append(port)
        return sorted(list(set(ports)))  # Remove duplicates and sort
    except ValueError as e:
        raise ValueError(f"Invalid port format: {str(e)}")

def validate_target(target: str) -> bool:
    """Validate target IP address or network"""
    try:
        # Try to parse as IP address
        ipaddress.ip_address(target)
        return True
    except ValueError:
        try:
            # Try to parse as network
            ipaddress.ip_network(target, strict=False)
            return True
        except ValueError:
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Network Scanner - A tool for analyzing hosts on a network",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "target",
        help="Target IP address or network (e.g., 192.168.1.1 or 192.168.1.0/24)"
    )
    
    parser.add_argument(
        "-t", "--type",
        choices=["all", "icmp", "tcp", "arp"],
        default="all",
        help="Type of scan to perform (default: all)"
    )
    
    parser.add_argument(
        "-p", "--ports",
        help="Ports to scan (e.g., 80,443 or 1-1000)"
    )
    
    parser.add_argument(
        "-T", "--timeout",
        type=int,
        default=2,
        help="Timeout in seconds for each scan (default: 2)"
    )
    
    try:
        args = parser.parse_args()
        
        # Validate target
        if not validate_target(args.target):
            print(f"Error: Invalid target format: {args.target}")
            print("Please provide a valid IP address (e.g., 192.168.1.1) or network (e.g., 192.168.1.0/24)")
            sys.exit(1)
        
        # Validate timeout
        if args.timeout <= 0:
            print("Error: Timeout must be a positive number")
            sys.exit(1)
        
        scanner = NetworkScanner(timeout=args.timeout)
        
        # Parse ports if provided
        ports = None
        if args.ports:
            try:
                ports = parse_ports(args.ports)
            except ValueError as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
        
        # Perform scan
        results = scanner.scan_network(
            target=args.target,
            scan_type=args.type,
            ports=ports
        )
        
        # Print results
        print("\nScan Results:")
        print("=============")
        
        if results["icmp"] is not None:
            status = "UP" if results["icmp"] else "DOWN"
            print(f"\nICMP Scan: Host is {status}")
        
        if results["tcp"] is not None:
            print("\nTCP Port Scan Results:")
            for port, status in sorted(results["tcp"].items()):
                print(f"Port {port}: {status}")
        
        if results["arp"] is not None:
            print("\nARP Scan Results:")
            if results["arp"]:
                print("IP Address\t\tMAC Address")
                print("----------------------------------------")
                for client in sorted(results["arp"], key=lambda x: ipaddress.ip_address(x['ip'])):
                    print(f"{client['ip']}\t\t{client['mac']}")
            else:
                print("No hosts found in the network")
    
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 