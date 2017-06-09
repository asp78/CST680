#!/bin/bash

## This lil script sets up a nice little auction for testing

url='localhost:5000'

curl "$url/addUser/1ID" #fail withoutName
curl "$url/addUser/1ID/1Name"
curl "$url/addUser/1ID/1Name" # Test adding fail
curl "$url/addUser/someID/1Name" # Test adding fail
curl "$url/addUser/2ID/2NAME"
curl "$url/addUser/3ID/3NAME"
curl "$url/closeRegistration/"
curl "$url/addUser/4ID/4NAME" # Test adding fail

curl "$url/getPrices/"

curl "$url/getCost/0,0,0,0,1,0,0,0,0,0/"
curl "$url/getCost/0,0,0,0,1,0,0,0,0/"
curl "$url/makeTrade/1ID/0,0,0,0,1,0,0,0,0,0/"
curl "$url/makeTrade/1Name/0,0,0,0,1,0,0,0,0,0/" # Test failure
curl "$url/makeTrade/1ID/0,0,0,0,1,0,0,0,0/" # Test failure
curl "$url/makeTrade/2ID/0,0,1,2,1,2,0,0,0,0/"
curl "$url/makeTrade/3ID/0,1,1,2,0,0,0,0,0,0/"
curl "$url/status/3ID/"
curl "$url/status/4ID/" # Test fail
curl "$url/winningOutcome/2/" #fail to set outcome
curl "$url/closeAuction/"
curl "$url/winningOutcome/2/"
