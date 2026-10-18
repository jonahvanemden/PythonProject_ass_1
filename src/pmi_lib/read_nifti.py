import nibabel as nib
import numpy as np
from pmi_lib.image_class import Image

def read_nifti(file_path :str) -> Image:
    """
    Reads a Nifti file and returns a the data.

    :param file_path: path of the NIFTI file 
    :returns: correct display of the NIFTI image and its relevant voxel spacing
    """
    nifti_image = nib.load(file_path)  # Read the image

    spacing = nifti_image.header.get_zooms() # Get pixel spacing stored in NIFTI header

    np_image = nifti_image.get_fdata()  # Store np array

    image_tp = np.transpose(np_image)  # Transpose for the expected display layout

    if image_tp.ndim == 2:
        image_fl = np.flip(image_tp)
    else:
        image_fl = np.flip(image_tp, axis=(1, 2))

    return Image(image_fl, spacing)
