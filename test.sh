#!/usr/bin/env bash

# exit immediately if a simple command exits with a nonzero exit value
set -e

export PYCOIN_NATIVE=openssl
PEP8=${VIRTUALENV_PATH}pep8
COVERAGE=${VIRTUALENV_PATH}coverage

echo $PEP8
echo $COVERAGE

# ensure pep8
$PEP8 storjnet

# start server
$COVERAGE run --source=storjnet swarm.py & 
PID=$!

# run compatibility tests
bash -c "source <(curl -s https://raw.githubusercontent.com/Storj/storjspec/master/test_storjnet_compatibility.sh)"

# stop server
kill -INT $PID

# report coverage
sleep 1
$COVERAGE report # --fail-under=95
