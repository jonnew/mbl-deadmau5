import datetime
import json
import os

class Recorder:

    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.paused = True
        self.f = None
        self.write_number = 0
    
    def close_file(self):
        if self.f:
            self.f.seek(-1, os.SEEK_END)
            self.f.truncate()
            self.f.write(bytes('}}', 'utf8'))

    def write(self, datum):
        if not self.paused and self.f:
            dat = '\"' + str(self.write_number) + '\":'
            dat += json.dumps(datum)
            dat += ','
            self.f.write(bytes(dat, 'utf8'))
            self.write_number += 1
        
    # RPC Calls

    def run(self, cmd):
        return getattr(self, cmd)()

    def new(self):
        date = datetime.datetime.now()
        fid = date.strftime(self.folder + '%Y-%m-%d-%H-%M-%S') + \
            '_' + self.name + '.json'
        self.f = open(fid, 'wb')
        self.f.write(bytes('{', 'utf8'))
        return 'File opened'

    def start(self):
        self.paused = False
        return 'Recording started'

    def pause(self):
        self.paused = True
        return 'Recording Paused'

    def ping(self):
        return 'Recorder ready.'

