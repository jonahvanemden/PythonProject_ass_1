import numpy as np

class image: 
    def __init__(self, data, spacing):
        self.data=np.asarray(data)
        self.spacing=tuple(float(s) for s in spacing)

        if len(self.spacing) != self.data.ndim:
            raise ValueError("Data and spacing are not compatible.")

    
    def __str__(self):  
        return (
            f"A {self.data.dtype} image with shape {self.data.shape} "
            f"and a spacing of {self.spacing} mm."
        )  
    def get_pixel_area(self):
        if self.data.ndim <2:
            raise ValueError("Image must have at least 2 dimensions.")
        # Calculate pixel area in mm²
        return self.spacing[0] * self.spacing[1]
    
    def get_voxel_volume(self):
        if self.data.ndim <3:
            raise ValueError("Image must have at least 3 dimensions.")
        
        # Calculate voxel volume in mm³
        return self.spacing[0] * self.spacing[1] * self.spacing[2]

class DicomImage(image):
    def __init__(self, data, spacing, metadata):
        super().__init__(data, spacing)

        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary.")

        self.metadata = metadata


# Example

data = np.zeros((10, 20, 30)) 
spacing = (1, 0.5, 2)  

image = image(data, spacing)  

print(image)  