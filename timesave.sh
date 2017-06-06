#!/bin/bash

file1='data.txt'
file2='data2.txt'

while :
do
  tail -n 1 $file1 >> $file2
  sleep 1800
done
