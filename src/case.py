import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from types import TracebackType
from typing import Any


class CaseStatus(Enum):
    success = 'success'
    failed = 'failed'
    error = 'error'


@dataclass
class Case:
    test_func: Callable
    ran: bool = False
    status: CaseStatus | None = None
    failure_reason: str | None = None
    tb: TracebackType | None = None
    suffix: str = ''
    params: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self):
        if self.suffix:
            return self.test_func.__name__ + '__' + self.suffix
        return self.test_func.__name__

    def run(self, verbose: bool = False) -> None:
        if verbose:
            print(self.name, end='')
        self._run()
        if verbose:
            msg = self.status.name.upper()
            print('.' * (80 - len(self.name) - len(msg)), msg)

    def _run(self) -> None:
        try:
            self.test_func(**self.params)
        except AssertionError as e:
            self.status = CaseStatus.failed
            self.failure_reason = e.args[0]
        except Exception as e:
            self.status = CaseStatus.error
            self.tb = sys.exc_info()[2]
        else:
            self.status = CaseStatus.success
        finally:
            self.ran = True
