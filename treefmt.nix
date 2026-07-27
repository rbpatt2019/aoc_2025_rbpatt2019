_: {
  projectRootFile = "flake.nix";
  programs = {
    nixfmt.enable = true;
    deadnix.enable = true;
    statix.enable = true;
    actionlint.enable = true;
    mdformat.enable = true;
    taplo.enable = true;
    ruff-format.enable = true;
    ruff-check.enable = true;
  };
}
