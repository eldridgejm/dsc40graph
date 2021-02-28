with import <nixpkgs> {};
with python38Packages;

buildPythonPackage rec {
  name = "dsc40graph";
  src = ./.;
  nativeBuildInputs = with python3Packages; [ pytest black ipython jupyter sphinx sphinx_rtd_theme ];
}
