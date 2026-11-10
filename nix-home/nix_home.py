import os
import re
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
@click.pass_context
def apply_cmd(ctx: click.Context, config_dir: Path):
    nix_path_profile = get_nix_state_home() / "profiles/channels"

    log_step("Applying NIX_PATH")
    try:
        nix_path_generation = get_nix_env_current_generation(
            profile=str(nix_path_profile),
        )
        run_nix_env_set(
            str(config_dir),
            attr="nix-path",
            profile=str(nix_path_profile),
        )
    except subprocess.CalledProcessError:
        ctx.exit(1)

    log_step("Applying user environment")
    try:
        run_nix_env_set(
            str(config_dir),
            attr="user-env",
        )
    except subprocess.CalledProcessError:
        log_warning("Failed to apply, rolling back.")
        try:
            run_nix_env_switch_generation(
                generation=nix_path_generation,
                profile=nix_path_profile,
            )
        except subprocess.CalledProcessError:
            log_error("Failed to roll back, manual cleanup needed!")

        ctx.exit(1)


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


def get_nix_env_current_generation(profile: StrPath | None = None):
    args: list[StrPath] = ["nix-env", "--list-generations"]
    if profile is not None:
        args.extend(["--profile", profile])
    result = subprocess.run(args, check=True, stdout=subprocess.PIPE, text=True)

    match = re.search(r"(\d+).*\(current\)", result.stdout, flags=re.MULTILINE)
    if match is not None:
        return int(match[1])
    raise ValueError("unsupported output of nix-env --list-generations")


def run_nix_env_switch_generation(generation: int, profile: StrPath | None = None):
    args: list[StrPath] = ["nix-env", "--switch-generation"]
    args.append(str(generation))
    if profile is not None:
        args.extend(["--profile", profile])
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


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
    click.echo(
        click.style("==>", fg="blue", bold=True) + " " + text,
        file=sys.stderr,
    )


def log_error(text: str):
    click.echo(
        click.style("error:", fg="red", bold=True) + " " + text,
        file=sys.stderr,
    )


def log_warning(text: str):
    click.echo(
        click.style("warning:", fg="yellow", bold=True) + " " + text,
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
