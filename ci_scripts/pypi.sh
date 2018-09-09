# Use the miniconda installer for faster download / install of conda
# itself
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
pip install setuptools-golang
setuptools-golang-build-manylinux-wheels --pythons cp35-cp35m,cp36-cp36m --golang 1.10

# Upload wheels
pip install twine
twine upload /dist/
