"""
functions.py
Includes all the necessary functions
to process CSV files and form JSON output
"""

import sys
from os import path
import pandas as pd

def printHelp():
    """print help message"""
    print("Usage: python %s [courses.csv] [students.csv] [tests.csv] [marks.csv] [output.json]\n" % sys.argv[0])

def validateExistence(filename):
    """check if a given file exists"""
    if not path.isfile(filename):
        print("\nError: file \"%s\" does not exist." % filename)
        printHelp()
        sys.exit(1)
    return True
    
def validateFormat(filename, suffix):
    """check if a file's suffix is valid"""
    if not filename.endswith(suffix):
        print("\nError: file %s has invalid file type. Should end with \"%s\"" % (filename,suffix))
        printHelp()
        sys.exit(1)
    return True

def checkInput():
    """parse commandline arguments"""
    argc = len(sys.argv)
    # check if number of arguments is valid
    if argc!=6:
        print("\nError: arguments missing")
        printHelp()
        sys.exit(1) 

    # check each argument for existence and format
    for i in range(1,argc-1):
        validateExistence(sys.argv[i])
        validateFormat(sys.argv[i], ".csv")

    # check output file format
    validateFormat(sys.argv[-1], ".json")
    return sys.argv[1:-1], sys.argv[-1]

def checkCourseWeight(tests):
    """check if each course's weight sum up to 100"""
    sums = tests.groupby('course_id')['weight'].sum().to_numpy()
    return (sums==100).all()

def getDataFrames(inputfiles):
    """read all csv files into dataframes"""
    courses = pd.read_csv(inputfiles[0])
    students = pd.read_csv(inputfiles[1])
    tests = pd.read_csv(inputfiles[2])
    marks = pd.read_csv(inputfiles[3])
    return courses, students, tests, marks

def generateScoreStats(students, tests, marks):
    """calculate courseAverage and totalAverage, and store them in dataframes"""
    # merge useful columns into a single dataframe
    temp = pd.merge(students[['id']], marks.set_index('student_id'),left_on="id", right_index=True)
    temp = temp.merge(tests.set_index('id'), left_on="test_id",right_index=True).drop(['test_id'],axis=1)
    
    # calculate weighted score for each student's courses
    temp['weighted_mark'] = temp.mark * (temp.weight*0.01)

    # calculate courseAverage and totalAverage
    temp['courseAverage'] = temp.groupby(['id','course_id'])['weighted_mark'].transform('sum')
    temp = temp[["id","course_id","courseAverage"]].drop_duplicates(subset=["id","course_id"])
    temp['totalAverage'] = temp.groupby(['id'])['courseAverage'].transform('mean')

    # extract results to separate dataframes
    courseAvg = temp[['id','course_id','courseAverage']].sort_values(by=['id','course_id']).reset_index(drop=True)
    totalAvg = temp[['id','totalAverage']].drop_duplicates(subset=['id']).reset_index(drop=True)
    return courseAvg, totalAvg

def generateDict(courses, students, courseAvg, totalAvg):
    """generate the output dictionary for JSON file"""
    outputDict = {}
    studentList = []
    for studentIdx in range(students.shape[0]):
        studentDict = buildStudentDict(courses, students, courseAvg, totalAvg, studentIdx)
        studentList.append(studentDict)
    outputDict["students"] = studentList
    return outputDict

def buildStudentDict(courses, students, courseAvg, totalAvg, studentIdx):
    """generate nested dictionary for each student"""
    studentDict = {}
    studentDict["id"] = students.loc[studentIdx,"id"].item()
    studentDict["name"] = students.loc[studentIdx,"name"].lstrip(' ').strip()
    studentDict["totalAverage"] = round(totalAvg.loc[studentIdx,"totalAverage"],2).item()

    # filter out other students and form a dataframe
    subDataframe = courseAvg[courseAvg["id"]==studentDict["id"]]

    courseList = []
    for courseIdx in range(len(subDataframe)):
        courseDict = buildCourseDict(courses, subDataframe, courseIdx)
        courseList.append(courseDict)
    studentDict["courses"] = courseList
    return studentDict

def buildCourseDict(courses, subDataframe, courseIdx):
    """generate nested dictonary for each course by a student"""
    courseDict = {}
    courseDict["id"]=subDataframe.iloc[courseIdx,1].item()
    courseDict["name"]=courses.loc[courses["id"]==courseDict["id"],"name"].values[0].lstrip(' ').strip()
    courseDict["teacher"]=courses.loc[courses["id"]==courseDict["id"],"teacher"].values[0].lstrip(' ').strip()
    courseDict["courseAverage"]=round(subDataframe.loc[subDataframe["course_id"]==courseDict["id"],"courseAverage"].values[0],2).item()
    return courseDict