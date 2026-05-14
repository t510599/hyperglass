"""Parsed ping output model."""

# Local
from ..main import HyperglassModel


class PingOutput(HyperglassModel):
    """Post-parsed ping output."""

    output: str
    latency: float
