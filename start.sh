#!/bin/bash

if [ -f ./errors.log ]; then
    rm errors.log
fi

# Launch docker-compose
echo "----- Run docker-compose -----"
docker-compose up --build -d
