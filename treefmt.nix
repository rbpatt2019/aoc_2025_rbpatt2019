_: {
  projectRootFile = "flake.nix";
  programs.nixfmt.enable = true;
  programs.deadnix.enable = true;
  programs.statix.enable = true;
  programs.mdformat.enable = true;
  programs.taplo.enable = true;
  programs.ruff-format.enable = true;
  programs.ruff-check.enable = true;
}
