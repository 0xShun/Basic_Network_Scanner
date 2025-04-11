# Network Scanner

A command-line tool for analyzing hosts on a network using various scanning techniques including ICMP echo requests, TCP port scanning, and ARP scanning. This tool is designed for network administrators and security professionals to assess network configurations and identify potential vulnerabilities.

## Features

-   **ICMP Echo Request (Ping) Scanning**: Quickly check the availability of hosts.
-   **TCP Port Scanning**: Identify open ports and services running on a host.
-   **ARP Network Scanning**: Discover devices on a local network.
-   **Configurable Scan Types and Timeouts**: Customize scans to suit your needs.
-   **Support for Port Ranges**: Scan specific ports or entire ranges.
-   **Detailed Scan Results Output**: Get comprehensive information about each scan.

## Requirements

-   **Python 3.6 or higher**: Ensure you have the correct version of Python installed.
-   **Scapy 2.5.0 or higher**: Required for packet crafting and network interactions.
-   **Root/Administrator Privileges**: Necessary for raw socket operations.

## Installation

1. **Clone the Repository**:

```bash
git clone https://github.com/yourusername/network-scanner.git
cd network-scanner
```

2. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:

```bash
python src/main.py <target> [options]
```

### Examples

1. **Scan a Single Host with All Scan Types**:

```bash
python src/main.py 192.168.1.1
```

2. **Perform Only ICMP Scan**:

```bash
python src/main.py 192.168.1.1 -t icmp
```

3. **Scan Specific Ports**:

```bash
python src/main.py 192.168.1.1 -p 80,443,8080
```

4. **Scan a Port Range**:

```bash
python src/main.py 192.168.1.1 -p 1-1000
```

5. **Scan a Network Subnet**:

```bash
python src/main.py 192.168.1.0/24 -t arp
```

### Command Line Options

-   `target`: Target IP address or network (required)
-   `-t, --type`: Type of scan to perform (choices: all, icmp, tcp, arp; default: all)
-   `-p, --ports`: Ports to scan (e.g., 80,443 or 1-1000)
-   `-T, --timeout`: Timeout in seconds for each scan (default: 2)

## Project Structure

```
network-scanner/
├── src/
│   ├── main.py         # Command-line interface
│   └── scanner.py      # Core scanning functionality
├── tests/              # Test files
├── docs/               # Documentation
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Security Considerations

-   **Intrusive Nature**: This tool performs network scanning which may be considered intrusive.
-   **Permission**: Use only on networks you have permission to scan.
-   **Network Restrictions**: Some networks may block ICMP or ARP requests.
-   **Privileges**: Running the tool requires elevated privileges.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
