let
  sources = import ./npins;

  pkgs = import sources.nixpkgs {
    config = { };
    overlays = [ ];
  };
in
{
  # NIX_PATH from npins sources.
  nix-path = pkgs.linkFarm "nix-path" {
    inherit (sources)
      nixpkgs
      ;
  };

  # User environment directory tree.
  user-env = pkgs.buildEnv {
    name = "user-env";
    paths = with pkgs; [
      micro
      nixd
      nixfmt
      npins
      shellcheck
      shfmt
    ];
  };
}
