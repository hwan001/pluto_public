#!/bin/bash
source ./docker_properties.sh

#echo ${imagename}:${build_version}

docker build --force-rm=false -t ${imagename}:${build_version} .
docker build --force-rm=false -t ${imagename}:latest .