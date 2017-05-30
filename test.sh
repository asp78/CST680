#!/bin/bash

## This lil script sets up a nice little auction for testing

url='localhost:5000'

curl "$url/addUser/user1/"
curl "$url/addUser/user2/"
curl "$url/addUser/user3/"

curl "$url/makeTrade/user1/0,0,0,0,1/"
curl "$url/makeTrade/user2/0,0,1,2,0/"
curl "$url/makeTrade/user3/0,1,1,2,0/"

curl "$url/closeAuction/"
curl "$url/winningOutcome/2/"
