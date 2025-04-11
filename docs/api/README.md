# NetworkScanner API Documentation

## Overview

The `NetworkScanner` class provides methods for performing various types of network scans including ICMP echo requests, TCP port scanning, and ARP network scanning.

## Class Definition

```python
class NetworkScanner:
    def __init__(self, timeout: int = 2):
        """
        Initialize the NetworkScanner with a timeout value.

        Args:
            timeout (int): Timeout in seconds for network operations (default: 2)
        """
```

## Methods

### icmp_scan

```python
def icmp_scan(self, target: str) -> bool:
    """
    Perform ICMP echo request (ping) scan on a target IP.

    Args:
        target (str): Target IP address to scan

    Returns:
        bool: True if host is up, False otherwise
    """
```

### tcp_scan

```python
def tcp_scan(self, target: str, ports: List[int]) -> Dict[int, str]:
    """
    Perform TCP SYN scan on specified ports.

    Args:
        target (str): Target IP address to scan
        ports (List[int]): List of ports to scan

    Returns:
        Dict[int, str]: Dictionary mapping port numbers to their status
                        Status can be: "open", "closed", "filtered", or "error"
    """
```

### arp_scan

```python
def arp_scan(self, network: str) -> List[Dict[str, str]]:
    """
    Perform ARP scan on a network.

    Args:
        network (str): Network address with subnet (e.g., "192.168.1.0/24")

    Returns:
        List[Dict[str, str]]: List of dictionaries containing IP and MAC addresses
                             of discovered hosts
    """
```

### scan_network

```python
def scan_network(self, target: str, scan_type: str = "all", ports: Optional[List[int]] = None) -> Dict:
    """
    Perform comprehensive network scan.

    Args:
        target (str): Target IP address or network
        scan_type (str): Type of scan to perform ("all", "icmp", "tcp", or "arp")
        ports (Optional[List[int]]): List of ports to scan (required for TCP scan)

    Returns:
        Dict: Dictionary containing scan results for each type of scan performed
    """
```

## Usage Examples

### Basic ICMP Scan

```python
scanner = NetworkScanner()
result = scanner.icmp_scan("192.168.1.1")
print(f"Host is {'up' if result else 'down'}")
```

### TCP Port Scan

```python
scanner = NetworkScanner()
ports = [80, 443, 8080]
results = scanner.tcp_scan("192.168.1.1", ports)
for port, status in results.items():
    print(f"Port {port}: {status}")
```

### ARP Network Scan

```python
scanner = NetworkScanner()
hosts = scanner.arp_scan("192.168.1.0/24")
for host in hosts:
    print(f"IP: {host['ip']}, MAC: {host['mac']}")
```

### Comprehensive Scan

```python
scanner = NetworkScanner()
results = scanner.scan_network(
    target="192.168.1.1",
    scan_type="all",
    ports=[80, 443, 8080]
)
```

## Error Handling

All methods include error handling and will:

-   Return appropriate default values on error
-   Print error messages to stdout
-   Handle network timeouts gracefully
-   Validate input parameters

## Notes

-   Running the scanner requires root/administrator privileges
-   Some networks may block certain types of scans
-   Be mindful of network policies and legal considerations when scanning
