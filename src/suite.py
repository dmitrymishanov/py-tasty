import importlib
import os
from dataclasses import dataclass, field
from inspect import getmembers, isfunction
from pathlib import Path
from typing import MutableMapping

from src.case import Case, CaseStatus
from src.parametrize import ParametrizedProxy


@dataclass
class Suite:
    cases: list[Case] = field(default_factory=list)
    ran: bool = False
    results: MutableMapping[CaseStatus, int] = field(default_factory=lambda: {s: 0 for s in CaseStatus})

    @classmethod
    def from_path(cls, path: Path) -> 'Suite':
        cases: list[Case] = []
        for path, subdirs, files in os.walk(path):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    module = importlib.import_module(str(Path(f'{path}/{file}')).replace('/', '.').replace('.py', ''))
                    for name, member in getmembers(module):
                        if name.startswith('test_'):
                            if isfunction(member):
                                cases.append(Case(member))
                            elif isinstance(member, ParametrizedProxy):
                                cases.extend(member.cases)
        return cls(cases=cases)

    def run(self, verbose: bool = False) -> None:
        for case in self.cases:
            case.run(verbose=verbose)
            self.results[case.status] += 1
        self.ran = True
