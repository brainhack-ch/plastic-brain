import mne
import numpy as np
import scipy.fftpack as fftpack
from scipy.signal import butter, lfilter, freqz, filtfilt


class BrainHackEEGProcessing:
    def __init__(self, sampling_frequency, eeg_ch_names):
        self.sampling_frequency = sampling_frequency
        self.eeg_ch_names = eeg_ch_names
        self.window_signal = None
        self.raw = None
        self.big_array_with_a_lot_of_sources = None

    def remove_unused_channels(self, unused_channels):
        new_index_list = list(range(len(self.eeg_ch_names)))
        for channel in unused_channels:
            new_index_list.remove(self.eeg_ch_names.index(channel))
        # Obs: Its required to do another 'for', otherwise: indexing errors
        for channel in unused_channels:
            self.eeg_ch_names.remove(channel)
        self.window_signal = self.window_signal[new_index_list, :]
        return (self.window_signal, self.eeg_ch_names)

    def convert_to_mne_obj(self):
        # Initialize an info structure
        info = mne.create_info(
            ch_names=self.eeg_ch_names,
            ch_types=['eeg'] * len(self.eeg_ch_names),
            sfreq=self.sampling_frequency
        )
        self.raw = mne.io.RawArray(self.window_signal, info)
        self.raw.set_eeg_reference(ref_channels='average')
        return self.raw

    def filter_signal(self, start_freq, stop_freq):
        self.raw = self.raw.filter(start_freq, stop_freq)
        return self.raw

    def convert_mne_back_to_np_array(self):
        self.window_signal = self.raw.get_data()
        return self.window_signal

    def multiply_inverse_solution(self):
        # qnt_sources = 5004
        # self.window_signal # 19 ch x 300 p
        # self.big_array_with_a_lot_of_sources # 5004 ch x 300 p
        self.big_array_with_a_lot_of_sources = self.window_signal
        self.big_array_with_a_lot_of_sources = np.zeros((5004, 300))
