# drawpia
A simple command line tool for performing draws.

# features
- Performing a draw between unlimited number of entries with different group sizes.
- Ability to set a `restricted_level` for each entry to be able to distribute such 
  entries on different groups without putting two entries with the same restricted 
  level in the same group (if it's not possible, an error would be raised).
- Ability to set an `optional_level` for each entry to be able to try to distribute 
  such entries on different groups without putting two entries with the same optional
  level in the same group (if it's actually possible, otherwise optional level would 
  be ignored).
- Detailed log output during each operation.

# data
You should first fill this file with real data:
- **files/entries.txt**: Contains the name, restricted level and optional level
  of each entry. `restricted_level` and `optional_level` are not mandatory but if you
  choose to provide them, then all entries must have them, otherwise an error would be 
  raised.
  
  Note that all entries must have the same number of parts, these combinations are possible 
  for each entry:
  - `Name`
  - `Name + Restricted Level`
  - `Name + Restricted Level + Optional Level`


  There are two sample files which can be used to get familiar with the data structure:
  - **files/entries.sample1.txt**: Contains a sample data with only `name`.
  - **files/entries.sample2.txt**: Contains a sample data with only `name + restricted level`.

You should also set the desired `GROUP_SIZE` in the `settings` module.
Note that the total entries count must be dividable by the provided group 
size, otherwise an error would be raised.

# run
python3 run.py
