import pytest
from src.scanner import NetworkScanner
from scapy.all import IP, ICMP, TCP, ARP, Ether
from scapy.sendrecv import sr1, srp
import ipaddress

class TestNetworkScanner:
    @pytest.fixture
    def scanner(self):
        return NetworkScanner(timeout=2)

    def test_icmp_scan_valid_ip(self, scanner):
        result = scanner.icmp_scan("8.8.8.8")
        assert result is True

    def test_icmp_scan_invalid_ip(self, scanner):
        result = scanner.icmp_scan("256.256.256.256")
        assert result is False

    def test_tcp_scan_open_port(self, scanner):
        result = scanner.tcp_scan("127.0.0.1", [80])
        assert result[80] == "open"

    def test_tcp_scan_closed_port(self, scanner):
        result = scanner.tcp_scan("127.0.0.1", [9999])
        assert result[9999] == "closed"

    def test_arp_scan_valid_network(self, scanner):
        result = scanner.arp_scan("192.168.1.0/24")
        assert isinstance(result, list)

    def test_arp_scan_invalid_network(self, scanner):
        result = scanner.arp_scan("256.256.256.0/24")
        assert result is None

    def test_validate_ip_valid(self, scanner):
        assert scanner.validate_ip("192.168.1.1") is True

    def test_validate_ip_invalid(self, scanner):
        assert scanner.validate_ip("256.256.256.256") is False

    def test_validate_network_valid(self, scanner):
        assert scanner.validate_network("192.168.1.0/24") is True

    def test_validate_network_invalid(self, scanner):
        assert scanner.validate_network("256.256.256.0/24") is False 