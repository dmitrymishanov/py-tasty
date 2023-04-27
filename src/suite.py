import importlib
import os
from dataclasses import dataclass, field
from inspect import getmembers, isfunction
from pathlib import Path

from src.case import Case, CaseStatus


@dataclass
class Suite:
    cases: list[Case] = field(default_factory=list)
    ran: bool = False
    success: int = 0
    failure: int = 0
    errors: int = 0

    @classmethod
    def from_path(cls, path: Path) -> 'Suite':
        cases: list[Case] = []
        for path, subdirs, files in os.walk(path):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    module = importlib.import_module(str(Path(f'{path}/{file}')).replace('/', '.').replace('.py', ''))
                    for name, member in getmembers(module):
                        if name.startswith('test_') and isfunction(member):
                            cases.append(Case(member))
        return cls(cases=cases)

    def run(self) -> None:
        for case in self.cases:
            case.run()
            if case.status is CaseStatus.success:
                self.success += 1
            elif case.status is CaseStatus.failed:
                self.failure += 1
            elif case.status is CaseStatus.error:
                self.errors += 1

        self.ran = True
