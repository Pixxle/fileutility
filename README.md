# File Utility
Small helper module to easily find files on local file system by different criterias. <br>

<b>WARNING this is still a work in progress. It's only been tested on Mac and Linux</b><br>

## fileutility.py

```
fileutility.py
Simple helper library for locating and manipulating files.
find_files(path:str, file_suffix:str, recursion_depth:int, minimum_file_age:datetime, maximum_file_age:datetime) -> list of files[]
path is the root path for the script to start searching, will never look below that path. Each file that is returned will contain the Path as the root for the file.
file_suffix: Gives you the possibiltiy to only find files ending in suffixes; example: .tar.gz
recursion_depth: Set the maximum depth the search is allowed to traverse down folders. Default of -1 means it will traverse forever. For only root folder, set it to 0.
minimum_file_age: All files retrieved must be older than this date.
maximum_file_age: All files retrieved must be younger than this date.


find_datetime_named_file(path:str, file_suffix:str, recursion_depth:int, minimum_file_age:datetime, maximum_file_age:datetime, regexp:str) -> list of files[]
path is the root path for the script to start searching, will never look below that path. Each file that is returned will contain the Path as the root for the file.
file_suffix: Gives you the possibiltiy to only find files ending in suffixes; example: .tar.gz
recursion_depth: Set the maximum depth the search is allowed to traverse down folders. Default of -1 means it will traverse forever. For only root folder, set it to 0.
minimum_file_age: All files retrieved must be older than this date.
maximum_file_age: All files retrieved must be younger than this date.
regexp: If you want to provide a custom regexp for fetching dates instead of using those provided you can just use this functionality.

----
Raises OSError in case path does not exists
Raises TypeError wrong type was provided for any of the input parameters
```
## test_fileutility.py

```
test_fileutility.py
Provides basic unit test for fileutility.py
Will create folders and files on your drive using the python os module, change the timestamps and perform the tests.

Latest test 2018-11-30:
test_find_all (__main__.TestFindDatetimeFiles) ... ok
test_find_all_suffix (__main__.TestFindDatetimeFiles) ... ok
test_find_older (__main__.TestFindDatetimeFiles) ... ok
test_find_older_younger (__main__.TestFindDatetimeFiles) ... ok
test_find_older_younger_suffix (__main__.TestFindDatetimeFiles) ... ok
test_find_regexp (__main__.TestFindDatetimeFiles) ... ok
test_find_regexp_suffix (__main__.TestFindDatetimeFiles) ... ok
test_find_regexp_suffix_no_recursion (__main__.TestFindDatetimeFiles) ... ok
test_find_root (__main__.TestFindDatetimeFiles) ... ok
test_find_subdir (__main__.TestFindDatetimeFiles) ... ok
test_find_younger (__main__.TestFindDatetimeFiles) ... ok
test_delete_files (__main__.TestFindFiles) ... ok
test_delete_files_and_directory (__main__.TestFindFiles) ... ok
test_find_all (__main__.TestFindFiles) ... ok
test_find_all_suffix (__main__.TestFindFiles) ... ok
test_find_older (__main__.TestFindFiles) ... ok
test_find_older_younger (__main__.TestFindFiles) ... ok
test_find_older_younger_suffix (__main__.TestFindFiles) ... ok
test_find_root (__main__.TestFindFiles) ... ok
test_find_subdir (__main__.TestFindFiles) ... ok
test_find_younger (__main__.TestFindFiles) ... ok

----------------------------------------------------------------------
Ran 21 tests in 0.073s

OK
```

# Installation
<p>Currently i don't provide any out-of-the-box installation such as pip. The easiest way to use this project is to clone it to your existing project and then import as normal</p>