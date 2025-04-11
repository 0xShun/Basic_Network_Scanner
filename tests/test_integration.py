import pytest
from src.scanner import NetworkScanner
import ipaddress
import socket
import time

class TestIntegration:
    @pytest.fixture
    def scanner(self):
        return NetworkScanner(timeout=2)

    def test_complete_scan_localhost(self, scanner):
        results = scanner.scan_network(
            target="127.0.0.1",
            scan_type="all",
            ports=[80, 443]
        )
        
        assert isinstance(results, dict)
        assert "icmp" in results
        assert "tcp" in results
        assert "arp" in results
        
        # ICMP should be True for localhost
        assert results["icmp"] is True
        
        # TCP results should be a dictionary
        assert isinstance(results["tcp"], dict)
        
        # ARP results should be a list
        assert isinstance(results["arp"], list)

    def test_network_scan_local(self, scanner):
        # Get local network
        local_ip = socket.gethostbyname(socket.gethostname())
        network = f"{local_ip}/24"
        
        results = scanner.scan_network(
            target=network,
            scan_type="arp"
        )
        
        assert isinstance(results["arp"], list)
        for host in results["arp"]:
            assert "ip" in host
            assert "mac" in host
            assert ipaddress.ip_address(host["ip"]) in ipaddress.ip_network(network, strict=False)

    def test_scan_known_services(self, scanner):
        # Test scanning common services on localhost
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995]
        results = scanner.scan_network(
            target="127.0.0.1",
            scan_type="tcp",
            ports=common_ports
        )
        
        assert isinstance(results["tcp"], dict)
        for port in common_ports:
            assert port in results["tcp"]
            assert results["tcp"][port] in ["open", "closed", "filtered"]

    def test_scan_large_port_range(self, scanner):
        # Test scanning a range of ports
        start_port = 1
        end_port = 100
        ports = list(range(start_port, end_port + 1))
        
        results = scanner.scan_network(
            target="127.0.0.1",
            scan_type="tcp",
            ports=ports
        )
        
        assert isinstance(results["tcp"], dict)
        assert len(results["tcp"]) == len(ports)
        for port in ports:
            assert port in results["tcp"]

    def test_scan_multiple_networks(self, scanner):
        # Test scanning multiple networks
        networks = ["127.0.0.0/8", "192.168.1.0/24"]
        
        for network in networks:
            results = scanner.scan_network(
                target=network,
                scan_type="arp"
            )
            assert isinstance(results["arp"], list)
            for host in results["arp"]:
                assert ipaddress.ip_address(host["ip"]) in ipaddress.ip_network(network, strict=False)

    def test_scan_performance(self, scanner):
        # Test scanning performance with different timeouts
        timeouts = [1, 2, 5]
        ports = [80, 443]
        
        for timeout in timeouts:
            scanner.timeout = timeout
            start_time = time.time()
            
            results = scanner.scan_network(
                target="127.0.0.1",
                scan_type="tcp",
                ports=ports
            )
            
            elapsed_time = time.time() - start_time
            assert elapsed_time <= (timeout * len(ports) * 1.5)  # Allow 50% margin

    def test_scan_invalid_inputs(self, scanner):
        # Test various invalid inputs
        invalid_inputs = [
            ("invalid_ip", "all", [80]),
            ("256.256.256.256", "all", [80]),
            ("192.168.1.1", "invalid_type", [80]),
            ("192.168.1.1", "tcp", [-1]),
            ("192.168.1.1", "tcp", [70000])
        ]
        
        for target, scan_type, ports in invalid_inputs:
            results = scanner.scan_network(
                target=target,
                scan_type=scan_type,
                ports=ports
            )
            assert isinstance(results, dict)
            assert results["icmp"] is None
            assert results["tcp"] is None
            assert results["arp"] is None

    def test_scan_network_edge_cases(self, scanner):
        # Test edge cases
        edge_cases = [
            ("0.0.0.0", "icmp"),  # Invalid host
            ("255.255.255.255", "icmp"),  # Broadcast address
            ("224.0.0.1", "icmp"),  # Multicast address
            ("::1", "icmp"),  # IPv6 localhost
        ]
        
        for target, scan_type in edge_cases:
            results = scanner.scan_network(
                target=target,
                scan_type=scan_type
            )
            assert isinstance(results, dict)
            assert results["icmp"] is None
            assert results["tcp"] is None
            assert results["arp"] is None

    def test_scan_network_with_different_timeouts(self, scanner):
        # Test scanning with different timeout values
        timeouts = [0.1, 0.5, 1, 2, 5]
        target = "127.0.0.1"
        ports = [80]
        
        for timeout in timeouts:
            scanner.timeout = timeout
            results = scanner.scan_network(
                target=target,
                scan_type="tcp",
                ports=ports
            )
            assert isinstance(results["tcp"], dict)
            assert ports[0] in results["tcp"]

    def test_scan_network_with_large_port_list(self, scanner):
        # Test scanning with a large number of ports
        ports = list(range(1, 101))  # 100 ports
        results = scanner.scan_network(
            target="127.0.0.1",
            scan_type="tcp",
            ports=ports
        )
        
        assert isinstance(results["tcp"], dict)
        assert len(results["tcp"]) == len(ports)
        for port in ports:
            assert port in results["tcp"]
            assert results["tcp"][port] in ["open", "closed", "filtered"] 