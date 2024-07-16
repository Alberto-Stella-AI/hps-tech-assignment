#!/bin/bash -e

read -p "Want to install conda env named 'hps'? (y/n)" answer
if [ "$answer" = "y" ]; then
  echo "Installing conda env..."
  conda create -n hps python=3.10 -y
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate hps
  echo "Installing requirements..."
  pip install -r requirements-developer.txt
  python3 -m ipykernel install --user --name=hps
  conda install -c conda-forge --name hps notebook -y
  echo "Installing pre-commit..."
  make install_precommit
  echo "Installation complete!"
else
  echo "Installation of conda env aborted!";
fi
