import nibabel as nib
import numpy as np

def write_nifti(data, spacing, file_path):
    affine = np.eye(4)

    affine[0, 0] = spacing[0]
    affine[1, 1] = spacing[1]
    affine[2, 2] = spacing[2]

    data = np.flip(data)
    data = np.transpose(data)

    if data.dtype == bool:
        data = data.astype(np.uint8)

    nf_image = nib.nifti1.Nifti1Image(data, affine)

    nib.nifti1.save(nf_image, file_path)

    #TODO add raise value error
