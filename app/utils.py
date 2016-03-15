''' Utility functions.'''

import config, sys

def read_rfid():
    ''' Read RFID tag from serial port.'''
    
    pass


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS
