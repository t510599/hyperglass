"""Parse ping latency from plain-text output."""

# Standard Library
import re
import typing as t

# Third Party
from pydantic import PrivateAttr

# Project
from hyperglass.models.data import PingOutput
from hyperglass.util.typing import is_series

# Local
from .._output import OutputPlugin

if t.TYPE_CHECKING:
    # Project
    from hyperglass.models.api.query import Query

    # Local
    from .._output import OutputType

PING_AVERAGE = re.compile(
    r"(?:round-trip|rtt)\s+min/avg/max(?:/(?:stddev|mdev))?\s*=\s*"
    r"(?P<min>\d+(?:\.\d+)?)/(?P<avg>\d+(?:\.\d+)?)/",
    re.IGNORECASE,
)
PING_REPLY = re.compile(r"\btime[=<](?P<time>\d+(?:\.\d+)?)\s*ms\b", re.IGNORECASE)


def parse_ping_latency(output: str) -> t.Optional[float]:
    """Extract average latency in milliseconds from plain-text ping output."""
    average = PING_AVERAGE.search(output)
    if average is not None:
        return float(average.group("avg"))

    replies = [float(match.group("time")) for match in PING_REPLY.finditer(output)]
    if replies:
        return round(sum(replies) / len(replies), 3)

    return None


class PingPlugin(OutputPlugin):
    """Coerce ping output to a structured output with an average latency."""

    _hyperglass_builtin: bool = PrivateAttr(True)
    common: bool = True

    def process(self, output: "OutputType", query: "Query") -> "OutputType":
        """Parse latency from plain-text ping output, if present."""
        if not is_series(output):
            return output

        results = []
        latencies = []
        for each_output in output:
            results.append(each_output)
            latency = parse_ping_latency(each_output)
            if latency is not None:
                latencies.append(latency)

        if latencies:
            latency = round(sum(latencies) / len(latencies), 3)
            return PingOutput(output="\n\n".join(results), latency=latency)
        return output
