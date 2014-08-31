# NFL Suicide Pool Picker

This is code that makes picks for an NFL Suicide Pool.
Thanks to Renjie You for organizing this pool.

# Basic Execution
To run from a clean repo, do the following:
```
make
./run.sh [year] [week]
```

For example, to make picks for the first week of the 2014 season, run
```
./run.sh 2014 1
```

You may have to install some depenecies for Python.
These should all be available on pip.

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
