from typing import Final, LiteralString
import uvicorn
import click


APPMOD: Final[LiteralString] = "eatcryrepeat.main:app"


def _run_app(host: str, port: int, reload: bool) -> None:
    """Run the FastAPI app with uvicorn."""
    uvicorn.run(app=APPMOD, host=host, port=port, reload=reload)


@click.group()
def main() -> None:
    """Eat. Cry. Repeat. CLI."""


@main.command()
@click.option(
    "--host",
    default="0.0.0.0",
    envvar="ECR_HOST",
    help="Host to bind to (can be set with ECR_HOST env variable)",
)
@click.option(
    "--port",
    default=8000,
    envvar="ECR_PORT",
    help="Port to bind to (can be set with ECR_PORT env variable)",
)
@click.option(
    "--reload/--no-reload",
    default=False,
    envvar="ECR_RELOAD",
    help="Enable reload (can be set with ECR_RELOAD env variable)",
)
def run(host: str, port: int, reload: bool) -> None:
    """Run the app in production mode."""
    _run_app(host, port, reload)


@main.command()
@click.option(
    "--host",
    default="127.0.0.1",
    envvar="ECR_HOST",
    help="Host to bind to (can be set with ECR_HOST env variable)",
)
@click.option(
    "--port",
    default=8000,
    envvar="ECR_PORT",
    help="Port to bind to (can be set with ECR_PORT env variable)",
)
@click.option(
    "--reload/--no-reload",
    default=True,
    envvar="ECR_RELOAD",
    help="Enable reload (can be set with ECR_RELOAD env variable)",
)
def dev(host: str, port: int, reload: bool) -> None:
    """Run the app in development mode (reload enabled)."""
    _run_app(host, port, reload)


if __name__ == "__main__":
    main()
