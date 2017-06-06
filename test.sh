#!/bin/bash

## This lil script sets up a nice little auction for testing

url='localhost:5000'

curl "$url/addUser/user1/"
curl "$url/addUser/user1/" # Test adding fail
curl "$url/addUser/user2/"
curl "$url/addUser/user3/"
curl "$url/closeRegistration/"
curl "$url/addUser/user4/" # Test adding fail

curl "$url/getPrices/"

curl "$url/getCost/0,0,0,0,1,0,0,0,0,0/"
curl "$url/getCost/0,0,0,0,1,0,0,0,0/"
curl "$url/makeTrade/user1/0,0,0,0,1,0,0,0,0,0/"
curl "$url/makeTrade/user1/0,0,0,0,1,0,0,0,0/" # Test failure
curl "$url/makeTrade/user2/0,0,1,2,1,2,0,0,0,0/"
curl "$url/makeTrade/user3/0,1,1,2,0,0,0,0,0,0/"
curl "$url/status/user3/"
curl "$url/status/user4/" # Test fail
curl "$url/closeAuction/"
curl "$url/winningOutcome/2/"
