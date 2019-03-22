from pycnbi.stream_player.stream_player import stream_player

# sample code
if __name__ == '__main__':
    server_name = 'StreamPlayer'
    chunk_size = 8 # chunk streaming block size
    fif_file = r'C:\Recordings\Gait\exp1 - Copy\fif\mb007_1.fif'
    stream_player(server_name, fif_file, chunk_size)
