#!/bin/sh

 

echo "Hello, world!"

git status 

git add --all

NOW=$(date +"%m-%d-%Y")

git commit -m NOW

git push