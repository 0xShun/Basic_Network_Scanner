# User Guide

This guide provides comprehensive instructions for installing, configuring, and using the Network Scanner tool.

## Installation

### Prerequisites

-   Python 3.6 or higher
-   pip (Python package installer)
-   Root/Administrator privileges
-   Network access

### Step-by-Step Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/network-scanner.git
    cd network-scanner
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Verify Installation**
    ```bash
    python src/main.py --help
    ```

## Configuration

### Basic Configuration

1. **Timeout Settings**

    - Default: 2 seconds
    - Adjust using `-T` or `--timeout` option
    - Example: `python src/main.py 192.168.1.1 -T 5`

2. **Port Ranges**

    - Specify ports using `-p` or `--ports` option
    - Example: `python src/main.py 192.168.1.1 -p 80,443,8080`
    - Range example: `python src/main.py 192.168.1.1 -p 1-1000`

3. **Scan Types**
    - Choose scan type with `-t` or `--type` option
    - Available types: all, icmp, tcp, arp
    - Example: `python src/main.py 192.168.1.1 -t tcp`

## Usage Examples

### Basic Scans

1. **Single Host Scan**

    ```bash
    python src/main.py 192.168.1.1
    ```

2. **Network Scan**

    ```bash
    python src/main.py 192.168.1.0/24
    ```

3. **Port Scan**
    ```bash
    python src/main.py 192.168.1.1 -p 80,443,8080
    ```

### Advanced Usage

1. **Combined Scan**

    ```bash
    python src/main.py 192.168.1.1 -t all -p 1-1000
    ```

2. **Custom Timeout**

    ```bash
    python src/main.py 192.168.1.1 -T 5
    ```

3. **Specific Protocol Scan**
    ```bash
    python src/main.py 192.168.1.1 -t arp
    ```

## Output Interpretation

### ICMP Scan Results

-   `UP`: Host is responding to ICMP requests
-   `DOWN`: Host is not responding to ICMP requests

### TCP Scan Results

-   `open`: Port is accepting connections
-   `closed`: Port is not accepting connections
-   `filtered`: Port status cannot be determined
-   `error`: Error occurred while scanning

### ARP Scan Results

-   Lists all discovered hosts with their IP and MAC addresses
-   Empty list indicates no hosts found

## Best Practices

1. **Scan Planning**

    - Schedule scans during maintenance windows
    - Inform network administrators
    - Document scan objectives

2. **Resource Management**

    - Use appropriate timeout values
    - Limit port ranges
    - Monitor system resources

3. **Security**
    - Obtain proper permissions
    - Document scan results
    - Follow security guidelines

## Common Use Cases

1. **Network Inventory**

    ```bash
    python src/main.py 192.168.1.0/24 -t arp
    ```

2. **Service Discovery**

    ```bash
    python src/main.py 192.168.1.1 -p 80,443,8080
    ```

3. **Host Availability**
    ```bash
    python src/main.py 192.168.1.1 -t icmp
    ```

## Tips and Tricks

1. **Performance Optimization**

    - Use appropriate timeout values
    - Limit port ranges
    - Schedule scans during off-peak hours

2. **Troubleshooting**

    - Check network connectivity
    - Verify permissions
    - Review error messages

3. **Advanced Features**
    - Combine scan types
    - Use custom port ranges
    - Adjust timeout values
