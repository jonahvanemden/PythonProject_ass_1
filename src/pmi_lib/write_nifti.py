import nibabel as nib
import numpy as np
from pmi_lib.image_class import Image


def write_nifti(image : Image, file_path : str) -> nib.Nifti1Image:
    """
    Save a 2D or 3D array as a NIfTI-1 image.

    :param image: image data to save
    :param file_path: Destination path for the NIfTI file
    
    :returns: NifTI image object
    :raises TypeError: if image is not an Image or file_path is not a string
    :raises ValueError: if the image is not 2D or 3D
    """

    if not isinstance(image, Image):
        raise TypeError(f"image must be an Image, got {type(image).__name__}")
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
 
    data = np.asarray(image)  # the pixel data as a NumPy array
    if data.ndim not in (2, 3):
        raise ValueError(f"Only 2D and 3D images can be written, got {data.ndim} dimensions.")
 
    affine = np.eye(4)  # start with the identity matrix
    for axis, spacing in enumerate(image.spacing):
        affine[axis, axis] = spacing  # put the voxel spacing on the diagonal
 
    data = np.transpose(np.flip(data))  # convert to the NIfTI axis layout
 
    if data.dtype == bool:  # a segmentation: NIfTI cannot store booleans
        data = data.astype(np.uint8)
 
    nf_image = nib.Nifti1Image(data, affine)
    nib.save(nf_image, file_path)
    print(f"Saved NIfTI image to {file_path} successfully.")
    return nf_image
