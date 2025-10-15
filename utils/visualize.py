
def visualize_markers(marker_positions_FK, marker_positions_exp):
    """Visualize the markers from FK and experimental data"""

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
        for i in range(len(marker_positions_exp.values[:-1].reshape(-1, 3))):
            marker_name = marker_positions_exp.index[2 + 3*i]
            marker = marker_positions_exp.values[:-1].reshape(-1, 3)[i]
            ax.plot(*marker[[idx[0], idx[1]]], 'gx')
            ax.text(marker[idx[0]], marker[idx[1]], marker_name, color='green', fontsize=6)
    plt.show()

def evaluate_marker_error(marker_positions_FK, marker_positions_exp):
    """Evaluate the RMSE error between FK and experimental marker positions"""
    e = []
    for marker in marker_positions_FK.keys():
        if marker + "_x" not in marker_positions_exp.index:
            continue
        col_idx_0 = marker_positions_exp.index.get_loc(marker + "_x")
        e.append(np.linalg.norm(
            marker_positions_exp.values[col_idx_0:col_idx_0+3] - np.array(marker_positions_FK[marker])
        )**2)
    rmse = np.sqrt(np.mean(e))
    return rmse