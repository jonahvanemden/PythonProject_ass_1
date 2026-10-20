# PMI lib

## Assignment description 
This is the project template for the library that you will build during the group assignments.


### Project Template Layout

This project template contains a directory `src/pmi_lib/`. This directory is the actual Python package, in which you'll be adding new modules.

The file `pyproject.toml` is the project configuration. It contains e.g. information about the package, about the dependencies, and about the authors. You'll need to make some changes in here.

`README.md` is this file. Replace all this information and describe your library. A Markdown file (`.md`) is a text file with a simple [markup syntax](https://www.markdownguide.org/basic-syntax/).

The files `setup.py` and `MANIFEST.in` should **not** be changed. The file `setup.py` is a script for building code that we'll add in the second group assignment.

Finally, `LICENSE.md` contains the license. It contains the terms of use for this template.

```
project/
├── src/
│   └── pmi_lib/
│       ├── __init__.py
│       └── ...
├── pyproject.toml
├── README.md
├── setup.py
├── MANIFEST.in
└── LICENSE.md
```


### License

`pmi-lib` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Assignment 2a&2b implementation

pmi_lib is a small Python library for reading, converting and filtering medical images (DICOM and NIfTI). Images are represented by an Image class that keeps the pixel data together with the pixel spacing in millimetres, so that physical quantities (areas, volumes, filter widths) can be handled in mm instead of pixels.


### Image Class

The `Image` class represents image data along with its pixel spacing.

| Member | Description |
|---|---|
| `image.spacing` | Tuple of floats representing the spacing in millimetres (mm) along each axis of the image data. |
| `image.get_pixel_area()` | Returns the area of one pixel in mm². Requires at least 2 dimensions. |
| `image.get_voxel_volume()` | Returns the volume of one voxel in mm³. Requires at least 3 dimensions. |
| `print(image)` | Displays the image data type, shape, and spacing in the format: `A {dtype} image with shape {shape} and a spacing of {spacing} mm.` |

### DicomImage class

`DicomImage(data, spacing, metadata)` extends `Image` with an additional `metadata` attribute.

- **`data`**: The image pixel data.
- **`spacing`**: The spacing between pixels or voxels along each axis, in millimetres.
- **`metadata`**: A dictionary of DICOM attributes, mapping each attribute keyword to its value. Pixel data is excluded.

### Available functions

| Function | Description |
|---|---|
| `read_dicom(path) -> DicomImage` | Reads a DICOM file or a directory containing a single DICOM series. Slices are sorted by z-position, and pixel values are rescaled to physical values. Raises `ValueError` if the files do not belong to the same series. |
| `read_nifti(path) -> Image` | Reads a NIfTI file and returns an `Image`. |
| `write_nifti(image, path) -> None` | Writes an `Image` to a NIfTI file. |
| `masked_gaussian_filter(image, bool_mask, sigma) -> Image` | Applies Gaussian smoothing within a boolean mask. `sigma` is a tuple specifying the standard deviation in millimetres for each axis. These values are converted to pixels using `image.spacing`. |
| `convert(dicom_path, nifti_path) -> None` | Converts DICOM data to NIfTI format in one step by reading the DICOM input and writing the resulting image to a NIfTI file. |


### Command Line Interface usage (CLI):

To see the instructions on how to use the dicom_to_nifty function from the command line interface.
In the project root:

```bash
$env:PYTHONPATH = "$PWD\src"
python -m pmi_lib.dicom_to_nifti --help
```

To use: 

```bash
dicom-to-nifti path/to/dicom_directory_or_file output.nii.gz
``` 

**Arguments:**

- `path/to/dicom_directory_or_file`: Path to a DICOM file or a directory containing a DICOM series.
- `output.nii.gz`: Path where the output NIfTI file will be saved


### Installation and instruction

Python 3.10 or newer is required.

To test the functions the file test.py can be run, without any modifications to the code. This will first test all the read_dicom, read_nifti, write_nifti and conversion functions, followed by the gaussian filter. Then, the CLI interface of the conversion function is validated. Lastly, both the dicom image and gaussian filtered image are plotted.

#### Running the tests

The test file can be run directly. When encountering problems with importing the functions, in the terminal try:
```
$env:PYTHONPATH = "$PWD\src"
``` 

From the repository root, with the virtual environment activated, run:

```bash
python test.py
```

This uses the example CT dataset in `src/pmi_lib/images/ct_jaw`.

To test with your own DICOM data, different DICOM files can be selected by modifying the paths in test.py line 8.

The test function can also be imported and run in a python script:

```python
from test import test
```

### Library structure
The library structure goes as follows:

```
project/
├── src/
│   └── pmi_lib/
│       ├── images
|       |    └── folder with all dicom and nifti image files. All newly written files are also saved to this folder.
│       ├── dicom_class.py
│       ├── dicom_to_nifti.py
│       ├── image_class.py
│       ├── masked_gaussian_filter.py
│       ├── read_dicom.py
│       ├── read_nifty.py
│       ├── test.py
│       └── write_nifty.py
├── pyproject.toml
├── README.md
├── setup.py
├── MANIFEST.in
└── LICENSE.md
```

