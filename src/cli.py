from pathlib import Path

import click
from click import Path as PathParam

from src.case import CaseStatus
from src.suite import Suite


@click.command()
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.argument('path', type=PathParam(exists=True, path_type=Path))
def run(verbose: bool, path: Path) -> None:
    suite = Suite.from_path(path)
    suite.run(verbose=verbose)
    print(f'Success: {suite.results[CaseStatus.success]}, '
          f'Failures: {suite.results[CaseStatus.failed]}, '
          f'Errors: {suite.results[CaseStatus.error]}')
