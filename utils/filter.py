

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
    
    # Design the Butterworth filter

    pass 
