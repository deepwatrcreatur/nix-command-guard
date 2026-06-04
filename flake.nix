{
  description = "Nix-packaged command guardrails for AI coding agents";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (system:
          f {
            pkgs = import nixpkgs { inherit system; };
          });
    in
    {
      formatter = forAllSystems ({ pkgs }: pkgs.nixfmt-rfc-style);

      checks = forAllSystems ({ pkgs }: {
        unit = pkgs.runCommand "nix-command-guard-unit" { } ''
          export PYTHONPATH="${./src}"
          cd ${./.}
          ${pkgs.python3}/bin/python -m unittest discover -s tests -p 'test*.py'
          touch "$out"
        '';
      });

      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            nixfmt-rfc-style
            python3
            ripgrep
          ];
        };
      });
    };
}
