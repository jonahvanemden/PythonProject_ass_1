import read_dicom, read_nifti, write_nifti, dicom_to_nifit, masked_gaussian_filter
from read_nifti import read_nifti
from pmi_viewer import view

def test(image_path):
    image_fl, spacing = read_nifti(image_path)
    view(image_fl)
    # write_nifti(image_fl, spacing)

test("images/ct_jaw_slice.nii.gz")

