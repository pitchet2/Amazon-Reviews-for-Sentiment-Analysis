#!/bin/bash
cd ..
cd "textcat_multilabel"
n=1

# Increment $N as long as a directory with that name exists
while [[ -d "models/model-"v."${n}" ]] ; do
    n=$(($n+1))
done
mkdir -p "models/model-"v."${n}"

cd "models/model-"v."${n}"

cp '../../project.yml' .
python -m spacy project run all