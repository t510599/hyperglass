"""Data structure models."""

# Standard Library
from typing import Union

# Local
from .ping import PingOutput
from .bgp_route import BGPRouteTable

OutputDataModel = Union[BGPRouteTable, PingOutput]

__all__ = (
    "BGPRouteTable",
    "OutputDataModel",
    "PingOutput",
)
