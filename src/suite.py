from dataclasses import dataclass, field

from src.case import Case, CaseStatus


@dataclass
class Suite:
    cases: list[Case] = field(default_factory=list)
    ran: bool = False
    success: int = 0
    failure: int = 0
    errors: int = 0

    def run(self):
        for case in self.cases:
            case.run()
            if case.status is CaseStatus.success:
                self.success += 1
            elif case.status is CaseStatus.failed:
                self.failure += 1
            elif case.status is CaseStatus.error:
                self.errors += 1

        self.ran = True
