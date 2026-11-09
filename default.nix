let
  sources = import ./npins;

  pkgs = import sources.nixpkgs {
    config = { };
    overlays = [ ];
  };

  nix-home = pkgs.callPackage ./nix-home { };
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
      nix-home
      nixd
      nixfmt
      npins
      shellcheck
      shfmt
    ];
  };

  inherit nix-home;
}
