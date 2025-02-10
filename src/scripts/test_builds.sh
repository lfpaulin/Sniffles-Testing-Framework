#!/bin/bash

# init conda
conda_base

# PYPI
conda create \
    --name build_pypi \
    python=3.10 \
    pysam=0.22.0 \
    python-edlib=1.3.9 \
    psutil=5.9.4 \
    -vv

conda activate build_pypi 

wget https://github.com/lfpaulin/Snifflesv253/archive/refs/tags/v2.5.3.tar.gz
python -m pip install v2.5.3.tar.gz

# CONDA
# condabuild
conda create \
    --name condabuild \
    anaconda-client \
    conda-build \
    -vv

conda activate condabuild  

conda-build sniffles

# DELETE ENVS
conda activate base

conda remove --name build_pypi --all
conda remove --name condabuild --all
