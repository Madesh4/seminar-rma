import numpy as np
from scipy.signal import butter, filtfilt

def butterworth_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    filtered = data.copy()
    numeric_cols = data.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col == 'time':
            continue
        filtered[col] = filtfilt(b, a, data[col].values)

    return filtered  # <-- this was missing