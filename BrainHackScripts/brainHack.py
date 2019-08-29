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
from arduino_handler import ArduinoCommHandler
from leds_csv_index import leds_csv_sources

# EEG Channel names
EEG_CH_NAMES = [
    'TRIGGER', 'P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'Pz',
    'Fp1', 'Fp2', 'T3', 'T5', 'O1', 'O2', 'X3', 'X2', 'F7', 'F8', 'X1',
    'A2', 'T6', 'T4'
]

window_max_power = 0
window_min_power = 0
last_max_values = []
last_min_values = []
qnt_max_values = 0
qnt_min_values = 0


def normalize_array(input_array):
    max_value = input_array.max()
    min_value = input_array.min()
    range_value = max_value - min_value
    return (input_array - min_value) / range_value

def normalize_array_with_min_max(input_array, max_value, min_value):
    # max_value = input_array.max()
    # min_value = input_array.min()
    range_value = max_value - min_value
    return (input_array - min_value) / range_value

# Main function and loop to send live EEG filtered data to PlasticBrain
if __name__ == '__main__':
    # Setup the processing object
    brainhack = BrainHackEEGProcessing(sampling_frequency=300,
                                       eeg_ch_names=EEG_CH_NAMES.copy())

    # Setup the arduino using the first USB port
    arduino = ArduinoCommHandler(port_name='/dev/ttyACM0', baudrate=115200)
    arduino.start_communication()
    # We have 191 LEDs in the PlasticBrain
    leds_values = [0] * 191
    leds_values_index_for_test = 0

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
    # qc.print_c('Trigger channel: %d' % trg_ch, 'G')

     # Frequency band for the band-pass filter
    fmin = 1
    fmax = 47
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

        # if len(trigger) > 0:
            # qc.print_c('Triggers: %s' % np.array(trigger), 'G')

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

        window = brainhack.sources # shape 5004x300
        # Just keep the sources used for the LEDs
        window = window[leds_csv_sources, :] # Shape 191x300

        # Computing the power spectrum density using multitapers
        psd = psde.transform(
            window.reshape((1, window.shape[0], window.shape[1]))
        )
        # channels x frequencies
        psd = psd.reshape((psd.shape[1], psd.shape[2]))

        # Alpha band (8-12 Hz)
        alpha_average_power = psd[:, 8:12].mean(1)
        # Beta band (13-40 Hz)
        # beta_average_power = psd[:, 13:40].mean(1)

        print(alpha_average_power.mean())

        last_max_values.append(alpha_average_power.max())
        if len(last_max_values) > 1000: # Keep the last 1000 max values
            last_max_values.pop(0)

        last_min_values.append(alpha_average_power.min())
        if len(last_min_values) > 1000:# Keep the last 1000 min values
            last_min_values.pop(0)

        # Autoscale alpha values from the history of min and max values
        max = np.mean(last_max_values) + np.std(last_max_values)
        min = np.mean(last_min_values) - np.std(last_min_values)

        print("max: %.4f, min: %.4f -- mean_max: %.4f, mean_min: %.4f" % (
            alpha_average_power.max(), alpha_average_power.min(),
            max, min
        ))

        # alpha_normalized = normalize_array(alpha_average_power) * 255

        # alpha_normalized = normalize_array_with_min_max(
        #     alpha_average_power, max_value=max, min_value=min
        # ) * 255

        alpha_normalized = normalize_array_with_min_max(
            alpha_average_power, max_value=0.015, min_value=0.01
        ) * 255

        # Convert to bytes (0-255)
        alpha_normalized[alpha_normalized>255] = 255
        alpha_normalized[alpha_normalized<0] = 0
        alpha_normalized = alpha_normalized.astype(np.uint8)
        leds_values = list(alpha_normalized)
        # leds_values = [127] * 191
        # leds_values[leds_values_index_for_test] = 255
        # leds_values[leds_values_index_for_test-1] = 255
        # leds_values[leds_values_index_for_test-2] = 127
        # leds_values[leds_values_index_for_test-3] = 0
        # leds_values[leds_values_index_for_test-4] = 0
        # leds_values_index_for_test = leds_values_index_for_test + 1
        # if leds_values_index_for_test >= 191:
            # leds_values_index_for_test = 0
        # leds_values = list(np.random.randint(0, 255, 191))

        # Send byte values to the arduino which will compute the 3-byte RGB color
        arduino.send_led_values(leds_values)

        last_ts = tslist[-1] # Last timestamp
        tm.sleep_atleast(0.05)
