#!/bin/bash
for i in {0..19}
do
   start python3 work.py $i >> out.txt
done
