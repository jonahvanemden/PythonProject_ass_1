from .image_class import image

class DicomImage(image):
    def __init__(self, data, spacing, metadata):
        super().__init__(data, spacing)

        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary.")

        self.metadata = metadata
