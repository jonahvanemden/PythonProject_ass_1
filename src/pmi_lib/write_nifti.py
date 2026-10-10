import nibabel as nib
import numpy as np

def write_nifti(data, spacing, file_path):
    """
    Saves a 3D array as a NIfTI-1 image.

    :param data: 3D image data to save
    :param spacing: Voxel spacing values
    :param file_path: Destination path for the NIfTI file
    """
    try:  # Try to convert the input data to an numpy array
        data = np.asarray(data)
    except (TypeError, ValueError) as error:  # If the input data can't be converted raise value error
        raise ValueError("data must be convertible to a NumPy array") from error

    try:  # Check if spacing is array of floats
        spacing = np.asarray(spacing, dtype=float)
    except (TypeError, ValueError) as error:    # Raise error if spacing data is incorrect 
        raise ValueError("spacing must be a sequence of floats") from error
    if spacing.shape != (3,):   # Check if spacing has 3 values
        raise ValueError("spacing must contain exactly 3 floats")
    if not isinstance(file_path, str):  # Filepath must be a string
        raise ValueError("file_path must be a string")

    affine = np.eye(4) # Initialize affine matrix
                

    affine[0, 0] = spacing[0]   # Adjust affine matrix with correct voxel spacing
    affine[1, 1] = spacing[1]
    affine[2, 2] = spacing[2]
    
    data = np.flip(data)
    data = np.transpose(data)

    if data.dtype == bool:  # Check if we are trying to use this function for a segmentation
        data = data.astype(np.uint8)    # Convert segmentation boolean values

    nf_image = nib.nifti1.Nifti1Image(data, affine)

    nib.nifti1.save(nf_image, file_path)

