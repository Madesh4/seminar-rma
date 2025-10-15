import torch 

def rotate_by_axis(point, axis, angle):
    """
    Rotate a set of point around a given axis by a specified angle.


    Parameters:
    point (ndarray): An 1x3 array of the point to be rotated.
    axis (ndarray): A 3-element array representing the axis of rotation.
    angle (float): The angle in radians to rotate the point.

    Returns:
    ndarray: The rotated point as an 1x3 array
    ndarray: The rotation matrix used for the rotation
    """
    # To keep it simple in this function, we only allow rotations around the standard basis axes
    assert list(axis) in [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "Axis must be one of the standard basis vectors."

    # TODO: Implement the rotation logic here
    # Caveat: Our testing will use numpy arrays, so you might need to type-check and convert to other data types if necessary.
    pass

    if not isinstance(point, torch.Tensor):
        point = torch.tensor(point, dtype=torch.float32)
    if not isinstance(axis, torch.Tensor):
        axis = torch.tensor(axis, dtype=torch.float32)
    if not isinstance(angle, torch.Tensor):
        angle = torch.tensor(angle, dtype=torch.float32)
    sin = torch.sin(angle)
    cos = torch.cos(angle)

    if list(axis) == [1, 0, 0]:  # Rotation around x-axis
        rotation_matrix = torch.tensor([
            [1, 0, 0],
            [0, cos, -sin],
            [0, sin, cos]
        ], dtype=torch.float32
        )
    elif list(axis) == [0, 1, 0]:  # Rotation around y-axis
        rotation_matrix = torch.tensor([
            [cos, 0, sin],
            [0, 1, 0],
            [-sin, 0, cos]], dtype=torch.float32
        )
    elif list(axis) == [0, 0, 1]:  # Rotation around z-axis
        rotation_matrix = torch.tensor([
            [cos, -sin, 0],
            [sin, cos, 0],
            [0, 0, 1]
        ], dtype=torch.float32)

    return torch.matmul(rotation_matrix, point.T).T, rotation_matrix

def rotate_multi_axis(point, order, angles):
    """
    Rotate a point around multiple axes in a specified order.
    Parameters:
    point (ndarray): An 1x3 array of points to be rotated.
    order (str): A string specifying the order of axes to rotate around, e.g., 'xyz', 'zyx', etc.
    angles (list or ndarray): A list or array of three angles in radians corresponding to the axes in the order string.
    Returns:
    ndarray: The rotated point as an 1x3 array
    ndarray: The combined rotation matrix used for the rotations
    """
    assert len(order) == 3 and all(axis in 'xyz' for axis in order), "Order must be a permutation of 'xyz'."
    assert len(angles) == 3, "Angles must be a 3-element list or array."

    # TODO: Implement the multi-axis rotation logic here
    # Caveat: Our testing will use numpy arrays, so you might need to type-check and convert to other data types if necessary.
    pass

    if not isinstance(point, torch.Tensor):
        point = torch.tensor(point, dtype=torch.float32)
    if not isinstance(angles, torch.Tensor):
        angles = torch.tensor(angles, dtype=torch.float32)

    # Initialize the rotated points as the original points
    rotated_points = point
    rotations = []

    for i, axis in enumerate(order):
        if axis == 'x':
            _, rotation = rotate_by_axis(rotated_points, torch.tensor([1, 0, 0], dtype=torch.float32), angles[i])
        elif axis == 'y':
            _, rotation = rotate_by_axis(rotated_points, torch.tensor([0, 1, 0], dtype=torch.float32), angles[i])
        elif axis == 'z':
            _, rotation = rotate_by_axis(rotated_points, torch.tensor([0, 0, 1], dtype=torch.float32), angles[i])
        rotations.append(rotation)
    
    matrix = rotations[2] @ (rotations[1] @ rotations[0])  # Combined rotation matrix
    rotated_points = torch.matmul(matrix, point.T).T
    return rotated_points, matrix
