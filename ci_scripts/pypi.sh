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
docker run --rm --volume /home/travis/gopath/src/github.com/MaxHalford/xgp-python/dist:/dist:rw --user 2000:2000 quay.io/pypa/manylinux1_x86_64:latest bash -o pipefail -euxc 'cd /tmp
curl https://storage.googleapis.com/golang/go1.9.linux-amd64.tar.gz --silent --location | tar -xz
for py in cp35-cp35m cp36-cp36m; do
    "/opt/python/$py/bin/pip" wheel --no-deps --wheel-dir /tmp /dist/*.tar.gz
done
ls *.whl | xargs -n1 --verbose auditwheel repair --wheel-dir /dist
ls -al /dist
'

# Upload wheels
pip install twine
twine upload /dist/
