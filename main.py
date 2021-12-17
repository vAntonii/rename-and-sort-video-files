from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from configparser import ConfigParser
from config import default, getRegexLists
import os
from os import path
import time
import utils
import re

# Search file for episode or season
def searchFor(regexes, filename):
    for regex in regexes:
        m = re.search(f'{regex}', filename)
        if not m is None:
            return m.group(1)

# Get file details
def getFileDetails(file, config):
    filestring, file_extension = path.splitext(file)
    error = [None, None, file_extension]
    # Skip temporary and current downloading files, and assume files without extension is directories
    if file_extension == '.tmp' or file_extension == '.opdownload' or not file_extension:
        return error
    
    # If not video file return
    if file_extension != '.mov' and file_extension != '.mkv' and file_extension != '.mp4':
        return error

    # Get regex list
    season_reg, episode_reg = getRegexLists()
    if not season_reg:
        return error

    # Get season
    season = searchFor(season_reg, filestring) or '1'
    # Get Episode
    episode = searchFor(episode_reg, filestring) or filestring
    # Creat filename
    filename = config['filename']['Prefix'] + episode + file_extension
    print(f'(File) Renamed {file} to {filename}')

    return [filename, season, file_extension]


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        for file in os.listdir(dir_to_track):
            if not path.isdir(file):
                filename, season, extension = getFileDetails(file, config)

                if filename:
                    directory = dir_destination + '/Season ' + season
                    file_destination = directory + '/' + filename
                    utils.createDirectory(directory)

                    if path.exists(file_destination):
                        return print(f'(conflict) File {filename} has same name in the {directory}')
                    file_exists = path.isfile(file_destination)

                    while file_exists:
                        file_exists = path.isFile(file_destination)

                    src = dir_to_track + '/' + file
                    if path.isfile(src):
                        new_destination = file_destination
                        os.rename(src, new_destination)
                        print(f'(Moved) {filename} moved from {dir_to_track} to {dir_destination}')


# Varaiables
event_handler = Handler()
observer = Observer()
config = ConfigParser()
config.optionxform = str
config.read('config.ini')

def setup(config, default):
    if not 'directory' in config:
        return utils.createConfig(config, default)
    print('Run setup ? (Y/n)')
    i = input()
    if i != 'Y' and i != 'n' and i != 'y':
        setup(config, default)
    if i == 'Y' or i == 'y':
        utils.createConfig(config, default)


setup(config, default)

# config
dir_to_track = config['directory']['DirectoryToTrack']
dir_destination = config['directory']['DirectoryDestination']

# Change directory to user
os.chdir(config['directory']['HomeDirectory'])
utils.createDirectory(dir_to_track)
utils.createDirectory(dir_destination)

# Monitor path and calls method in response to file system events
observer.schedule(event_handler, dir_to_track, recursive=True)
observer.start()

print('Observing: ' + dir_to_track + '. Destination: ' + dir_destination)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
