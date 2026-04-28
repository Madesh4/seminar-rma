import numpy as np
import pandas as pd


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

    force = grf_y_column.values

    # --- 1. Find heel strikes (force crosses threshold upward) ---
    above = force > threshold
    # A heel strike is where above goes from False to True
    heel_strikes = np.where(~above[:-1] & above[1:])[0] + 1

    # --- 2. Slice data between consecutive heel strikes ---
    segments = []
    for i in range(len(heel_strikes) - 1):
        start = heel_strikes[i]
        end   = heel_strikes[i + 1]
        cycle = data.iloc[start:end].copy()
        # Reset time so each cycle starts at 0
        cycle['time'] = cycle['time'] - cycle['time'].iloc[0]
        segments.append(cycle)

    # --- 3. Remove cycles that never reach 300 N (partial steps / noise) ---
    segments = [c for c in segments if c[grf_y_column.name].max() >= 300]

    # --- 4. Remove cycles whose duration is > ±2 SD from the mean ---
    durations = np.array([c['time'].iloc[-1] - c['time'].iloc[0] for c in segments])
    mean_dur  = durations.mean()
    std_dur   = durations.std()
    segments  = [
        c for c, d in zip(segments, durations)
        if abs(d - mean_dur) <= 2 * std_dur
    ]

    return segments


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

    # Normalise each cycle to 0–100% (101 points) so they can be averaged
    normalised = []
    for cycle in cycles:
        index = np.linspace(0, 100, 101)
        resampled = pd.DataFrame(index=index)
        x = np.linspace(0, 100, len(cycle))
        for col in cycle.columns:
            resampled[col] = np.interp(index, x, cycle[col].values)
        normalised.append(resampled)

    stacked    = np.stack([df.values for df in normalised], axis=0)
    mean_cycle = pd.DataFrame(np.mean(stacked, axis=0), columns=cycles[0].columns)
    std_cycle  = pd.DataFrame(np.std(stacked,  axis=0), columns=cycles[0].columns)

    return mean_cycle, std_cycle