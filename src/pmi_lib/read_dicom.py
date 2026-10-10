import os
import nibabel as nib
import numpy as np
from pydicom import dcmread
from pydicom.pixels import apply_rescale
from pmi_viewer import view
from pathlib import Path

#assignment deel 2

def get_z_position(dicom_image):
    """
    Returns the z-coordinate of the Image Position Patient DICOM attribute.
    """
    return dicom_image.ImagePositionPatient[2]


def get_spacing(dicom_list):
    """" 
    calculate the pixel spacing. Slice spacing is calculated from the first slice to the last slice devided by the number of intervals.
    """
    dx, dy = map(float, dicom_list[0].PixelSpacing)

    if len(dicom_list) > 1:
        positions = np.array([
            d.ImagePositionPatient for d in dicom_list
        ], dtype=float)

        distances = np.linalg.norm(
            np.diff(positions, axis=0), axis=1
        )
        dz = float(np.mean(distances))
    else:
        dz = float(getattr(
            dicom_list[0],
            "SpacingBetweenSlices",
            getattr(dicom_list[0], "SliceThickness", 1.0)
        ))

    return (dx, dy, dz)




def read_dicom(file_path: str):
    """
    Reads a single DICOM file or a directory of DICOM files.

    Returns:
        data: NumPy array containing physical pixel values.
        spacing: Tuple of floats (dx, dy, dz).
    """
    if os.path.isfile(file_path):
        dicom_list = [dcmread(file_path)]

    elif os.path.isdir(file_path):
        dicom_list = []

        for file_name in os.listdir(file_path):
            full_name = os.path.join(file_path, file_name)

            if not os.path.isfile(full_name):
                continue

            try:
                dicom_image = dcmread(full_name)

                if hasattr(dicom_image, "PixelData"):
                    dicom_list.append(dicom_image)

            except Exception:
                continue

        if not dicom_list:
            raise ValueError("No DICOM files found in directory.")

    else:
        raise FileNotFoundError(f"Path does not exist: {file_path}")

    # Check Series Instance nstance UID
    series_uids = [
        getattr(dicom_image, "SeriesInstanceUID", None)
        for dicom_image in dicom_list
    ]

    if None in series_uids or len(set(series_uids)) != 1:
        raise ValueError(
            "All DICOM files must have the same Series Instance UID."
        )

    # Sort slices by z-position when position information is available
    if len(dicom_list) > 1:
        dicom_list.sort(key=get_z_position)

    # Convert stored pixel values to physical values
    images = []

    for dicom_image in dicom_list:
        image = apply_rescale(
            dicom_image.pixel_array,
            dicom_image
        )
        images.append(image)

    # A single file gives a 2D array; a directory gives a 3D array
    if len(images) == 1:
        data = np.asarray(images[0])
    else:
        data = np.stack(images, axis=0)

    spacing = get_spacing(dicom_list)

    return data, spacing

    
dicom_folder = Path(__file__).parent / "images" / "ct_jaw"

data, spacing = read_dicom(str(dicom_folder))

print("Shape:", data.shape)
print("Voxel spacing:", spacing)

view(data, spacing=spacing)