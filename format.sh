#!/bin/bash
# should pipe kmers into this
./permute.py | sort | ./reduce.py
