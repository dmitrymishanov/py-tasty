from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class CaseStatus(Enum):
    success = 'success'
    failed = 'failed'


@dataclass
class Case:
    content: Callable
    status: CaseStatus | None = None
    ran: bool = False

    def run(self) -> None:
        try:
            self.content()
        except AssertionError as e:
            self.status = CaseStatus.failed
        else:
            self.status = CaseStatus.success
        finally:
            self.ran = True


