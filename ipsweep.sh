#!/bin/bash

for ip in {1..254}
    do
	ping -c 1 $1.$ip | grep "bytes from" | cut -d " " -f 4 | tr -d ":" &
    done
