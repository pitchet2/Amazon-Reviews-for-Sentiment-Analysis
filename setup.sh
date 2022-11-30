#!/bin/bash


# sudo -u azureuser -i <<'EOF'

PYTHON_VERSION="3.8.1"
if [ -n "$PYTHON_VERSION" ]; then
      echo "Using $PYTHON_VERSION as the Python version to build the kernel"
      conda create --name spacy_MOF python="$PYTHON_VERSION" -y

      eval "$(conda shell.bash hook)"

      conda activate spacy_MOF

      pip install -U pip

      conda install --force-reinstall -y ipykernel

      pip install -r "requirements.txt"
      python -m spacy download en_core_web_lg
      python -m ipykernel install --user --name spacy_MOF --display-name "spacy_MOF ($PYTHON_VERSION)"

else
echo "Unknown Python version"
exit 1
fi     

echo "[$(date)] Done"'!'

# EOF
