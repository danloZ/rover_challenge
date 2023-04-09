#!/bin/bash
cd solution

echo "Downloading base image"
docker pull python:3.8-slim-buster

echo "Building application image"
docker build -t rover_challenge:v1.0 .

echo "Running application"
docker run --name wall-e -it rover_challenge:v1.0

echo "Cleaning up"
docker rm wall-e
docker rmi rover_challenge:v1.0

echo "Enjoy!"