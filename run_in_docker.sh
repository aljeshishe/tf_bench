#!/bin/bash
set -ex

docker build . -t tf_bench
docker run -it tf_bench 
