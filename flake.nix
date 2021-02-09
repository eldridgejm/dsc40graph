{
  description = "A simple graph library used in DSC40B @ UCSD.";

  inputs.nixpkgs.url = github:NixOS/nixpkgs/20.03;

  outputs = { self, nixpkgs }: 
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
      {
        publish = forAllSystems (system:
          with import nixpkgs { system = "${system}"; };

            python3Packages.buildPythonPackage {
              name = "dsc40graph";
              src = ./.;
              propagatedBuildInputs = with python3Packages; [];
              nativeBuildInputs = with python3Packages; [ pytest black ipython jupyter sphinx sphinx_rtd_theme ];
            }

          );

        defaultPackage = forAllSystems (system:
            self.publish.${system}
          );
      };

}
