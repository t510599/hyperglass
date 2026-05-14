"""Ping output parsing tests."""

# Project
from hyperglass.models.data import PingOutput

# Local
from .._builtin.ping import PingPlugin, parse_ping_latency

PING = """PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: icmp_seq=0 ttl=59 time=4.696 ms
64 bytes from 1.1.1.1: icmp_seq=1 ttl=59 time=4.699 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=59 time=4.640 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=59 time=4.583 ms
64 bytes from 1.1.1.1: icmp_seq=4 ttl=59 time=4.640 ms

--- 1.1.1.1 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 4.583/4.652/4.699/0.043 ms
"""


def test_parse_ping_latency_summary():
    assert parse_ping_latency(PING) == 4.652


def test_parse_ping_latency_summary_without_deviation():
    output = "Success rate is 100 percent, round-trip min/avg/max = 1/2/4 ms"
    assert parse_ping_latency(output) == 2


def test_parse_ping_latency_reply_average():
    output = """
64 bytes from 192.0.2.1: icmp_seq=0 ttl=59 time=4.696 ms
64 bytes from 192.0.2.1: icmp_seq=1 ttl=59 time=4.699 ms
64 bytes from 192.0.2.1: icmp_seq=2 ttl=59 time=4.640 ms
"""
    assert parse_ping_latency(output) == 4.678


def test_ping_plugin_structures_latency_output():
    plugin = PingPlugin()
    query = type("Query", (), {})()

    result = plugin.process(output=(PING,), query=query)

    assert isinstance(result, PingOutput)
    assert result.output == PING
    assert result.latency == 4.652


def test_ping_plugin_preserves_multiple_outputs():
    plugin = PingPlugin()
    query = type("Query", (), {})()

    result = plugin.process(output=(PING, "No latency here"), query=query)

    assert isinstance(result, PingOutput)
    assert result.output == f"{PING}\n\nNo latency here"
    assert result.latency == 4.652


def test_ping_plugin_ignores_non_ping_output():
    plugin = PingPlugin()
    query = type("Query", (), {})()
    output = ("No latency here",)

    assert plugin.process(output=output, query=query) == output
