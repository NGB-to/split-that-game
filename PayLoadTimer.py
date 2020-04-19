# PayLoadTimer.py

import signal
from json import dump, dumps
from time import sleep, time
from glob import glob
from os import stat, path, sep
from sys import exit
# Linux Target folder to watch
#SRC_FOLDER = '/home/jan/GOG Games/Master of Magic'

# Windows Target folder to watch, overwrites previous SRC_FOLDER
# Use # in front to comment out
#SRC_FOLDER = 'C:\\Games\\Master of Magic'

# --------------------------------------------------------------
STRIP_SRC = True  # Remove src folder path from output, True/False
SRC_CHECK_INTERVAL = 20  # Time to check for file changes in seconds
# --------------------------------------------------------------

signal.signal(signal.SIGINT, signal.default_int_handler)

fileData = {}


def getFolders(rootFolder):
    return glob(f'{rootFolder}{sep}**', recursive=True)


def getFileAtime(targetFile):
    return stat(targetFile).st_atime


def getFileSize(targetFile):
    return path.getsize(targetFile)


def noteChanges(fileDataKeys, fileData, outputFileName):
    try:
        for fileEntry in fileDataKeys:
            accessTime = getFileAtime(fileEntry)
            if fileData['files'][fileEntry]['last'] != accessTime:
                fileData['files'][fileEntry]['time'].append(accessTime)
                fileData['files'][fileEntry]['cnt'] += 1
                fileData['files'][fileEntry]['last'] = accessTime
                print(f'Updated entry: {fileEntry} - {accessTime}')

        sleep(SRC_CHECK_INTERVAL)
        noteChanges(fileDataKeys, fileData, outputFileName)
    except KeyboardInterrupt as e:
        print(f'\nYes my grace.. saving data to: {outputFileName}')
        with open(outputFileName, "w") as outputFile:
            fileData['src_time_end'] = int(time())

            if STRIP_SRC:
                srcFolder = fileData['src_folder']
                del fileData['src_folder']
                jsonData = dumps(fileData)
                jsonData = jsonData.replace(srcFolder, '')
                removalString = srcFolder.replace('\\', '\\\\')
                jsonData = jsonData.replace(removalString, '')
                outputFile.write(jsonData)
            else:
                dump(fileData, outputFile)

        exit(0)


def fillFileData(folders, srcFolder):
    fileData = {}
    fileData['files'] = {}
    fileData['src_folder'] = srcFolder
    fileData['basedir'] = baseFolder[-1]
    fileData['src_time'] = int(time())
    fileData['src_time_start'] = int(time())
    fileData['src_time_end'] = 0

    for folder in folders:
        folderFiles = glob(f"{folder}**")

        for fileEntry in folderFiles:
            accessTime = getFileAtime(fileEntry)
            fileSize = getFileSize(fileEntry)
            fileData['files'][fileEntry] = {
                'time': [], 'cnt': 0,
                'init': accessTime, 'last': accessTime,
                'size': fileSize
            }
    return fileData


# --------------------------------------------------------------
if path.exists('src.txt'):
    with open('src.txt', "r") as inputFile:
        SRC_FOLDER = inputFile.readline()
        SRC_FOLDER = SRC_FOLDER.strip().rstrip(sep)
        print(f'Path to game: "{SRC_FOLDER}"')

        if not path.exists(SRC_FOLDER):
            print(f'Path "{SRC_FOLDER}" does not exist. Exiting.')
            exit(1)

        print("Path found, starting logging.")

        baseFolder = path.split(SRC_FOLDER)
        outputFileName = 'Log_' + baseFolder[-1] + '_' + str(int(time())) + '.json'

        fileData = fillFileData(getFolders(SRC_FOLDER), SRC_FOLDER)
        fileDataKeys = fileData['files'].keys()
        noteChanges(fileDataKeys, fileData, outputFileName)
else:
    print('No file "src.txt" with proper path found. Create "src.txt" and add a valid path.')
    exit(0)