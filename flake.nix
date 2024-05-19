{
  description = "Sphinx Python shell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      with nixpkgs.legacyPackages.${system};

      let
        pyPkgs = p: with p; [
          sphinx
          sphinx-rtd-theme
        ];

        devShells.default = mkShell {
          name = "sphinx";
          buildInputs = [ (python3.withPackages pyPkgs) ];
        };

      in {
        inherit devShells;
      }
    );
}
