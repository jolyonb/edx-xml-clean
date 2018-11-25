# -*- coding: utf-8 -*-
"""
errors.py

Routines to report on errors found in a course
"""

def report_errors(errorstore):
    """Gives a simple report of all errors that were found"""
    if errorstore.errors:
        for error in errorstore.errors:
            print(f"{error.level} ({error.filename}): {error.description} ({error.name})")
    else:
        print("No errors found!")