# Network Protocol Documentation

This document explains the network protocols and scanning techniques used in the Network Scanner project.

## ICMP Scanning

### Overview

ICMP (Internet Control Message Protocol) scanning, commonly known as ping scanning, is used to determine if a host is online and responding to network requests.

### How It Works

1. The scanner sends an ICMP Echo Request (ping) packet to the target
2. If the host is up, it responds with an ICMP Echo Reply
3. If no response is received within the timeout period, the host is considered down

### Technical Details

-   Uses ICMP Type 8 (Echo Request) and Type 0 (Echo Reply)
-   Default timeout: 2 seconds
-   Can be blocked by firewalls or network policies

### Example Packet Structure

```
ICMP Echo Request:
- Type: 8
- Code: 0
- Checksum: [calculated]
- Identifier: [random]
- Sequence Number: [incremental]
```

## TCP Port Scanning

### Overview

TCP port scanning is used to determine which ports are open, closed, or filtered on a target host.

### How It Works

1. The scanner sends a TCP SYN packet to each target port
2. Three possible responses:
    - SYN-ACK: Port is open
    - RST-ACK: Port is closed
    - No response: Port is filtered

### Technical Details

-   Uses TCP SYN scanning (half-open scanning)
-   Sends RST packet to close connections after receiving SYN-ACK
-   Can scan multiple ports simultaneously
-   Default timeout: 2 seconds per port

### Example Packet Structure

```
TCP SYN Packet:
- Source Port: [random]
- Destination Port: [target port]
- Sequence Number: [random]
- Flags: SYN
```

## ARP Scanning

### Overview

ARP (Address Resolution Protocol) scanning is used to discover hosts on a local network by mapping IP addresses to MAC addresses.

### How It Works

1. The scanner sends an ARP request to each IP in the target network
2. Active hosts respond with their MAC addresses
3. The scanner builds a list of IP-MAC address pairs

### Technical Details

-   Works only on local networks
-   Uses broadcast MAC address (ff:ff:ff:ff:ff:ff)
-   Default subnet mask: /24 if not specified
-   Default timeout: 2 seconds

### Example Packet Structure

```
ARP Request:
- Hardware Type: Ethernet (1)
- Protocol Type: IPv4 (0x0800)
- Hardware Size: 6
- Protocol Size: 4
- Opcode: Request (1)
- Sender MAC: [scanner MAC]
- Sender IP: [scanner IP]
- Target MAC: 00:00:00:00:00:00
- Target IP: [target IP]
```

## Protocol Comparison

| Protocol | Scope  | Speed  | Reliability | Stealth |
| -------- | ------ | ------ | ----------- | ------- |
| ICMP     | Global | Fast   | Medium      | Low     |
| TCP      | Global | Medium | High        | Medium  |
| ARP      | Local  | Fast   | High        | Low     |

## Best Practices

1. **ICMP Scanning**

    - Use appropriate timeout values
    - Be aware of ICMP rate limiting
    - Consider network policies

2. **TCP Scanning**

    - Scan common ports first
    - Use appropriate timeout values
    - Be mindful of connection limits

3. **ARP Scanning**
    - Use appropriate subnet masks
    - Consider network size
    - Be aware of ARP cache behavior

## Limitations

1. **ICMP Limitations**

    - May be blocked by firewalls
    - Subject to rate limiting
    - Not always reliable

2. **TCP Limitations**

    - Slower than other methods
    - May trigger security alerts
    - Requires more resources

3. **ARP Limitations**
    - Works only on local networks
    - Requires broadcast capability
    - May be affected by network configuration
