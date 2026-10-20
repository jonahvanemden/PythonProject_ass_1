import numpy as np
from pmi_lib import read_dicom, read_nifti, write_nifti, dicom_to_nifti, masked_gaussian_filter
from pmi_viewer import view
from pathlib import Path
from click.testing import CliRunner
from pmi_lib.dicom_to_nifti import convert, dicom_to_nifti
from pmi_lib.image_class import Image

dicom_path = "src/pmi_lib/images/ct_jaw"

def print_success(test_name):
    print(f"  [PASS] {test_name}")

def test(image_path):
    """
    Test function for all functions.
    :param image_path: Path to the DICOM image file
    :returns: DICOM image and Gaussian filtered image
    """

    # read_dicom test
    dicom_image = read_dicom(image_path)
    print("DICOM image:", dicom_image)
    print_success("Read DICOM")

    #read_nifti test
    nifti_image = read_nifti("src/pmi_lib/images/segment_1.nii.gz")
    print("NIfTI image:", nifti_image)
    print_success("Read NIfTI")

    # write nifti test: save file in pmi_lib/images
    output_path = Path(__file__).parent / "images" / "write_nifti_test.nii.gz"
    write_nifti(dicom_image, str(output_path))
    print_success("Write NIfTI")

    # dicom_to_nifti test 
    output_path = Path(__file__).parent / "images" / "dicom_to_nifti_test.nii.gz"
    convert(image_path, str(output_path))
    print_success("DICOM to NIfTI conversion")

    # Masked gaussian filter
    bool_mask = np.ones(dicom_image._data.shape, dtype=bool)
    sigma = (5.0,) * dicom_image._data.ndim
    image_gaussian = masked_gaussian_filter(dicom_image, bool_mask, sigma)

    print_success("Masked Gaussian Filter")
    
    return dicom_image, image_gaussian


def view_test_images (dicom_image, image_gaussian):
    """
    View the DICOM image and the Gaussian filtered image.
    :param dicom_image: The original DICOM image
    :param image_gaussian: The Gaussian filtered image
    :returns: None
    """
    view(dicom_image, spacing=dicom_image.spacing, orientation="sag")
    view(image_gaussian, spacing=dicom_image.spacing, orientation="sag")

    return


def test_cli(image_path):
    """Test the DICOM-to-NIfTI command-line interface.
    :param image_path: Path to the DICOM image file
    :returns: None
    """

    output_path = (Path(__file__).parent / "images" / "dicom_to_nifti_cli_test.nii.gz")

    runner = CliRunner()
    result = runner.invoke(dicom_to_nifti, [image_path, str(output_path)])

    # Check that the command completed successfully
    assert result.exit_code == 0, result.output or repr(result.exception)

    # Check that the output file was created
    assert output_path.exists(), "NIfTI output file was not created."

    # Check the success message
    assert "Converted" in result.output
    print_success("DICOM to NIfTI CLI conversion")
    return


def test_image_class() -> None:
       """Test the Image and DicomImage classes."""
       data = np.zeros((10, 20, 30))
       image = Image(data, spacing=(1, 0.5, 2))
       print(image)
       print("Default spacing:", Image(data, spacing=(1.0, 1.0, 1.0)).spacing)
       print("Voxel volume:", image.get_voxel_volume())
       print("Pixel area:", Image(np.zeros((4, 5)), (0.5, 2)).get_pixel_area())
       assert len(image) == 10 and np.shape(image) == (10, 20, 30) and np.ndim(image) == 3
       assert image[0].shape == (20, 30) and np.asarray(image, dtype=np.float32).dtype == np.float32

       for error, args in [(ValueError, (data, (1.0, 1.0))), (TypeError, ([1, 2],)), (TypeError, (data, 1.0))]:
           try:
               Image(*args)
           except error:
               pass
           else:
               raise AssertionError(f"Image{args} should raise {error.__name__}")
       print_success("Image class")


dicom_image, image_gaussian = test(dicom_path)
test_cli(dicom_path)
view_test_images(dicom_image, image_gaussian)
test_image_class()
