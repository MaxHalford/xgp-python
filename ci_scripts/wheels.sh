# Use the miniconda installer for faster download / install of conda
# itself
if [[ $TRAVIS_TAG ]];
    then
    pushd .
    cd
    mkdir -p download
    cd download
    echo "Cached in $HOME/download :"
    ls -l
    echo
    if [[ ! -f miniconda.sh ]]
       then
       wget http://repo.continuum.io/miniconda/Miniconda-3.6.0-Linux-x86_64.sh \
           -O miniconda.sh
       fi
    chmod +x miniconda.sh && ./miniconda.sh -b
    cd ..
    export PATH=/home/travis/miniconda/bin:$PATH
    conda update --yes conda
    popd

    # Build wheels
    conda create -n wheelenv --yes python=3.5
    source activate wheelenv
    pip install cibuildwheel==0.8.0
    python --version
    python setup.py --name
    cibuildwheel --output-dir wheelhouse

    # Upload wheels
    pip install twine
    twine upload wheelhouse/*.whl
    fi
