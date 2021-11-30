# ChangeName.py - Created by DMSobol, 3/14/21
# ---------------
# Utility to move file from download folder to Media folder
# renaming file to media server readable format
#
# ----> FUTURE WORK <----------------------
# Add method for .pdf and .epub
# Delete folder after file(s) moved
# Check if folder exists, create if needed
#------------------------------------------

import os
import re
import shutil


# Function to reformat file name
def fixVideoFile(oldName):
    # Determine file extension
    fType = 'skip'
    if oldName.__contains__('.mp4'):
        fType = '.mp4'
    elif oldName.__contains__('.mkv'):
        fType = '.mkv'
    elif oldName.__contains__('.srt'):
        fType = '.srt'
    elif oldName.__contains__('.avi'):
        fType = '.avi'
    else:
        return oldName

    # Match filename format with regex
    oldName = oldName.upper()
    normalShow = re.search(r"S\d\dE\d\d", oldName)
    datedShow = re.search(r'\d\d\d\d\.\d\d\.\d\d', oldName)
    movieFile = re.search(r'[\.\(]\d\d\d\d[\.\)]', oldName)
    videoType = 'Other'

    # Convert to Media server format
    if normalShow is not None:
        startInd, endInd = normalShow.span()  # return indices of match
        showName = oldName[:startInd]
        showName = showName.replace('.', ' ')
        episodeNum = oldName[startInd:endInd]
        newShowFilename = showName + episodeNum
        newShowFilename = newShowFilename.title() + fType  # Capitalize each word, first letter
        videoType = 'TV'
        #  print(newShowFilename)
    elif datedShow is not None:
        startInd, endInd = datedShow.span()
        showName = oldName[:startInd]
        showName = showName.replace('.', ' ')
        colbertDate = 'S' + str(oldName[startInd:startInd + 4]) + 'E' + str(oldName[startInd + 5:startInd + 7]) \
                      + str(oldName[startInd + 8:startInd + 10])
        newShowFilename = showName + colbertDate
        newShowFilename = newShowFilename.title() + fType
        videoType = 'TV'
    elif movieFile is not None:
        # print('MOVIE: ' + oldName)
        startInd, endInd = movieFile.span()
        movieName = str(oldName[:startInd])
        movieName = movieName.replace('.', ' ')
        newShowFilename = movieName.title() + ' (' + str(oldName[startInd + 1:startInd + 5]) + ')' + fType
        videoType = 'Movie'
    else:
        newShowFilename = oldName.title()
    return newShowFilename, videoType


# ------------------------ Main Program ----------------------------
# ******* WINDOWS ********
# sourcePath = r"C:\Users\DMSob\Documents\Vuze Downloads"
# tvDestPath = r"C:\Users\DMSob\Videos\Televise"
# movieDestPath = r"C:\Users\DMSob\Videos\LeFilms"
# ******** MacOS **********

sourcePath = r"/Users/davids/Downloads"
movieDestPath = r"/Volumes/Macintosh HD 1/Users/davidsolo/Movies"
tvDestPath = r"/Volumes/Macintosh HD 1/Users/davidsolo/Movies/Televise"

# Loop through folders in directory, find files with .mkv, .mp4, .srt or .avi extensions
for folderName, subfolders, filenames in os.walk(sourcePath):
    print(" Current Folder: " + folderName)
    for subfolder in subfolders:
        pass
        # print("    Subfolder of " + folderName + ": " + subfolder)

    for filename in filenames:
        # Convert format
        convertedName = fixVideoFile(filename)
        # print(convertedName[0] + " ")  # Returns (newShowFilename, videoType)

        # Move Movie file
        if convertedName[1] == 'Movie':
            # ****** NEED SUBFOLDER FOR SOURCE
            movieFileName = os.path.join(movieDestPath, convertedName[0])
            sourceFileName = os.path.join(folderName, filename)
            print(" Moving :  " + sourceFileName)
            print("     TO : " + movieFileName)
            shutil.move(sourceFileName, movieFileName)
        # Move TV File
        if convertedName[1] == 'TV':
            tvFileName = os.path.join(tvDestPath, convertedName[0])
            sourceFileName = os.path.join(folderName, filename)
            print(" Moving :  " + sourceFileName)
            print("     TO : " + tvFileName)
            shutil.move(sourceFileName, tvFileName)



# --------------- TESTING ARENA -----------------------------
# sampleTVFile = 'South.Park.S24E02.1080p.CC.WEB-DL.AAC2.0.H.264-PARQ.mkv'
# sampleTVFile = 'Stephen.Colbert.2021.03.12.Dr.Anthony.Fauci.720p.WEB.H264-JEBAITED[rarbg].mkv'
# Format of General Movie file: Name.YYYY.&|###.Garbage.type

# Find folders in which files should be placed
