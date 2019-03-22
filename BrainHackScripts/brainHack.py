import mne
import os
import pycnbi.utils.q_common as qc
import numpy as np
from pycnbi.utils import pycnbi_utils as pu
from pycnbi.stream_receiver.stream_receiver import StreamReceiver

if __name__ == '__main__':
    
    mne.set_log_level('ERROR')
    os.environ['OMP_NUM_THREADS'] = '1' # actually improves performance for multitaper

    amp_name, amp_serial = pu.search_lsl()
    sr = StreamReceiver(window_size=1, buffer_size=1, amp_name=amp_name, amp_serial=amp_serial, eeg_only=False)
    sfreq = sr.get_sample_rate()
    watchdog = qc.Timer()
    tm = qc.Timer(autoreset=True)
    trg_ch = sr.get_trigger_channel()
    last_ts = 0
    qc.print_c('Trigger channel: %d' % trg_ch, 'G')

    fmin = 1
    fmax = 40
    psde = mne.decoding.PSDEstimator(sfreq=sfreq, fmin=fmin, fmax=fmax, bandwidth=None, \
        adaptive=False, low_bias=True, n_jobs=1, normalization='length', verbose=None)

    while True:
        sr.acquire()
        window, tslist = sr.get_window() # window = [samples x channels]
        window = window.T # chanel x samples

        # print event values
        tsnew = np.where(np.array(tslist) > last_ts)[0][0]
        trigger = np.unique(window[trg_ch, tsnew:])

        if len(trigger) > 0:
            qc.print_c('Triggers: %s' % np.array(trigger), 'G')

        print('[%.1f] Receiving data...' % watchdog.sec())

        # ADD YOUR CODE

        # Computing the power spectrum density using multitapers
        psd = psde.transform(window.reshape((1, window.shape[0], window.shape[1])))
        psd = psd.reshape((psd.shape[1], psd.shape[2])) # channels x frequencies

        last_ts = tslist[-1]
        tm.sleep_atleast(0.05)
