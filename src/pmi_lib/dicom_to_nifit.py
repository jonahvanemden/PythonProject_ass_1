import pydicom
import nibabel as nib
import numpy as np
import os
import click

def dicom_to_nifti (dicom_path, nifti_path):
    """
    Converts a DICOM file to Nifti format.

    :param dicom_path: path of the DICOM file(s)
    :param nifti_path: path to save the converted NIFTI file
    :returns: Nifti image object
    """
    # todo: incorporate click for command line interface

    if os.path.isfile(dicom_path):      # Single file

        dicom_image = pydicom.dcmread(dicom_path)       # Read file
        pixel_array = dicom_image.pixel_array           # Get pixel array from dicom image
        nifti_image = nib.Nifti1Image(pixel_array, affine=np.eye(4))    # Convert to nifti image using identity matrix as affine
        nib.save(nifti_image, nifti_path)               # Save nifti image to specified path
        print(f"Converted {dicom_path} to {nifti_path} successfully.")

        return nifti_image

    elif os.path.isdir(dicom_path):      # Multiple files in directory
        list_images = []
        for file_name in os.listdir(dicom_path):  # Iterate over all items in path_name
            full_name = os.path.join(dicom_path, file_name)  # Join the directory name and item name                    
            
            if os.path.isfile(full_name):  # Check if the item is a file. If it is, read it
                dicom_image = pydicom.dcmread(full_name)  # Read the image
                list_images.append(dicom_image)

        list_images = sorted(list_images, key=lambda img: img.ImagePositionPatient[2])   # sort the images based on the z-coordinate of the ImagePositionPatient attribute
        
        list_arrays = [image.pixel_array for image in list_images]
        pixel_array = np.stack(list_arrays, axis=-1)                # build a 3D array from the list of 2D arrays

        nifti_image = nib.Nifti1Image(pixel_array, affine=np.eye(4))   # Convert to nifti image using identity matrix as affine
        nib.save(nifti_image, nifti_path)       
        print(f"Converted {dicom_path} to {nifti_path} successfully.")

        return nifti_image

    else:       # When no file or directory is found, raise an error
        raise ValueError(f"Invalid path: {dicom_path}. Please provide a valid DICOM file or directory.")
    return

