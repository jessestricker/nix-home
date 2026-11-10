{
  lib,
  installShellFiles,
  python3Packages,
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
  nativeBuildInputs = [ installShellFiles ];

  postInstall = ''
    installShellCompletion --cmd nix-home \
      --bash <(_NIX_HOME_COMPLETE=bash_source $out/bin/nix-home)
  '';
}
