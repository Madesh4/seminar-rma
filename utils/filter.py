import scipy
import numpy as np

def butterworth_lowpass_filter(data, cutoff, fs, order=2):
    """Apply a zero-lag Butterworth low-pass filter to the data.
    
    Parameters:
    - data: pandas DataFrame with the data to be filtered
    - cutoff: cutoff frequency in Hz
    - fs: sampling frequency in Hz
    - order: order of the Butterworth filter (default is 2)
    
    Returns:
    - filtered_data: pandas DataFrame with the filtered data
    """

    # Todo: Implement the Butterworth low-pass filter here
    # Use a forward-backward filter (filtfilt) to avoid phase shift
    # Hint: You can use scipy.signal.butter and scipy.signal.filtfilt
    
    # Iterate over each column and apply the filter
    # !Do not filter time or frame number columns!
    # We use order = 2 as a default, because filtfilt effectively doubles the order
    pass 

    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    
    # Apply the filter to each column
    filtered_data = data.copy()
    for col in data.columns:
        if col.lower() in ['time', 'frame#', 'frame']:
            continue  # Skip non-numeric columns
        if np.issubdtype(data[col].dtype, np.number):
            filtered_data[col] = scipy.signal.filtfilt(b, a, data[col])
    
    return filtered_data