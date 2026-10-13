import pmi_lib as pmi
from pmi_viewer import view

def test(image_path):
    image_fl, spacing = pmi.read_nifti(image_path)
    view(image_fl, spacing = spacing, orientation='sag')
    # pmi.write_nifti(data, spacing, file_path)

test("images/ct_jaw.nii.gz")

