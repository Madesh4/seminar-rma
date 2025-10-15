

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
    
    pass
