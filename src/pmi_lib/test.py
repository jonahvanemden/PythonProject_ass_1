import numpy as np
from pmi_lib import read_dicom, read_nifti, write_nifti, dicom_to_nifti, masked_gaussian_filter, convert
from pmi_viewer import view

def test(image_path):
    """
    Test function for all functions.
    :param image_path: Path to the DICOM image file
    :return: None
    """

    # read_dicom test
    dicom_image, dicom_spacing = read_dicom(image_path)
    view(dicom_image, spacing=dicom_spacing, orientation='sag') # show

    # read_nifti test
    # image_nf, spacing_nf = read_nifti(image_path)
    # view(image_nf, spacing=spacing_nf, orientation="sag")

    # write_nifti test
    write_nifti(dicom_image, dicom_spacing, "write_nifti.nii.gz")

    # dicom_to_nifti test 
    convert(image_path, "nifti_convert.nii.gz") 

    # Masked gaussian filter
    bool_mask = np.ones(dicom_image.shape, dtype=bool)
    sigma = (5.0,) * dicom_image.ndim
    image_gaussian = masked_gaussian_filter(dicom_image, bool_mask, sigma)
    view(image_gaussian, spacing=dicom_spacing)


test("src/pmi_lib/images/ct_jaw")

#TODO API hide helper functions, good comments + docstrings, Readme.md file update 
