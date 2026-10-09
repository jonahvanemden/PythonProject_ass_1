import nibabel as nib
import numpy as np

def read_nifti(file_path):
    """
    Reads a Nifti file and returns a the data.
    """
    nifti_image = nib.load(file_path)  # Read the image.

    spacing = nifti_image.header.get_zooms()

    np_image = nifti_image.get_fdata()  # Store np array.

    image_tp = np.transpose(np_image)  # Transpose
    image_fl = np.flip(image_tp)  # Flip

    return image_fl, spacing

