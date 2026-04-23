import matplotlib.pyplot as plt
import numpy as np


def _extract_experimental_markers(marker_positions_exp):
    if isinstance(marker_positions_exp, dict):
        return {
            str(name): np.asarray(position, dtype=float)
            for name, position in marker_positions_exp.items()
        }

    if hasattr(marker_positions_exp, "columns"):
        if len(marker_positions_exp) == 0:
            return {}
        marker_positions_exp = marker_positions_exp.iloc[0]

    if hasattr(marker_positions_exp, "index") and hasattr(marker_positions_exp, "to_numpy"):
        index = [str(name) for name in marker_positions_exp.index]
        values = marker_positions_exp.to_numpy(dtype=float)
        marker_map = {}
        for start in range(len(index) - 2):
            current = index[start]
            if not current.endswith("_x"):
                continue
            base_name = current[:-2]
            expected = [f"{base_name}_x", f"{base_name}_y", f"{base_name}_z"]
            if index[start:start + 3] != expected:
                continue
            marker_map[base_name] = values[start:start + 3]
        return marker_map

    return {}


def _lookup_marker(marker_map, marker_name):
    candidates = [
        marker_name,
        f"marker_{marker_name}",
        marker_name.removeprefix("marker_"),
        f"marker_{marker_name.removeprefix('marker_')}",
    ]
    for candidate in candidates:
        if candidate in marker_map:
            return marker_map[candidate]
    return None

def visualize_markers(marker_positions_FK, marker_positions_exp):
    """Visualize the markers from FK and experimental data"""

    experimental_markers = _extract_experimental_markers(marker_positions_exp)

    fig = plt.figure()
    for i in range(3):
        ax = fig.add_subplot(131 + i)
        idx = [0, 1] if i == 0 else [2, 1] if i == 1 else [0, 2]
        for marker_name, marker_pos in marker_positions_FK.items():
            ax.plot(*marker_pos[[idx[0], idx[1]]], 'rx')
            ax.text(marker_pos[idx[0]], marker_pos[idx[1]], marker_name, color='red', fontsize=6)
        ax.axis('equal')
        plane = "Sagittal" if i == 0 else "Frontal" if i == 1 else "Transverse"
        ax.set_title(f"{plane} Plane")
        for marker_name, marker in experimental_markers.items():
            ax.plot(*marker[[idx[0], idx[1]]], 'gx')
            ax.text(marker[idx[0]], marker[idx[1]], marker_name, color='green', fontsize=6)
    plt.show()

def evaluate_marker_error(marker_positions_FK, marker_positions_exp):
    """Evaluate the RMSE error between FK and experimental marker positions"""
    experimental_markers = _extract_experimental_markers(marker_positions_exp)
    e = []
    for marker, marker_position in marker_positions_FK.items():
        experimental_marker = _lookup_marker(experimental_markers, marker)
        if experimental_marker is None:
            continue
        e.append(np.linalg.norm(np.asarray(experimental_marker, dtype=float) - np.asarray(marker_position, dtype=float)) ** 2)
    if not e:
        return np.nan
    rmse = np.sqrt(np.mean(e))
    return rmse