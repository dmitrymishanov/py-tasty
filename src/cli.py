from pathlib import Path

import click
from click import Path as PathParam

from src.suite import Suite


@click.command()
@click.argument('path', type=PathParam(exists=True, path_type=Path))
def run(path: Path) -> None:
    suite = Suite.from_path(path)
    suite.run()
    print(f'Success: {suite.success}, Failures: {suite.failure}, Errors: {suite.errors}')
