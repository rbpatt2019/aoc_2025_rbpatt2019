# adapted from https://github.com/lovesegfault/beautysh/blob/master/flake.nix
{
  description = "hello world application using uv2nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    flake-parts.url = "github:hercules-ci/flake-parts";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs = {
        pyproject-nix.follows = "pyproject-nix";
        nixpkgs.follows = "nixpkgs";
      };
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs = {
        pyproject-nix.follows = "pyproject-nix";
        uv2nix.follows = "uv2nix";
        nixpkgs.follows = "nixpkgs";
      };
    };

    git-hooks.url = "github:cachix/git-hooks.nix";

    treefmt-nix.url = "github:numtide/treefmt-nix";
  };

  outputs =
    inputs@{
      flake-parts,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.treefmt-nix.flakeModule
        inputs.git-hooks.flakeModule
      ];
      systems = [ "aarch64-darwin" ];
      perSystem =
        {
          config,
          lib,
          pkgs,
          ...
        }:
        let
          workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
          overlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel";
          };
          editableOverlay = workspace.mkEditablePyprojectOverlay {
            root = "$REPO_ROOT";
          };
          mkPythonSet =
            python:
            (pkgs.callPackage pyproject-nix.build.packages { inherit python; }).overrideScope (
              lib.composeManyExtensions [
                pyproject-build-systems.overlays.wheel
                overlay
              ]
            );

          pythonSet = mkPythonSet pkgs.python3;
          devPythonSet = pythonSet.overrideScope editableOverlay;

          venv = pythonSet.mkVirtualEnv "aoc_2025" workspace.deps.default;
          buildVenv = pythonSet.mkVirtualEnv "build_aoc_2025" {
            aoc-2025 = [ "build" ];
          };
          devVenv = devPythonSet.mkVirtualEnv "dev_aoc_2025" workspace.deps.all;

          inherit (pkgs.callPackage pyproject-nix.build.util { }) mkApplication;
        in
        {
          packages.default = mkApplication {
            inherit venv;
            package = pythonSet.aoc-2025;
          };

          checks =
            let
              fs = lib.fileset;
              pyproject = fs.unions [
                ./pyproject.toml
                ./uv.lock
              ];
              runCommand =
                name: command:
                pkgs.runCommand name {
                  buildInputs = [ buildVenv ];
                  src = fs.toSource {
                    root = ./.;
                    fileset = pyproject;
                  };
                  postInstall = ''
                    cp -vr . $out
                  '';
                } command;
            in
            {
              # drv is RO, so this will fail if there are updates
              uv-lock = runCommand "uv-lock" ''
                ${buildVenv}/bin/uv lock --project $src \
                --upgrade --no-cache -p ${buildVenv}/bin/python &&
                touch $out
              '';
              uv-audit = runCommand "uv-audit" ''
                ${buildVenv}/bin/uv audit --project $src \
                --preview-features audit-command --no-cache --frozen --no-dev &&
                touch $out
              '';
            };

          devShells.default = pkgs.mkShell {
            packages = [
              devVenv
            ]
            ++ (builtins.attrValues config.treefmt.build.programs)
            ++ config.pre-commit.settings.enabledPackages;

            env = {
              UV_NO_SYNC = "1";
              UV_PYTHON = devPythonSet.python.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              unset PYTHONPATH
              export REPO_ROOT=$(git rev-parse --show-toplevel)
              ${config.pre-commit.installationScript}
            '';
          };

          treefmt = {
            projectRootFile = "flake.nix";
            flakeFormatter = true;
            flakeCheck = false; # handled by pre-commit
            programs = {
              nixfmt.enable = true;
              deadnix.enable = true;
              statix.enable = true;
              ruff-format = {
                enable = true;
                lineLength = 88;
              };
              mdformat.enable = true;
              yamlfmt.enable = true;
              taplo.enable = true;
            };
          };

          pre-commit.settings = {
            package = pkgs.prek;
            hooks = {
              check-added-large-files.enable = true;
              check-merge-conflicts.enable = true;
              end-of-file-fixer.enable = true;
              mixed-line-endings.enable = true;
              trim-trailing-whitespace.enable = true;
              ripsecrets.enable = true;
              treefmt.enable = true;
              flake-checker.enable = true;
              ruff = {
                enable = true;
                entry = lib.mkForce "${devVenv}/bin/ruff check";
              };
              uv-check = {
                enable = true;
                entry = lib.mkForce "${devVenv}/bin/uv check";
                pass_filenames = false;
              };
              nix-flake-check = {
                enable = true;
                entry = "nix flake check --no-warn-dirty .";
                pass_filenames = false;
                stages = [ "pre-push" ];
              };
            };
          };
        };
    };
}
