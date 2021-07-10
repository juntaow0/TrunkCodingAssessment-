"""
unit_tests.py
Tests functions in functions.py
"""
import os
import unittest
import pandas as pd
from functions import *

class TestCases(unittest.TestCase):
    """run tests for functions.py"""

    def test_validateExistence1(self):
        """invalid filename test"""
        filename="non_exist.csv"
        with self.assertRaises(SystemExit) as cm:
            validateExistence(filename)
        self.assertEqual(cm.exception.code, 1)

    def test_validateExistence2(self):
        """valid filename test"""
        filename="testfile.csv"
        with open('testfile.csv', 'w') as filePointer:
            pass
        self.assertTrue(validateExistence(filename))
        os.remove(filename)

    def test_validateFormat1(self):
        """invalid suffix test"""
        filename = "test.psd"
        suffix = ".csv"
        with self.assertRaises(SystemExit) as cm:
            validateFormat(filename,suffix)
        self.assertEqual(cm.exception.code, 1)

    def test_validateFormat2(self):
        """valid suffix test"""
        filename = "test.csv"
        suffix = ".csv"
        self.assertTrue(validateFormat(filename,suffix))

    def test_checkCourseWeight1(self):
        """valid weight test"""
        testData = {'id': [1, 2, 3, 4, 5, 6],
                'course_id':[1, 1, 2, 2, 3, 3], 
                'weight': [10, 90, 30, 70, 5, 95]}
        testDataframe = pd.DataFrame(data=testData)
        self.assertTrue(checkCourseWeight(testDataframe))

    def test_checkCourseWeight2(self):
        """invalid weight test"""
        testData = {'id': [1, 2, 3, 4, 5, 6],
                'course_id':[1, 1, 2, 2, 3, 3], 
                'weight': [10, 88, 30, 70, 5, 95]}
        testDataframe = pd.DataFrame(data=testData)
        self.assertFalse(checkCourseWeight(testDataframe))

if __name__=='__main__':
    unittest.main()