#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlasticBrain Sender of recorded EEG data. Allows to send prerecorded EEG data through LSL to replay it on the PlasticBrain

Developed at the 2019 Brainhack Geneva event for the PlasticBrain project, runs on windows with a prerecorded file.
Participants : Manik Bhattacharjee,Victor Ferat, Italo Fernandes, Jelena, Gaetan, Elif, Jorge

Original project by Manik Bhattacharjee and Pierre Deman

"""

from pycnbi.stream_player.stream_player import stream_player
import os

fif_file = r'./Recordings/brainHackTestOpen.fif'

if os.name == 'nt':  # nt -> Windows and posix -> Linux
    print("Running on windows system")
    fif_file = r'C:\Recordings\Gait\exp1 - Copy\fif\mb007_1.fif'

if __name__ == '__main__':
    server_name = 'StreamPlayer'
    chunk_size = 8  # chunk streaming block size
    stream_player(server_name, fif_file, chunk_size)
