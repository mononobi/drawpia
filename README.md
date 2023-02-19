# drawpia
A simple command line tool for performing draws.

# features
- Performing a draw between unlimited number of entries with different group sizes.
- Ability to set a `restricted level` for each entry to be able to distribute such 
  entries on different groups without putting two entries with the same restricted 
  level in the same group (if it's not possible, an error would be raised).
- Ability to set an `optional level` for each entry to be able to try to distribute 
  such entries on different groups without putting two entries with the same optional
  level in the same group (if it's not possible, optional level would be ignored).

# data
You should first fill this file with real data:
- **files/entries.txt**: Contains the name, restricted level and optional level
  of each entry. `restricted level` and `optional level` are not mandatory but
  each entry can have them if needed.
  
  These combinations are possible for each entry:
  - `Name`
  - `Name + Restricted Level`
  - `Name + Restricted Level + Optional Level`


  There are three sample files which can be used to get familiar with the data structure:
  - **files/samples/entries.sample1.txt**: Contains a sample data with only `name`.
  - **files/samples/entries.sample2.txt**: Contains a sample data with only `name + restricted level`.
  - **files/samples/entries.sample3.txt**: Contains a sample data with mixed entry structures.

# run
python3 run.py
