import os
import subprocess
import sys
from pathlib import Path

import click

type StrPath = str | os.PathLike[str]


@click.group()
@click.help_option("--help", "-h")
def main():
    pass


@main.command()
@click.help_option("--help", "-h")
@click.argument("config_dir", type=click.Path(path_type=Path))
def apply_cmd(config_dir: Path):
    nix_path_profile = get_nix_state_home() / "profiles/channels"

    log_step("Applying NIX_PATH")
    run_nix_env_set(
        str(config_dir),
        attr="nix-path",
        profile=str(nix_path_profile),
    )

    log_step("Applying user environment")
    run_nix_env_set(str(config_dir), attr="user-env")


def get_nix_state_home():
    # https://nix.dev/manual/nix/2.35/command-ref/env-common.html
    value = os.getenv("NIX_STATE_HOME")
    if value is not None and value != "":
        return Path(value)
    return get_xdg_state_home() / "nix"


def get_xdg_state_home():
    # https://specifications.freedesktop.org/basedir/0.8/
    value = os.getenv("XDG_STATE_HOME")
    if value is not None and value != "":
        return Path(value)
    return Path.home() / ".local" / "state"


def run_nix_env_set(
    file: StrPath,
    attr: StrPath | None = None,
    profile: StrPath | None = None,
):
    args: list[StrPath] = ["nix-env", "--set"]
    args.extend(["--file", file])
    if attr is not None:
        args.extend(["--attr", attr])
    if profile is not None:
        args.extend(["--profile", profile])
    subprocess.run(args, check=True)


def log_step(text: str):
    click.echo(click.style("==>", fg="blue", bold=True) + " " + text, file=sys.stderr)


if __name__ == "__main__":
    main()
