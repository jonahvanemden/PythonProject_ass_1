import numpy as np
from pmi_lib import read_dicom, read_nifti, write_nifti, dicom_to_nifti, masked_gaussian_filter, convert
from pmi_viewer import view

def test(image_path):
    """
    Test function for all functions.
    :param image_path: Path to the DICOM image file
    :return: None
    """
    dicom_image, dicom_spacing = pmi.read_dicom(image_path) # read_dicom test
    view(dicom_image, spacing=dicom_spacing, orientation='sag') # show
    
    nifti_path = image_path.replace('.dcm', '.nii.gz') 
    convert(image_path, nifti_path) # dicom_to_nifty test

    # Read Dicom
    image, spacing = read_dicom(image_path)

    # Read NIFTI
    image, spacing = read_nifti(image_path)

    # Write NIFTI
    write_nifti(image, spacing, "write_nifti.nii.gz")

    # Dicom to NIFTI
    dicom_to_nifti(image_path, "converted_nifti.nii.gz")

    # Masked gaussian filter
    bool_mask = np.ones(image.shape, dtype=bool)
    sigma = (1.0,) * image.ndim
    image = masked_gaussian_filter(image, bool_mask, sigma)

    view(image, spacing = spacing, orientation='sag')

test("/Users/jonahvanemden/Desktop/PythonProject_ass_1/src/pmi_lib/images/ct_jaw_slice.dcm")
