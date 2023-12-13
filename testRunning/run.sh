#!/bin/bash
rm testRunning/solvingTimesO0.txt
rm testRunning/solvingTimesO1.txt
rm testRunning/solvingTimesO2.txt
for i in {5..10}
do
  echo 'instance size of' $i
  for j in {1..20}
  do
    python3 python/generateData.py newdata $i $i
    python3 python/distanceMatrixCalculation.py newdata
    echo 'iteration' $j
    start=`date +%s`
    python3 python/solver.py newdata -O1 1> /dev/null
    end=`date +%s`
    echo $((start-end)) >> testRunning/solvingTimesO1.txt
    start=`date +%s`
    python3 python/solver.py newdata -O2 1> /dev/null
    end=`date +%s`
    echo $((start-end)) >> testRunning/solvingTimesO2.txt
  done
done
for i in {5..9}
do
  echo 'instance size of' $i
  for j in {1..15}
  do
    python3 python/generateData.py newdata $i $i
    python3 python/distanceMatrixCalculation.py newdata
    echo 'iteration' $j
    start=`date +%s`
    python3 python/solver.py newdata -O0 1> /dev/null
    end=`date +%s`
    echo $((start-end)) >> testRunning/solvingTimesO0.txt
  done
done
