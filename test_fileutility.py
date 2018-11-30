#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
from fileutility import find_datetime_named_file, find_files, delete_files
import datetime
import time
import shutil
import datetime
import pdb
""" test_fileutility.py
Provides the basic test cases for fileutility.py
Will create folders and files on your drive using the python os module, change the timestamps and perform the tests.
""" 
    
test_files = [
    'tests/test1.txt',
    'tests/test1.csv',
    'tests/test1.png',
    'tests/subdir1/test2.txt', 
    'tests/subdir1/test2.csv',
    'tests/subdir3/test2.txt',
    'tests/subdir1/test4-2018Aug17.txt', 
    'tests/subdir1/test4-2018-August-17.txt', 
    'tests/subdir3/test4.2018-August-17.csv', 
    'tests/subdir3/test4-2018-08-17.txt',
    'tests/subdir1/subdir2/test3.txt', 
    'tests/subdir1/subdir2/test3.csv', 
    'tests/subdir3/subdir4/test3.txt', 
    'tests/subdir3/subdir4/test3.csv',
    'tests/subdir1/subdir2/test4_2018_08_17.csv', 
    'tests/subdir1/subdir2/test4.18Aug17.tar.gz',
    'tests/subdir1/subdir2/test4.18Aug19.tar.gz'
]

class TestFindFiles(unittest.TestCase):

    def setUp(self):
        os.makedirs('tests/subdir1/subdir2')
        os.makedirs('tests/subdir3/subdir4')

        for _file in test_files:
            open(_file, 'a').close()

        unixtime = time.mktime(datetime.date(2015,10,10).timetuple())
        unixtime2 = time.mktime(datetime.date(2017,10,10).timetuple())
        os.utime('tests/subdir1/subdir2/test3.txt', (unixtime, unixtime))
        os.utime('tests/test1.txt', (unixtime, unixtime))
        os.utime('tests/subdir1/subdir2/test4_2018_08_17.csv', (unixtime2, unixtime2))

    def tearDown(self):
        shutil.rmtree('tests/')

    def test_find_all(self):
        found_files = find_files('tests/')
        self.assertListEqual(sorted(found_files), sorted(test_files))

    def test_find_root(self):
        found_files = find_files('tests/', recursion_depth=0)
        comp_files = test_files[0:3]
        self.assertListEqual(sorted(found_files), sorted(comp_files))
    
    def test_find_subdir(self):
        found_files = sorted(find_files('tests/', recursion_depth=1))
        comp_files = sorted(test_files[0:10])
        self.assertListEqual(found_files, comp_files)

    def test_find_all_suffix(self):
        found_files = sorted(find_files('tests/', file_suffix='.csv'))
        comp_files = sorted([x for x in test_files if ".csv" in x])
        self.assertListEqual(found_files,comp_files)

    def test_find_younger(self):
        found_files = find_files(path='tests/', maximum_file_age=datetime.datetime(2015,10,11))
        comp_files = test_files
        comp_files.remove('tests/subdir1/subdir2/test3.txt')
        comp_files.remove('tests/test1.txt')
        self.assertListEqual(sorted(found_files),sorted(comp_files))

    def test_find_older(self):
        found_files = find_files(path='tests/', minimum_file_age=datetime.datetime(2015,10,11))
        comp_files = ['tests/subdir1/subdir2/test3.txt', 'tests/test1.txt']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_older_younger(self):
        found_files = find_files(path='tests/', minimum_file_age=datetime.datetime(2017,10,11), maximum_file_age=datetime.datetime(2015,10,9))
        comp_files = ['tests/subdir1/subdir2/test3.txt', 'tests/test1.txt', 'tests/subdir1/subdir2/test4_2018_08_17.csv']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_older_younger_suffix(self):
        found_files = find_files(path='tests/', file_suffix=".csv", minimum_file_age=datetime.datetime(2017,10,11), maximum_file_age=datetime.datetime(2015,10,9))
        comp_files = ['tests/subdir1/subdir2/test4_2018_08_17.csv']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_delete_files(self):
        found_files = find_files(path='tests/subdir1/subdir2/')
        delete_files(found_files)
        found_files = find_files(path='tests/subdir1/subdir2/')
        self.assertListEqual(found_files,[])

    def test_delete_files_and_directory(self):
        found_files = find_files(path='tests/subdir1/subdir2/')
        delete_files(found_files, True)
        with self.assertRaises(OSError):
            find_files(path='tests/subdir1/subdir2/')


class TestFindDatetimeFiles(unittest.TestCase):

    def setUp(self):
        os.makedirs('tests/subdir1/subdir2')
        os.makedirs('tests/subdir3/subdir4')

        for _file in test_files:
            open(_file, 'a').close()

        unixtime = time.mktime(datetime.date(2015,10,10).timetuple())
        unixtime2 = time.mktime(datetime.date(2017,10,10).timetuple())
        os.utime('tests/subdir1/subdir2/test3.txt', (unixtime,unixtime))
        os.utime('tests/test1.txt', (unixtime,unixtime))
        os.utime('tests/subdir1/subdir2/test4_2018_08_17.csv', (unixtime2, unixtime2))

    def tearDown(self):
        shutil.rmtree('tests/')

    def test_find_all(self):
        found_files = find_datetime_named_file('tests/')
        comp_files = ['tests/subdir1/test4-2018Aug17.txt', 'tests/subdir1/test4-2018-August-17.txt', 'tests/subdir3/test4.2018-August-17.csv', 'tests/subdir3/test4-2018-08-17.txt','tests/subdir1/subdir2/test4_2018_08_17.csv', 'tests/subdir1/subdir2/test4.18Aug17.tar.gz','tests/subdir1/subdir2/test4.18Aug19.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_root(self):
        found_files = find_datetime_named_file('tests/subdir1/', recursion_depth=0)
        comp_files = ['tests/subdir1/test4-2018Aug17.txt','tests/subdir1/test4-2018-August-17.txt' ]
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_subdir(self):
        found_files = find_datetime_named_file('tests/subdir1/', recursion_depth=1)
        comp_files = ['tests/subdir1/test4-2018Aug17.txt', 'tests/subdir1/test4-2018-August-17.txt','tests/subdir1/subdir2/test4_2018_08_17.csv', 'tests/subdir1/subdir2/test4.18Aug17.tar.gz','tests/subdir1/subdir2/test4.18Aug19.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))
    
    def test_find_all_suffix(self):
        found_files = find_datetime_named_file('tests/', file_suffix='.tar.gz')
        comp_files = ['tests/subdir1/subdir2/test4.18Aug17.tar.gz','tests/subdir1/subdir2/test4.18Aug19.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_younger(self):
        found_files = find_datetime_named_file(path='tests/', minimum_file_age=datetime.datetime(2018,8,18))
        comp_files = ['tests/subdir1/test4-2018Aug17.txt','tests/subdir1/test4-2018-August-17.txt', 'tests/subdir3/test4.2018-August-17.csv', 'tests/subdir3/test4-2018-08-17.txt','tests/subdir1/subdir2/test4_2018_08_17.csv', 'tests/subdir1/subdir2/test4.18Aug17.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_older(self):
        found_files = find_datetime_named_file(path='tests/', maximum_file_age=datetime.datetime(2018,8,18))
        comp_files = ['tests/subdir1/subdir2/test4.18Aug19.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_older_younger(self):
        found_files = find_datetime_named_file(path='tests/', minimum_file_age=datetime.datetime(2018,8,19), maximum_file_age=datetime.datetime(2018,8,17))
        comp_files = ['tests/subdir1/test4-2018Aug17.txt','tests/subdir1/test4-2018-August-17.txt', 'tests/subdir3/test4.2018-August-17.csv', 'tests/subdir3/test4-2018-08-17.txt','tests/subdir1/subdir2/test4_2018_08_17.csv', 'tests/subdir1/subdir2/test4.18Aug17.tar.gz', 'tests/subdir1/subdir2/test4.18Aug19.tar.gz']
        self.assertListEqual(sorted(found_files),sorted(comp_files))

    def test_find_older_younger_suffix(self):
        found_files = find_datetime_named_file(path='tests/', file_suffix='.tar.gz', minimum_file_age=datetime.datetime(2018,8,19), maximum_file_age=datetime.datetime(2018,8,17))
        comp_files = ['tests/subdir1/subdir2/test4.18Aug19.tar.gz', 'tests/subdir1/subdir2/test4.18Aug17.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_regexp(self):
        found_files = find_datetime_named_file(path='tests/', regexp=r'([0-9]{4})-([0-9]{2})-([0-9]{2})')
        comp_files = ['tests/subdir3/test4-2018-08-17.txt']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_regexp_suffix(self):
        found_files = find_datetime_named_file(path='tests/', file_suffix='.tar.gz', regexp=r'([0-9]{2})[\-]?([a-zA-Z]{3})[\-]?([0-9]{2})')
        comp_files = ['tests/subdir1/subdir2/test4.18Aug19.tar.gz', 'tests/subdir1/subdir2/test4.18Aug17.tar.gz']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

    def test_find_regexp_suffix_no_recursion(self):
        found_files = find_datetime_named_file(path='tests/subdir1/', file_suffix='.txt', recursion_depth=0, regexp=r'([0-9]{4})[\-]?([a-zA-Z]{3,10})[\-]?([0-9]{2})')                                                                                          
        comp_files = ['tests/subdir1/test4-2018-August-17.txt', 'tests/subdir1/test4-2018Aug17.txt']
        self.assertListEqual(sorted(found_files), sorted(comp_files))

if __name__ == '__main__':
    unittest.main()