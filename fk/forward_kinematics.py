from . import rotation
import numpy as np

def forward_kinematics(q, key, kintree):
    """Compute the forward kinematics for the given joint angles and kinematic tree.

    Args:
        q (ndarray): Generalized coordinates (joint angles) of shape (N,).
        key (list): List of joint names corresponding to the angles in 'q'.
        kintree (dict): Kinematic tree as in `model/kintree.py`.

    Returns:
        joints (dict): 3D positions of each joint after applying the forward kinematics, (J: 3).
        markers (dict): 3D positions of each marker after applying the forward kinematics, (M: 3).
    """

    ## ToDo: Your implementation here, hint: use recursion to traverse the kinematic tree
    # Check when an axis is written with [-1, 0, 0] instead of [1, 0, 0] - then you need to invert the angle
    pass

    a = 0
    positions_joints, positions_markers, orientations_joints = {}, {}, {}

    def get_positions(body_name, curr_body):
        # Now curr_body is the dictionary with 'parent', 'joints', 'offset', etc.
        # Don't overwrite it - just use it directly
        parent = curr_body.get('parent', None)
        if parent is None:
            curr_position = np.array(curr_body.get('offset', [0, 0, 0]), dtype=np.float32)
            # joints is a dict, so iterate over its items (key-value pairs)
            order = []
            angle = []
            translation = np.zeros(3, dtype=np.float32)
            for joint_name, joint_data in curr_body.get('joints', {}).items():
                if joint_data.get('type') == 'slider':
                    translation += np.array(joint_data.get('axis'), dtype=np.float32) * q[key.index(joint_name)]
                if joint_data.get('type') == 'hinge':
                    axis = joint_data.get('axis')
                    if axis[0] < 0 or axis[1] < 0 or axis[2] < 0:
                        # Invert the angle if any component of the axis is negative
                        angle.append(-q[key.index(joint_name)])
                        axis = [-a for a in axis]  # Make axis positive for order determination
                    else:
                        angle.append(q[key.index(joint_name)])
                    order.append('x' if np.allclose(axis, [1, 0, 0]) else 'y' if np.allclose(axis, [0, 1, 0]) else 'z')
            # For root: rotate the offset first
            curr_position, curr_orientation = rotation.rotate_multi_axis(
                point=curr_position,
                order=''.join(order),
                angles=angle
            )
            # Then add translation in the world frame (after rotation)
            curr_position = curr_position + translation
            orientations_joints[body_name] = curr_orientation
            positions_joints[body_name] = curr_position
        else:
            parent_position = positions_joints[parent]
            parent_orientation = orientations_joints[parent]
            curr_position = np.array(curr_body.get('offset', [0, 0, 0]), dtype=np.float32)
            order = []
            angle = []
            for joint_name, joint_data in curr_body.get('joints', {}).items():
                if joint_data.get('type') == 'hinge':
                    axis = joint_data.get('axis')
                    if axis[0] < 0 or axis[1] < 0 or axis[2] < 0:
                        # Invert the angle if any component of the axis is negative
                        angle.append(-q[key.index(joint_name)])
                        axis = [-a for a in axis]  # Make axis positive for order determination
                    else:
                        angle.append(q[key.index(joint_name)])
                    order.append('x' if np.allclose(axis, [1, 0, 0]) else 'y' if np.allclose(axis, [0, 1, 0]) else 'z')

            while len(order) < 3:
                order.append('x' if 'x' not in order else 'y' if 'y' not in order else 'z')
                angle.append(0.0)

            # For child bodies: rotate offset first
            _, curr_orientation = rotation.rotate_multi_axis(
                point=curr_position,
                order=''.join(order),
                angles=angle
            )
            # Then add translation in the local frame (after rotation)
            # Then transform to parent frame
            curr_orientation = parent_orientation @ curr_orientation
            curr_position = parent_position + parent_orientation @ curr_position
            orientations_joints[body_name] = curr_orientation
            positions_joints[body_name] = curr_position
        # Now handle markers
        for marker_name, marker_offset in curr_body.get('markers', {}).items():
            marker_position = curr_orientation @ np.array(marker_offset, dtype=np.float32) + curr_position
            positions_markers[marker_name] = marker_position

        # Recursively process children
        for child_name, child_body in curr_body.get('children', {}).items():   
            get_positions(child_name, child_body)

    # kintree is a dict where keys are body names and values are body data
    for body_name, body_data in kintree.items():
        get_positions(body_name, body_data)


    return positions_joints, positions_markers

def get_connections(kintree, joints):
    """Get connections between joints for visualization.

    Args:
        kintree (dict): Kinematic tree as in `model/kintree.py`.
        joints (dict): 3D positions of each joint after applying the forward kinematics, (J: 3).

    Returns:
        connections (list): List of tuples representing connection lines between joints.
        e.g [([x1, y1, z1], [x2, y2, z2]), ([x3, y3, z3], [x4, y4, z4]), ...] for lines between joint1 and joint2, joint3 and joint4.
    """
    pass
    connections = []
    def add_connections(body_name, curr_body):
        parent = curr_body.get('parent', None)
        if parent is not None and body_name in joints and parent in joints:
            connections.append((joints[parent], joints[body_name]))
        for child_name, child_body in curr_body.get('children', {}).items():
            add_connections(child_name, child_body)
    for body_name, body_data in kintree.items():
        add_connections(body_name, body_data)
    return connections

if __name__ == "__main__":
    import sys
    sys.path.append("..")  # To import from parent directory
    import numpy as np
    import torch
    from model.kintree import kintree

    from fk.forward_kinematics import forward_kinematics
    from utils.load_data import * 

    q_all = load_kinematics_data()
    marker_data = load_marker_data()
    curr_frame = 1240
    q = q_all.iloc[curr_frame].values[1:] # Exclude time column, 
    #q = q*0
    #q[10] = 1
    markers_ = marker_data.iloc[curr_frame].values[2:] # Exclude time and frame column
    key = list(q_all.columns[1:]) # Exclude time column

    joints, markers = forward_kinematics(q, key, kintree)
    
    import matplotlib.pyplot as plt

    for a, b in zip(q, key):
        print(f"{b}: {a}")
   
    # Print the rmse error between the computed markers and the given markers
    e = []
    for marker in markers.keys():
        if marker + "_x" not in marker_data.columns:
            continue
        col_idx_0 = marker_data.columns.get_loc(marker + "_x") - 2
        e.append(np.linalg.norm(
            markers_[col_idx_0:col_idx_0+3] - markers[marker].numpy()
        )**2)
    print(f"Total error: {np.sqrt(np.mean(e)):.4f}")


    # Just view the body from each side
    fig = plt.figure()
    for i in range(3):
        ax = fig.add_subplot(131 + i)
        idx = [0, 1] if i == 0 else [2, 1] if i == 1 else [0, 2]
        for joint_name, joint_pos in joints.items():
            if joint_name.startswith('pelvis') or joint_name.startswith('femur') or joint_name.startswith('tibia') or joint_name.startswith('talus'):
                ax.plot(*joint_pos[[idx[0], idx[1]]], 'bo')
                ax.text(joint_pos[idx[0]], joint_pos[idx[1]], joint_name, color='blue', fontsize=8)
        for marker_name, marker_pos in markers.items():
            ax.plot(*marker_pos[[idx[0], idx[1]]], 'rx')
            ax.text(marker_pos[idx[0]], marker_pos[idx[1]], marker_name, color='red', fontsize=4)
        ax.axis('equal')
        ax.set_title(f"Frame {curr_frame}")
        for i in range(len(markers_[:-1].reshape(-1, 3))):
            marker_name = marker_data.columns[2 + 3*i]
            marker = markers_[:-1].reshape(-1, 3)[i]
            ax.plot(*marker[[idx[0], idx[1]]], 'gx')
            ax.text(marker[idx[0]], marker[idx[1]], marker_name, color='green', fontsize=4)
    plt.show()
