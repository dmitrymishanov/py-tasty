import sys
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from types import TracebackType


class CaseStatus(Enum):
    success = 'success'
    failed = 'failed'
    error = 'error'


@dataclass
class Case:
    content: Callable
    ran: bool = False
    status: CaseStatus | None = None
    failure_reason: str | None = None
    tb: TracebackType | None = None

    def run(self) -> None:
        try:
            self.content()
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


