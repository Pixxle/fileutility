# Fileutility

File utility is a helper module for locating files on the local file system. It provides functionality to find files based on recursion, min-mtime, max-mtime, file suffix and timestamped filenames with regexp. 

## At a Glance
Installation using pip:

```python
pip install fileutility
```

### Example usages of fileutility:

#### Locate all .txt files
```python
import fileutility

found_files = fileutility.find_files(path='/', file_suffix='.txt')
```

#### Locate all files last modified between 2017-11-30 and 2018-11-30

```python
import fileutility
from datetime import datetime

found_files = fileutility.find_files(
    path='/', 
    minimum_file_age=datetime(2018,11,30), 
    maximum_file_age=datetime(2017,11,30)
)
```

#### Locate all .txt files with dates in filename from 2017-11-30 to 2018-11-30

```python
import fileutility
from datetime import datetime

found_files = fileutility.find_datetime_named_files(
    path='/'
    minimum_file_age=datetime(2018,11,30),
    maximum_file_age=datetime(2017,11,30),
    file_suffix='.txt'
)
```

#### Locate all files in the local folder only

```python
import fileutility

found_files = fileutility.find_files(
    path='/',
    recursion_depth=0
)
```

#### Delete all files in a folder and remove folder
```python
import fileutility

found_files = fileutility.find_files(
    path='/tmp/test/'
)

delete_files(
    files=found_files,
    directory_delete=True
)
```

## Requirements
* Python2.7

<b>Warning. Package has only been tested on Linux and Mac.</b>


## Supported date in filename filters from out of the box:
* yyyy(-.\_)mm(-.\_)dd
* yy(-.\_)Mon(-.\_)dd
* yyyy(-.\_)Mon(-.\_)dd
* yy(-.\_)mon(-.\_)dd
* yyyy(-.\_)mon(-.\_)dd
* yyyy(-.\_)Mon(-.\_)dd
* yy(-.\_)Mon(-.\_)dd
* yyyy(-.\_)mon(-.\_)dd
* yy(-.\_)mon(-.\_)dd
* yyyy-mm-ddTHH:MM:SS

If none of the above regexps provide the filter or isn't specific enough you need to apply you can always write your own:

```python
import fileutility

found_files = fileutility.find_datetime_named_files(
    path='/'
    minimum_file_age=datetime(2018,11,30),
    maximum_file_age=datetime(2017,11,30),
    file_suffix='.txt',
    regexp=r'^myfilename-[a-z]{4,10}([0-9]{2})\@([a-z]{3})\@([0-9]{2})'
)

```

## Unit tests status
```bash
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
Ran 21 tests in 0.075s

OK
```