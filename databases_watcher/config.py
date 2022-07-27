from typing import List
from dataclasses import dataclass, field

from argparse import Namespace

@dataclass
class RunningConfig:
    connection_uri: str
    debug: bool = False

    @classmethod
    def from_argparser(cls, parsed: Namespace):
        return cls(**{k: v for k, v in parsed.__dict__.items() if v is not None})

__all__ = ("RunningConfig", )
