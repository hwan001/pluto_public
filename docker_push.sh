#!/bin/bash
source ./docker_properties.sh

#echo ${imagename}:${build_version}

docker push ${imagename}:${build_version}
docker push ${imagename}:latest