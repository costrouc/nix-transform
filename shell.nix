with import <nixpkgs> {};
python3.pkgs.buildPythonPackage {
  name = "env";
  src = ./.;
  propagatedBuildInputs = with python3.pkgs; [
    sly
  ];

  checkInputs = [ python3.pkgs.black python3.pkgs.pytest ];

}
