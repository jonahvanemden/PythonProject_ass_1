import pydicom
import click
from .read_dicom import read_dicom
from .write_nifti import write_nifti
import nibabel as nib

def convert(dicom_path : str, nifti_path : str) -> nib.Nifti1Image:
    """
    Converts a DICOM file to Nifti format.
    
    :param dicom_path: path of the DICOM file(s)
    :param nifti_path: path to save the converted NIFTI file
    :returns: NifTI image object
    """

    dicom_image = read_dicom(dicom_path)  # read dicom file(s)
    nf_image = write_nifti(dicom_image, nifti_path)  # write nifti file
    return nf_image

@click.command()
@click.argument("dicom_path", type=click.Path(exists=True, file_okay=True), required=True)
@click.argument("nifti_path", type=click.Path(dir_okay=False), required=True)

def dicom_to_nifti(dicom_path : str, nifti_path : str) -> None:
    """Convert a DICOM file or directory to a NIfTI file.

    The input can be a single DICOM file or a directory
    containing a DICOM series. The output is saved to NIFTI_PATH.
    """

    try:
        convert(dicom_path, nifti_path)
    except pydicom.errors.InvalidDicomError:
        raise click.ClickException(f"'{dicom_path}' is not a valid DICOM file.")
    except FileNotFoundError as error:
        raise click.ClickException(f"File not found: {error}")
    except PermissionError:
        raise click.ClickException("Permission denied while reading or writing a file.")
    except ValueError as error:
        raise click.ClickException(str(error))
    except Exception:
        raise click.ClickException("An unexpected error occurred during conversion.")
    click.echo(f"Converted {dicom_path} to {nifti_path} successfully.")
    return

if __name__ == "__main__":
    dicom_to_nifti()