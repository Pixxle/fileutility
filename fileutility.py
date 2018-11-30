#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
import os
import re


""" fileutility.py
Simple helper library for locating and manipulating files.
find_files(path:str, file_suffix:str, recursion_depth:int,
    minimum_file_age:datetime, maximum_file_age:datetime) -> list of files[]

path is the root path for the script to start searching, will never look below that path.
Each file that is returned will contain the Path as the root for the file.

file_suffix: Gives you the possibiltiy to only find files ending in suffixes; example: .tar.gz

recursion_depth: Set the maximum depth the search is allowed to traverse down folders.
Default of -1 means it will traverse forever. For only root folder, set it to 0.

minimum_file_age: All files retrieved must be older than this date.
maximum_file_age: All files retrieved must be younger than this date.


find_datetime_named_file(path:str, file_suffix:str, recursion_depth:int, minimum_file_age:datetime, maximum_file_age:datetime, regexp:str) -> list of files[]
path is the root path for the script to start searching, will never look below that path. Each file that is returned will contain the Path as the root for the file.
file_suffix: Gives you the possibiltiy to only find files ending in suffixes; example: .tar.gz
recursion_depth: Set the maximum depth the search is allowed to traverse down folders. Default of -1 means it will traverse forever. For only root folder, set it to 0.
minimum_file_age: All files retrieved must be older than this date.
maximum_file_age: All files retrieved must be younger than this date.
regexp: If you want to provide a custom regexp for fetching dates instead of using those provided you can just use this functionality.

delete_files(files:list, directory_delete:bool) -> None
Files is mandatory and provides the function with the list of files to delete. The files need to be full path or relative path to where the script is running from.
directory_delete is default set to False. If set to True the script will try to delete the file. Raises OSError if the directory is not empty.

----
Raises OSError in case path does not exists or directory is not empty when trying to delete.
Raises TypeError wrong type was provided for any of the input parameters
"""
logger = logging.getLogger(__name__)


def delete_files(files, directory_delete=False):
    ''' Deletes all files provided
        If directory_delete is set to true, python will try to delete the directory the File resides in. Raises OSError if directory is not empty.
    '''
    # Removes each file provided in the list. Splits the string on / and rebuilts it to a string with only directories.
    logger.debug("Starting to delete files: {files}".format(files=files))

    directories = []
    for _file in files:
        logger.debug("Trying to remove {_file}".format(_file=_file))
        os.remove(_file)
        if directory_delete:
            directory = '/'.join(_file.split('/')[0:-1])
            if os.path.isdir(directory):
                logger.debug("Adding directory {_directory} for deletion".format(_directory=directory))
                directories.append(directory)

    if directory_delete:
        # Removing duplicate entries to only try to delete dir once.
        directories = list(set(directories))
        for directory in directories:
            logger.debug("Removing directory {_directory}".format(_directory=directory))
            os.rmdir(directory)


def _input_validation(path, file_suffix, recursion_depth, minimum_file_age, maximum_file_age, regexp):
    logger.debug("Starting input validation")
    if type(path) is not str:
        raise TypeError("unsupported type for path: {current_type} expected 'str'".format(current_type=type(path)))
    if file_suffix and type(file_suffix) is not str:
        raise TypeError("unsupported type for file_suffix: {current_type} expected 'str'".format(current_type=type(file_suffix)))
    if type(recursion_depth) is not int:
        raise TypeError("unsupported type for recursion_depth: {current_type} expected 'int'".format(current_type=type(recursion_depth)))
    if minimum_file_age and type(minimum_file_age) is not datetime.datetime:
        raise TypeError("unsupported type for minimum_file_age: {current_type} expected 'datetime.datetime'".format(current_type=type(minimum_file_age)))
    if maximum_file_age and type(maximum_file_age) is not datetime.datetime:
        raise TypeError("unsupported type for maximum_file_age: {current_type} expected 'datetime.datetime'".format(current_type=type(maximum_file_age)))
    if regexp and type(regexp) is not str:
        raise TypeError("unsupported type for regexp: {current_type} expected 'str'".format(current_type=type(regexp)))
    logger.debug("Input validation completed successfully")


def _filter_files(files, file_suffix, minimum_file_age, maximum_file_age):
    logger.debug("Starting _filter_files")
    if file_suffix:
        logger.debug("File suffix provided. Removing all files not matching {suffix}".format(suffix=file_suffix))
        suffix = [x for x in files if x.endswith(file_suffix)]
        files = [x for x in files if x in suffix]

    if minimum_file_age:
        logger.debug("Minimum file age provided. Removing all files younger than {date}".format(date=minimum_file_age))
        minage = [x for x in files if datetime.datetime.fromtimestamp(os.path.getmtime(x)) <= minimum_file_age]
        files = [x for x in files if x in minage]

    if maximum_file_age:
        logger.debug("Maximum file age provided. Removing all files older than {date}".format(date=maximum_file_age))
        maxage = [x for x in files if datetime.datetime.fromtimestamp(os.path.getmtime(x)) >= maximum_file_age]
        files = [x for x in files if x in maxage]

    return files


def find_files(path, file_suffix=None, recursion_depth=-1, minimum_file_age=None, maximum_file_age=None):
    """ Locates all files below path
        file_suffix defaults to all files, takes a string in the format of .txt, .csv
        recursion_depth defaults to unlimited, can be changed by supplying a int. 0 = only this folder
        minimum_file_age defaults to None, if set returns only files older than this date.
        maximum_file_age defaults to None, if set returns only files younger than this date.
        """
    _input_validation(path, file_suffix, recursion_depth, minimum_file_age, maximum_file_age, None)

    # Instead of os.walk we scan folders ourselfs using os.listdir. We then iterate through each folder until maximum recursion depth is reached in each folder.
    def do_scan(start_dir, recursion_depth, depth=0):
        logger.debug("Scanning directories. Current depth: {depth}. Folder: {folder}.".format(depth=depth, folder=start_dir))
        scan = [os.path.join(start_dir, x) for x in os.listdir(start_dir)]
        found_files = [x for x in scan if os.path.isfile(x)]

        if recursion_depth == -1 or depth < recursion_depth:
            logger.debug("Maximum recursion depth not reached. Continuing down the file tree.")
            [found_files.extend(do_scan(x, recursion_depth, depth+1)) for x in scan if os.path.isdir(x)]
        return found_files

    found_files = do_scan(path, recursion_depth)
    logger.debug("All files found before filter is applied: {files}".format(files=found_files))
    return _filter_files(found_files, file_suffix, minimum_file_age, maximum_file_age)


def _determine_dates(year, month, date, hour, minutes, seconds, miliseconds):
        logger.debug("Starting trying to determine date")
        month = month.lower()
        if 'jan' in month:
            month = 1
        elif 'feb' in month:
            month = 2
        elif 'mar' in month:
            month = 3
        elif 'apr' in month:
            month = 4
        elif month == 'may':
            month = 5
        elif 'jun' in month:
            month = 6
        elif 'jul' in month:
            month = 7
        elif 'aug' in month:
            month = 8
        elif 'sep' in month:
            month = 9
        elif 'oct' in month:
            month = 10
        elif 'nov' in month:
            month = 11
        elif 'dec' in month:
            month = 12

        year = int(year)
        month = int(month)
        date = int(date)
        hour = int(hour)
        minutes = int(minutes)
        seconds = int(seconds)
        miliseconds = int(miliseconds)*1000

        # This is our way to determine what a date it is, if it is provided in the yy format.
        # If the year found is less than 1000, it means that the year is in a yy format, where 18 would translate to 2018 and 98 would translate to 1998
        if year < 1000:
            if year > 50:
                year = 1900 + year
            else:
                year = 2000 + year

        return datetime.datetime(year, month, date, hour, minutes, seconds, miliseconds)


def _filter_datetime_named_files(files, file_suffix, minimum_file_age, maximum_file_age, regexp):
    if file_suffix:
        logger.debug("File suffix provided. Removing all files not matching {suffix}".format(suffix=file_suffix))
        suffix = [x for x in files if x.endswith(file_suffix)]
        files = [x for x in files if x in suffix]

    if not regexp:
        logger.debug("No custom regexp provided. Using existing regexps")
        regexp = [
            r'([0-9]{4})[\-\.\_\ ]?([0-9]{1,2})[\-\.\_\ ]?([0-9]{1,2})',                                                                                # yyyy-mm-dd
            r'([0-9]{2})[\-\.\_\ ]?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\-\.\_\ ]?([0-9]{1,2})',                                           # yyMondd
            r'([0-9]{4})[\-\.\_\ ]?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\-\.\_\ ]?([0-9]{1,2})',                                           # yyyyMondd
            r'([0-9]{2})[\-\.\_\ ]?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\.\_\ ]?([0-9]{1,2})',                                           # yymondd
            r'([0-9]{4})[\-\.\_\ ]?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\-\.\_\ ]?([0-9]{1,2})',                                           # yyyymondd
            r'([0-9]{4})[\-\.\_\ ]?(Januari|February|March|April|May|June|July|August|September|October|November|December)[\-\.\_\ ]?([0-9]{1,2})',     # yyyyMondd
            r'([0-9]{2})[\-\.\_\ ]?(Januari|February|March|April|May|June|July|August|September|October|November|December)[\-\.\_\ ]?([0-9]{1,2})',     # yyMondd
            r'([0-9]{4})[\-\.\_\ ]?(januari|february|march|april|may|june|july|august|september|october|november|decemeber)[\-\.\_\ ]?([0-9]{1,2})',    # yyyymondd
            r'([0-9]{2})[\-\.\_\ ]?(januari|february|march|april|may|june|july|august|september|october|november|decemeber)[\-\.\_\ ]?([0-9]{1,2})',    # yymondd
            r'([0-9]{4})\-([0-9]{2})\-([0-9]{2})\T([0-9]{2})\:([0-9]{2})\:([0-9]{2})\.([0-9]{3})',                                                      # Javascript
        ]
        logger.debug("Existing regexps: {regexp}".format(regexp=regexp))
        regexp = [re.compile(x) for x in regexp]

    else:
        logger.debug("Custom regexp provided, compiling: {regexp}".format(regexp=regexp))
        regexp = [re.compile(regexp)]

    to_be_filtered = []
    for _file in files:
        name = _file.split('/')[-1]
        for reg in regexp:
            result = re.search(reg, name)
            if result:
                # Creating the datetime object. If the object contained group 4-7 it was provided in a Javascript timestamp format such as : 2010-10-10T10:10:10.100
                logger.debug("Creating datetime obj for {_file}".format(_file=_file))
                _file_date = _determine_dates(
                    (result.group(1) if len(result.groups()) >= 1 else 0),
                    (result.group(2) if len(result.groups()) >= 2 else 0),
                    (result.group(3) if len(result.groups()) >= 3 else 0),
                    (result.group(4) if len(result.groups()) >= 4 else 0),
                    (result.group(5) if len(result.groups()) >= 5 else 0),
                    (result.group(6) if len(result.groups()) >= 6 else 0),
                    (result.group(7) if len(result.groups()) >= 7 else 0)
                    )
                logger.debug("Datetime for {_file} is {_date}".format(_file=_file, _date=_file_date))

                if minimum_file_age and _file_date > minimum_file_age or maximum_file_age and _file_date < maximum_file_age:
                    logger.debug("Minimum age or Maximum age provided and file: {_file} is out side the scope".format(_file=_file))
                    to_be_filtered.append(_file)

                break

        else:
            logger.debug("Unable to determine date for {_file}. Adding it to the list of files should be filtered out.".format(_file=_file))
            to_be_filtered.append(_file)

    for _file in to_be_filtered:
        if _file in files:
            files.remove(_file)

    return files


def find_datetime_named_files(path, file_suffix=None, recursion_depth=-1, minimum_file_age=None, maximum_file_age=None, regexp=None):
    """ Locates all files below path
    file_suffix if provided all files not ending with this pattern will be filtered out.
    recursion_depth defaults to unlimited, if provided will only look n folders deep for files.
    minimum_file_age defaults to None, if set returns only files older than this date.
    maximum_file_age defaults to None, if set returns only files younger than this date.
    regexp, will use own list of date regexps if none provided.
    """
    _input_validation(path, file_suffix, recursion_depth, minimum_file_age, maximum_file_age, regexp)

    def do_scan(start_dir, recursion_depth, depth=0):
        logger.debug("Scanning directories. Current depth: {depth}. Folder: {folder}.".format(depth=depth, folder=start_dir))
        scan = [os.path.join(start_dir, x) for x in os.listdir(start_dir)]
        found_files = [x for x in scan if os.path.isfile(x)]

        if recursion_depth == -1 or depth < recursion_depth:
            logger.debug("Maximum recursion depth not reached. Continuing down the file tree.")
            [found_files.extend(do_scan(x, recursion_depth, depth+1)) for x in scan if os.path.isdir(x)]
        return found_files

    found_files = do_scan(path, recursion_depth)
    logger.debug("All files found before filter is applied: {files}".format(files=found_files))
    return _filter_datetime_named_files(found_files, file_suffix, minimum_file_age, maximum_file_age, regexp)
