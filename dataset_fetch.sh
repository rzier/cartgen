#!/bin/bash


echo "Downloading Dataset From Source..."

set -xe

if [ ! -d "dataset" ]; then
	curl -L -o 20k-album-covers-within-20-genres.zip https://www.kaggle.com/api/v1/datasets/download/michaeljkerr/20k-album-covers-within-20-genres
	unzip -d dataset 20k-album-covers-within-20-genres.zip
	rm "20k-album-covers-within-20-genres.zip"
else 
	echo "Dataset Directory already exist!"
fi
