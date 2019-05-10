#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PlasticBrain main script. Receives EEG data from LSL, filter it, get power spectrum and project onto sources the mean alpha power

Developed at the 2019 Brainhack Geneva event for the PlasticBrain project.
Participants : Manik Bhattacharjee,Victor Ferat, Italo Fernandes, Jelena, Gaetan, Elif, Jorge

Original project by Manik Bhattacharjee and Pierre Deman

"""

import os
import numpy as np
import mne
import pycnbi.utils.q_common as qc
from pycnbi.utils import pycnbi_utils as pu
from pycnbi.stream_receiver.stream_receiver import StreamReceiver
from eeg_processing import BrainHackEEGProcessing

EEG_CH_NAMES = [
    'TRIGGER', 'P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'Pz',
    'Fp1', 'Fp2', 'T3', 'T5', 'O1', 'O2', 'X3', 'X2', 'F7', 'F8', 'X1',
    'A2', 'T6', 'T4'
]

window_max_power = 0
window_min_power = 0
last_max_values = np.zeros(5000)
last_min_values = np.zeros(5000)
qnt_max_values = 0
qnt_min_values = 0


def normalize_array(input_array):
    max_value = input_array.max()
    min_value = input_array.min()
    range_value = max_value - min_value
    return (input_array - min_value) / range_value

# Main function and loop to send live EEG filtered data to PlasticBrain
if __name__ == '__main__':
    # Setup the processing object
    brainhack = BrainHackEEGProcessing(sampling_frequency=300,
                                       eeg_ch_names=EEG_CH_NAMES.copy())
    mne.set_log_level('ERROR')
    # actually improves performance for multitaper
    os.environ['OMP_NUM_THREADS'] = '1'

    # Find a LSL stream to receive raw EEG data
    amp_name, amp_serial = pu.search_lsl()
    sr = StreamReceiver(
        window_size=1, buffer_size=1, amp_name=amp_name,
        amp_serial=amp_serial, eeg_only=True
    )
    sfreq = sr.get_sample_rate()
    watchdog = qc.Timer()
    tm = qc.Timer(autoreset=True)
    trg_ch = sr.get_trigger_channel()
    last_ts = 0
    qc.print_c('Trigger channel: %d' % trg_ch, 'G')

     # Frequency band for the band-pass filter
    fmin = 1
    fmax = 40
    # Create an estimator of the power spectrum density in the frequency band
    psde = mne.decoding.PSDEstimator(
        sfreq=sfreq, fmin=fmin, fmax=fmax, bandwidth=None,
        adaptive=False, low_bias=True, n_jobs=1,
        normalization='length', verbose=None
    )
    # Main loop
    while True:
        sr.acquire() # Read data from LSL
        window, tslist = sr.get_window()  # window = [samples x channels]
        window = window.T  # channels x samples

        # print event values
        tsnew = np.where(np.array(tslist) > last_ts)[0][0]
        trigger = np.unique(window[trg_ch, tsnew:])

        if len(trigger) > 0:
            qc.print_c('Triggers: %s' % np.array(trigger), 'G')

        # print('[%.1f] Receiving data...' % watchdog.sec())

        # Pass data to the processing code
        # - bandpass it
        # - apply the inverse solution to get a signal for all cortical sources
        unused_channels = ['TRIGGER', 'X1', 'X2', 'X3', 'A2']
        brainhack.eeg_ch_names = EEG_CH_NAMES.copy()
        brainhack.window_signal = window
        brainhack.remove_unused_channels(unused_channels)
        brainhack.convert_to_mne_obj()
        brainhack.filter_signal(start_freq=fmin, stop_freq=fmax)
        brainhack.convert_mne_back_to_np_array()
        brainhack.multiply_inverse_solution()

        window = brainhack.big_array_with_a_lot_of_sources

        # Computing the power spectrum density using multitapers
        psd = psde.transform(
            window.reshape((1, window.shape[0], window.shape[1]))
        )
        # channels x frequencies
        psd = psd.reshape((psd.shape[1], psd.shape[2]))

        # Alpha band (6-13 Hz)
        alpha_average_power = psd[:, 6:13].mean(1)
        # Beta band (13-40 Hz)
        # beta_average_power = psd[:, 13:40].mean(1)

        alpha_normalized = normalize_array(alpha_average_power) * 255
        # Convert to bytes
        alpha_normalized = alpha_normalized.astype(np.uint8)

        last_ts = tslist[-1] # Last timestamp
        tm.sleep_atleast(0.05)

