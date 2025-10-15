import pandas as pd
# suppress pandas warnings for cleaner output
import warnings
import numpy as np

def load_marker_data(file_path="data/Trial1_marker.trc"):
    """Load marker data from a .trc file"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pd.errors.DtypeWarning)
        marker_data = pd.read_csv(file_path, sep='\t', skiprows=3)
    
    # Clean up header: 
    # The header has marker names in first row and X1, Y1, Z1, etc. in second row
    # We want to create column names like C7_x, C7_y, C7_z, T10_x, T10_y, T10_z, etc.
    header = marker_data.columns.tolist()
    new_columns = []
    marker_name = None
    coord_count = 1
    coords = ['x', 'y', 'z']
    
    for col in header:
        # Check if this is a marker name (not empty and not starting with X/Y/Z pattern)
        if col.startswith(('time', 'Frame#', 'Frame', 'Time')):
            new_columns.append(col)
            marker_name = None
            coord_count = 1
        elif col and not col.startswith(('X', 'Y', 'Z')) and 'Unnamed' not in str(col):
            marker_name = col
            coord_count = 1
            new_columns.append(col+'_x')
        else:
            # This is a coordinate column (X, Y, or Z)
            if marker_name and coord_count < 3:
                new_columns.append(f"{marker_name}_{coords[coord_count]}")
                coord_count += 1
            else:
                new_columns.append(col)
    
    marker_data.columns = new_columns
    marker_data = marker_data.iloc[1:]
    # Convert the strings to numeric, coerce errors to NaN
    marker_data = marker_data.apply(pd.to_numeric, errors='coerce')
    return marker_data

def load_grf_data(file_path="data/Trial1_GRF.mot"):
    """Load ground reaction force data from a .mot file"""
    grf_data = pd.read_csv(file_path, sep='\t', skiprows=5)
    return grf_data

def load_kinematics_data(file_path="data/Trial1_kinematics.mot"):
    """Load kinematics data from a .mot file"""
    kinematics_data = pd.read_csv(file_path, sep='\t', skiprows=10)
    return kinematics_data