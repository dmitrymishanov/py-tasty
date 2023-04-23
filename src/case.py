from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class CaseStatus(Enum):
    success = 'success'
    failed = 'failed'


@dataclass
class Case:
    content: Callable
    ran: bool = False
    status: CaseStatus | None = None
    error: str | None = None

    def run(self) -> None:
        try:
            self.content()
        except AssertionError as e:
            self.status = CaseStatus.failed
            self.error = e.args[0]
        else:
            self.status = CaseStatus.success
        finally:
            self.ran = True


