{
  description = "letterbash development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonPackages = pkgs.python312Packages;
        in
        {
          default = pythonPackages.buildPythonApplication {
            pname = "letterbash";
            version = "0.1.0";
            pyproject = true;

            src = pkgs.lib.fileset.toSource {
              root = ./.;
              fileset = pkgs.lib.fileset.unions [
                ./README.md
                ./pyproject.toml
                ./src
              ];
            };

            build-system = [ pythonPackages.hatchling ];
          };
        }
      );

      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python312;
        in
        {
          default = pkgs.mkShell {
            packages = [
              (python.withPackages (pythonPackages: with pythonPackages; [
                hatchling
                mypy
                pytest
                ruff
              ]))
            ];

            shellHook = ''
              export PYTHONPATH="$PWD/src''${PYTHONPATH:+:$PYTHONPATH}"
            '';
          };
        }
      );
    };
}
