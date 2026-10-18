import pydicom
import nibabel as nib
import numpy as np
import os
import click
from .read_dicom import read_dicom
from .write_nifti import write_nifti

def convert(dicom_path, nifti_path) -> None:
    """
    Converts a DICOM file to Nifti format.
    
    :param dicom_path: path of the DICOM file(s)
    :param nifti_path: path to save the converted NIFTI file
    :returns: None
    """

    data, spacing = read_dicom(dicom_path)  # read dicom file(s)
    write_nifti(data, spacing, nifti_path)  # write nifti file
    return

@click.command()
@click.argument("dicom_path", type=click.Path(exists=True, file_okay=True), required=True)
@click.argument("nifti_path", type=click.Path(dir_okay=False), required=True)

def dicom_to_nifti(dicom_path, nifti_path) -> None:
    """Convert DICOM_PATH (a DICOM file or a directory of DICOM files) to the NIfTI file NIFTI_PATH."""
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

# dicom-to-nifti DICOM_PATH NIFTI_PATH  # This allows the script to be run directly from the command line