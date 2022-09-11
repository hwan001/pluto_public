#!/bin/bash
source ./docker_properties.sh

#docker run -it --network=host ${imagename}:${run_version}
docker run -it --network=host "hwan001/pluto:latest"