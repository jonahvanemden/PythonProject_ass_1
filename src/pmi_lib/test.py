import pmi_lib as pmi
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
    pmi.convert(image_path, nifti_path) # dicom_to_nifty test
    
    image_fl, spacing = pmi.read_nifti(image_path)
    view(image_fl, spacing = spacing, orientation='sag')
    # pmi.write_nifti(data, spacing, file_path)

test("images/ct_jaw.nii.gz")

