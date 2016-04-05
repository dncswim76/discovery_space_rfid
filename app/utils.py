''' Utility functions.'''

import config, sys

def read_rfid():
    ''' Read RFID tag from serial port.'''
    
    pass


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


def media_type(extension):
    ''' Return type of media based on file extension.'''

    if extension in ['png', 'jpg', 'JPG', 'jpeg', 'gif']:
        media = "image"
    elif extension in ['mp3']:
        media = "audio"
    elif extension in ['mp4']:
        media = "video"

    return media
