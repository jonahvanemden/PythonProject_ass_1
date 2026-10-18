import numpy as np
from typing import Any
from pmi_lib.image_class import Image

class DicomImage(Image):
    def __init__(self, data : np.ndarray, spacing : tuple[float, ...], metadata : dict[str: Any]):
        super().__init__(data, spacing)

        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary.")

        self.metadata = metadata

data = np.zeros((10, 20, 30)) 
spacing = (1, 0.5, 2)  
metadata = dict()

image = DicomImage(data, spacing, metadata)
print(image)
