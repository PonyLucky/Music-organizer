"""_summary_
This script will take a directory of music files and organize them into folders.

There are three modes of operation:
- '--artist' will group files by artist
- '--album' will group files by artist/album
- '--all' will group files in one folder

We will organize them using their metadata.
"""

# Module to access files
import os
import sys
# Module to get arguments from the command line
import argparse
# Module to get metadata
import mutagen

def get_params():
    """
    Get the parameters from the command line.
    """
    parser = argparse.ArgumentParser(description='Organize music files.')
    parser.add_argument('-a', '--artist', action='store_true',
                        help='Group files by artist')
    parser.add_argument('-b', '--album', action='store_true',
                        help='Group files by artist/album')
    parser.add_argument('-l', '--all', action='store_true',
                        help='Group files in one folder')
    parser.add_argument('-d', '--directory', type=str,
                        help='Directory to organize')
    args = parser.parse_args()
    
    # Get the mode
    mode = ''
    if args.artist:
        mode = '--artist'
    elif args.album:
        mode = '--album'
    elif args.all:
        mode = '--all'
    args.mode = mode
    
    return args

class MusicOrganizer:
    """_summary_
    This class will organize music files into folders.
    """

    def __init__(self, directory, mode):
        """_summary_
        Initialize the class with the directory to organize.

        :param directory: The directory to organize.
        :type directory: str
        """
        self.directory = directory
        self.files = []
        self.artists = {}
        self.albums = {}
        self.mode = mode

    def get_files(self):
        """_summary_
        Get all files in the directory and their children.

        :return: None
        :rtype: None
        """
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                self.files.append(os.path.join(root, file))
    
    def get_metadata(self, file):
        """_summary_
        Get the metadata from the file.

        :param file: The file to get the metadata from.
        :type file: str
        :return: The metadata.
        :rtype: dict
        """
        metadata = mutagen.File(file)
        return metadata
    
    def get_artist(self, metadata):
        """_summary_
        Get the artist from the metadata.

        :param metadata: The metadata to get the artist from.
        :type metadata: dict
        :return: The artist.
        :rtype: str
        """
        if 'artist' in metadata:
            return metadata['artist'][0]
        else:
            return 'All'
        
    def sort_with_metadata(self):
        """_summary_
        Get the metadata of each file and organize them.

        :return: None
        :rtype: None
        """
        for file in self.files:
            metadata = self.get_metadata(file)
            artist = self.get_artist(metadata)
            if artist not in self.artists:
                self.artists[artist] = []
            self.artists[artist].append(file)
            if self.mode == '--album':
                if artist not in self.albums:
                    self.albums[artist] = {}
                if 'album' in metadata:
                    album = metadata['album'][0]
                    if album not in self.albums[artist]:
                        self.albums[artist][album] = []
                    self.albums[artist][album].append(file)
                else:
                    if 'All' not in self.albums[artist]:
                        self.albums[artist]['All'] = []
                    self.albums[artist]['All'].append(file)

    def organize_files(self):
        """_summary_
        Organize the files.

        :return: None
        :rtype: None
        """
        for artist in self.artists:
            if self.mode == '--artist':
                if artist != 'All':
                    # Create the artist folder if it doesn't exist
                    if not os.path.exists(os.path.join(self.directory, artist)):
                        os.mkdir(os.path.join(self.directory, artist))
                    for file in self.artists[artist]:
                        os.rename(file, os.path.join(self.directory, artist, os.path.basename(file)))
                    # Remove all empty folders in artist folder
                    for root, dirs, files in os.walk(os.path.join(self.directory, artist)):
                        for dir in dirs:
                            if not os.listdir(os.path.join(root, dir)):
                                os.rmdir(os.path.join(root, dir))
            elif self.mode == '--album':
                if artist != 'All':
                    # Create the artist folder if it doesn't exist
                    if not os.path.exists(os.path.join(self.directory, artist)):
                        os.mkdir(os.path.join(self.directory, artist))
                    
                    for album in self.albums[artist]:
                        # Create the artist/album folder if it doesn't exist
                        if not os.path.exists(os.path.join(self.directory, artist, album)):
                            os.mkdir(os.path.join(self.directory, artist, album))
                        for file in self.albums[artist][album]:
                            os.rename(file, os.path.join(self.directory, artist, album, os.path.basename(file)))
            elif self.mode == '--all':
                # Move all files to the root folder
                for file in self.artists[artist]:
                    os.rename(file, os.path.join(self.directory, os.path.basename(file)))
                # Remove all empty folders in root folder
                for root, dirs, files in os.walk(self.directory):
                    for dir in dirs:
                        if not os.listdir(os.path.join(root, dir)):
                            os.rmdir(os.path.join(root, dir))
    
    def organize (self):
        """_summary_
        Organize the files.

        :return: None
        :rtype: None
        """
        self.get_files()
        self.sort_with_metadata()
        self.organize_files()


# Get the parameters from the command line
params = get_params()
    
# Create the object to organize the files
music_organizer = MusicOrganizer(params.directory, params.mode)
# Organize the files
music_organizer.organize()
