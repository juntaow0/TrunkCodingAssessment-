"""
main.py
Process CSV files and output JSON file
"""

import sys
import json
from functions import *

def main():
    inputfiles, output = checkInput()
    courses, students, tests, marks = getDataFrames(inputfiles)
    if not checkCourseWeight(tests):
        errorOutput={"error": "Invalid course weights"}
        with open(output, 'w',encoding='utf-8') as jsonFile:
            json.dump(errorOutput, jsonFile, ensure_ascii=False, indent=4)
        sys.exit(1)

    courseAvg, totalAvg = generateScoreStats(students, tests, marks)
    outputData = generateDict(courses, students, courseAvg, totalAvg)
    
    with open(output, 'w',encoding='utf-8') as jsonFile:
        json.dump(outputData, jsonFile, ensure_ascii=False, indent=4)
    sys.exit(0)

if __name__ == '__main__':
    main()