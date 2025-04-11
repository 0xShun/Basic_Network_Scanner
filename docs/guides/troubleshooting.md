# Troubleshooting Guide

This guide helps you identify and resolve common issues with the Network Scanner tool.

## Common Issues and Solutions

### 1. Permission Errors

**Symptoms:**

-   "Permission denied" errors
-   Unable to send raw packets
-   Operation not permitted messages

**Solutions:**

1. Run the scanner with root/administrator privileges:
    ```bash
    sudo python src/main.py 192.168.1.1
    ```
2. On Windows, run PowerShell as Administrator
3. Check if your user has necessary network permissions

### 2. Network Connectivity Issues

**Symptoms:**

-   Timeout errors
-   No responses from targets
-   Network unreachable messages

**Solutions:**

1. Verify network connectivity:
    ```bash
    ping 192.168.1.1
    ```
2. Check firewall settings
3. Verify network interface is up and configured
4. Check routing tables

### 3. Port Scanning Issues

**Symptoms:**

-   All ports showing as filtered
-   Inconsistent results
-   Slow scanning

**Solutions:**

1. Adjust timeout values:
    ```bash
    python src/main.py 192.168.1.1 -T 5
    ```
2. Check for firewall interference
3. Verify target system is not rate limiting
4. Try scanning fewer ports at once

### 4. ARP Scanning Issues

**Symptoms:**

-   No hosts found
-   Incomplete results
-   Broadcast not working

**Solutions:**

1. Verify you're on the correct network
2. Check subnet mask:
    ```bash
    python src/main.py 192.168.1.0/24
    ```
3. Ensure network interface supports broadcast
4. Check for network segmentation

### 5. ICMP Scanning Issues

**Symptoms:**

-   Hosts showing as down when they're up
-   Inconsistent ping results
-   No ICMP responses

**Solutions:**

1. Check if ICMP is blocked:
    ```bash
    ping 192.168.1.1
    ```
2. Verify target firewall settings
3. Try different timeout values
4. Check for ICMP rate limiting

## Error Messages

### Common Error Messages and Solutions

1. **"Invalid IP address format"**

    - Solution: Verify IP address format
    - Example: `192.168.1.1` or `192.168.1.0/24`

2. **"No route to host"**

    - Solution: Check network connectivity
    - Verify routing tables
    - Check interface configuration

3. **"Operation not permitted"**

    - Solution: Run with elevated privileges
    - Check user permissions
    - Verify network interface permissions

4. **"Connection timed out"**
    - Solution: Increase timeout value
    - Check network connectivity
    - Verify target is reachable

## Performance Issues

### Slow Scanning

**Causes:**

-   Large port ranges
-   Low timeout values
-   Network congestion
-   System resource limitations

**Solutions:**

1. Reduce port range:
    ```bash
    python src/main.py 192.168.1.1 -p 1-100
    ```
2. Increase timeout:
    ```bash
    python src/main.py 192.168.1.1 -T 5
    ```
3. Schedule scans during off-peak hours
4. Optimize system resources

### High Resource Usage

**Causes:**

-   Too many simultaneous scans
-   Large network ranges
-   System limitations

**Solutions:**

1. Limit scan scope
2. Reduce concurrent operations
3. Monitor system resources
4. Adjust scan parameters

## Debugging Tips

1. **Enable Verbose Output**

    ```bash
    python src/main.py 192.168.1.1 -v
    ```

2. **Check System Logs**

    - Review system logs for errors
    - Check network interface status
    - Monitor system resources

3. **Test Network Connectivity**

    ```bash
    ping 192.168.1.1
    traceroute 192.168.1.1
    ```

4. **Verify Configuration**
    - Check network settings
    - Verify firewall rules
    - Test permissions

## Getting Help

1. **Documentation**

    - Review user guide
    - Check protocol documentation
    - Read security guidelines

2. **Community Support**

    - Check issue tracker
    - Join discussion forums
    - Contact maintainers

3. **Professional Support**
    - Contact network administrators
    - Consult security professionals
    - Get legal advice if needed
