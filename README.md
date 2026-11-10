# nix-home

Declarative Nix user environment and NIX_PATH.

## Setup

1. Clone nix-home repository and `cd` into it.
2. Build nix-home and run it:
   ```bash
   nix-build -A nix-home
   ./result/bin/nix-home apply .
   ```
3. (Optional) Delete all channels for the current user,
   using `nix-channel --list` and `nix-channel --remove`.

## Usage

- Apply a configuration: `nix-home apply <CONFIG_DIR>`
- Update sources: `cd <CONFIG_DIR> && npins update`
