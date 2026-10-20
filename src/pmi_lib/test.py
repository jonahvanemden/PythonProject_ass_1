import numpy as np
from pmi_lib import read_dicom, read_nifti, write_nifti, dicom_to_nifti, masked_gaussian_filter, convert
from pmi_viewer import view
from pathlib import Path
from click.testing import CliRunner

def test(image_path):
    """
    Test function for all functions.
    :param image_path: Path to the DICOM image file
    :returns: DICOM image and Gaussian filtered image
    """

    # read_dicom test
    dicom_image = read_dicom(image_path)
    print("DICOM image:", dicom_image)
    print("Read DICOM test completed.")

    # write nifti test: save file in pmi_lib/images
    output_path = Path(__file__).parent / "images" / "write_nifti_test.nii.gz"
    write_nifti(dicom_image, str(output_path))
    print("Write NIfTI test completed.")

    # dicom_to_nifti test 
    output_path = Path(__file__).parent / "images" / "dicom_to_nifti_test.nii.gz"
    convert(image_path, str(output_path))
    print("DICOM to NIfTI conversion test completed.")

    # Masked gaussian filter
    bool_mask = np.ones(dicom_image._data.shape, dtype=bool)
    sigma = (5.0,) * dicom_image._data.ndim
    image_gaussian = masked_gaussian_filter(dicom_image, bool_mask, sigma)

    print("Masked Gaussian filter test completed.")
    
    return dicom_image, image_gaussian


def view_test_images (image_path):
    """
    View the DICOM image and the Gaussian filtered image.
    :param image_path: Path to the DICOM image file
    :returns: None
    """

    dicom_image, image_gaussian = test(image_path)
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
    print("CLI test passed.")
    return


test("src/pmi_lib/images/ct_jaw")
test_cli("src/pmi_lib/images/ct_jaw")
view_test_images("src/pmi_lib/images/ct_jaw")
