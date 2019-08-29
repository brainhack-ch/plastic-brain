from pycnbi.stream_player.stream_player import stream_player
import os

fif_file = r'./Recordings/brainHackTestOpen.fif'

if os.name == 'nt':  # nt -> Windows and posix -> Linux
    print("Running on windows system")
    fif_file = r'C:\Recordings\Gait\exp1 - Copy\fif\mb007_1.fif'

# sample code
if __name__ == '__main__':
    server_name = 'StreamPlayer'
    chunk_size = 8  # chunk streaming block size
    stream_player(server_name, fif_file, chunk_size)
