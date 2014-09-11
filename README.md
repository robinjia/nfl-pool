# NFL Suicide Pool Picker

This is code that makes picks for an NFL Suicide Pool.
Thanks to Renjie You for organizing this pool.

# Setup
Most of this should run out of the box.  One important dependency you may not
already have is cvxpy, which can be installed by following the instructions
[here](http://cvxpy.readthedocs.org/en/latest/install/index.html).

# Basic Execution
From a clean repo, the following should generate a sequence of optimal picks:
```
make
./make-picks [year] [week]
```

For example, to make picks for the first week of the 2014 season, run
```
./make-picks 2014 1
```

This will also create a file data/predictions_${year}_${week}.txt
(e.g. data/predictions_2014_1.txt) that contains estimated winning
probabilities for each team in each week.  The picks the program chooses are
"optimal" in that they maximize expected win count, given these probabilities.
Note that tiebreakers are not taken into account.

# Tests:
* Python tests
To run all Python tests, run
```
cd src/py
./run_all_tests.sh
```

* C tests
To run all C tests, run
```
make check
```

# Data sources
Data on past NFL games comes from <http://pro-football-reference.com>.
