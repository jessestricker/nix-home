{
  python3Packages,
  lib,
}:
python3Packages.buildPythonApplication {
  name = "nix-home";
  pyproject = true;
  src = lib.sourceFilesBySuffices ./. [
    ".py"
    ".toml"
  ];

  build-system = with python3Packages; [ hatchling ];
  dependencies = with python3Packages; [ click ];
}
