import numpy as np

class Image: 
    def __init__(self, data : np.ndarray, spacing : tuple[float, ...]):
        self._data=np.asarray(data)
        self.spacing=tuple(float(s) for s in spacing)

        if len(self.spacing) != self._data.ndim:
            raise ValueError("Data and spacing are not compatible.")

    def __str__(self) -> str:  
        return (
            f"A {self._data.dtype} image with shape {self._data.shape} "
            f"and a spacing of {self.spacing} mm."
        )  
    def get_pixel_area(self) -> float:
        if self._data.ndim <2:
            raise ValueError("Image must have at least 2 dimensions.")
        # Calculate pixel area in mm^2
        return self.spacing[0] * self.spacing[1]
    
    def get_voxel_volume(self) -> float:
        if self._data.ndim <3:
            raise ValueError("Image must have at least 3 dimensions.")
        
        # Calculate voxel volume in mm^3
        return self.spacing[0] * self.spacing[1] * self.spacing[2]

    def __len__(self) -> int
        # return the size of the outer dim
        return self._data.shape[0]

    def __array__(
        self, 
        dtype: np.typing.DTypeLike | None = None, 
        *, 
        copy: bool | None = None
    ) -> np.ndarray
        #  return the pixel data with the specified pixel data type
        if dtype is None: 
            dtype = self._data.dtype
        return self._data.astype(dtype, copy=copy)

    def __getitem__(self, key: Any) -> np.ndarray 
        # enables data indexing
        return data[key]
        

# data = np.zeros((10, 20, 30)) 
# spacing = (1, 0.5, 2)  

# image = Image(data, spacing)  

# print(image)  
