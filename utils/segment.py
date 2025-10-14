import numpy as np
import pandas as pd
import scipy

def segment_gait_cycles(grf_y_column, data, threshold=60):
    """Segment gait cycles based on vertical ground reaction force (GRF) data.
    
    Parameters:
    - grf_y_column: pandas Series with vertical GRF data
    - threshold: force threshold to detect foot contact (default is 60 N)
    - data: optional pandas DataFrames with additional data to segment (e.g. kinematics)
    
    Returns:
    - segments: lists of DataFrames with segmented data if additional_data is provided
    """
    # Make sure to make the time starts at 0 in each returned segment
    


    pass
    
    # Identify indices where GRF exceeds the threshold
    above_threshold = grf_y_column > threshold
    indices = np.where(above_threshold)[0]
    
    if len(indices) == 0:
        return [], []
    
    # Find heel strikes (start of each contact phase)
    heel_strikes = []
    heel_strikes.append(indices[0])
    
    for i in range(1, len(indices)):
        if indices[i] > indices[i-1] + 1:
            # This is the start of a new contact phase (heel strike)
            heel_strikes.append(indices[i])
    
    # Create segments from one heel strike to the next heel strike
    segments = []
    for i in range(len(heel_strikes) - 1):
        if grf_y_column[heel_strikes[i]:heel_strikes[i+1]].max() < 300:
            continue  # Skip segments that do not reach 300 N
        segments.append((heel_strikes[i], heel_strikes[i+1]-1))

    # Remove segments that are +- 2 standard deviations away from the mean duration
    durations = [end - start for start, end in segments]
    mean_duration = np.mean(durations)
    std_duration = np.std(durations)
    filtered_segments = []
    for start, end in segments:
        duration = end - start
        if (mean_duration - 1 * std_duration) <= duration <= (mean_duration + 1 * std_duration):
            filtered_segments.append((start, end))
    segments = filtered_segments
    
    # If additional data is provided, segment it as well
    segmented_data = []
    if data is not None:
        for start, end in segments:
            segmented_data.append(data.iloc[start:end+1].reset_index(drop=True))
            segmented_data[-1].index = segmented_data[-1].index - segmented_data[-1].index[0]  # reset index to start at 0
            segmented_data[-1]['time'] = segmented_data[-1]['time'] - segmented_data[-1]['time'].iloc[0]  # reset time to start at 0

    return segmented_data


def ensemble_average(cycles):
    """Compute the ensemble average and standard deviation of segmented gait cycles.
    
    Parameters:
    - cycles: list of pandas DataFrames, each containing one gait cycle
    
    Returns:
    - mean_cycle: pandas DataFrame with the mean values across all cycles
    - std_cycle: pandas DataFrame with the standard deviation across all cycles
    """
    if len(cycles) == 0:
        return None, None
    
    # Resample each cycle to 100 data points using linear interpolation
    resampled_cycles = []
    for cycle in cycles:
        resampled_time = np.linspace(0, 1, 100)
        resampled_cycle = pd.DataFrame()
        for col in cycle.columns:
            if True:
                interp_values = np.interp(resampled_time, 
                                          (cycle['time'] - cycle['time'].min()) / (cycle['time'].max() - cycle['time'].min()), 
                                          cycle[col])
                resampled_cycle[col] = interp_values
        resampled_cycles.append(resampled_cycle)
    
    # Concatenate all resampled cycles into a single DataFrame
    all_cycles_df = pd.concat(resampled_cycles, ignore_index=True)
    
    # Compute mean and standard deviation for each column
    mean_cycle = all_cycles_df.groupby(all_cycles_df.index % 100).mean().reset_index(drop=True)
    std_cycle = all_cycles_df.groupby(all_cycles_df.index % 100).std().reset_index(drop=True)
    
    return mean_cycle, std_cycle
