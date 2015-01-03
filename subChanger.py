#!/usr/bin/python3
# -*- coding: UTF8 -*-
# Author Stéphane Bakelants
# Version 0.1
# Date 9 March 2012

import sys
import os
import re
import datetime

def main():
    # Place the sub and time parameter in variables.
    sub,timeToAdd = getSubAndTime()
    # Create a new subtitle file with the correct time.
    createNewSub(sub,timeToAdd)

# Collect the sub and time parameters given via the command line and check if they are correct.
def getSubAndTime():
    # Check if the user provided 2 arguments, being the subtitle file and time to be added.
    # Note that it is len == 3 because ./subChanger.py also counts as argument.
    if len(sys.argv) == 3:
        # Check if the subtitle file exists on the filesystem
        if not os.path.exists(sys.argv[1]):
            print("The subtitle cannot be found on the system.")
            sys.exit(0)
            
        # Check if the time provided is an integer
        try:
            int(sys.argv[2])
        except ValueError:
            print("The time parameter needs to be of integer type.")
            sys.exit(0)
        return sys.argv[1],sys.argv[2]
    else:
        print("Usage: python subChanger.py location/to/subtitle timeInMilliseconds")
        print("You only need to pass the subtitle file and the time to be added!")
        sys.exit(0)

# Create a new subtitle file with the correct time.
def createNewSub(sub,timeToAdd):
    # append the original filename with .backup
    os.rename(sub,sub+".backup")
    # Open the subtitle file so we can read the lines.
    subFile = open(sub+".backup", "r")
    # Open a new file for the new subtitle and create a list for the lines
    newSubFile = open(sub,"w")
    lines = []
    # Read line per line
    for line in subFile.readlines():
        # Remove the annoying \n character that we get from the readlines() function.
        line = line.rstrip('\n')
        # Check if we are at the line where it tells the time
        if re.match("\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d\:\d\d,\d\d\d",line):
            # Change the time to be correct with createNewTime and append this to lines.
            lines.append(createNewTime(line.split(" --> ")[0],int(timeToAdd)) + " --> " + createNewTime(line.split(" --> ")[1],int(timeToAdd)) + "\n")
        else:
            lines.append(line + "\n")
    # Write the lines array to the file.
    newSubFile.writelines(lines)
    subFile.close()
    newSubFile.close()

# Make the new time
def createNewTime(currentTime,timeToAdd):
    # Split the time on : and place the values in variables
    hours,minutes,seconds = currentTime.split(":")
    # Create a new datetime object with the given hours, minutes and seconds.
    # Also split seconds on , because there is where the milliseconds are and
    # multiply with 1000 so its microseconds. For some reason I can't store the milliseconds.
    # year=1900; the datetime strftime() methods require year >= 1900
    dt = datetime.datetime(1900,1,1,int(hours),int(minutes),int(seconds.split(",")[0]),int(seconds.split(",")[1])*1000)
    # Add the timeToAdd to the time.
    newTime = dt + datetime.timedelta(milliseconds=timeToAdd)
    # Return the new Time but drop the last 3 characters because those are the microseconds.
    return newTime.strftime("%H:%M:%S,%f")[:-3]

if __name__=='__main__':
    main()
    sys.exit(0)
