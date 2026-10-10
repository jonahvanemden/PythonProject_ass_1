def masked_gaussian_filter(pixel_data, bool_mask, sigma):
    """
        Gaussian smoothing restricted to a mask: M × (G(M×I, σ) / G(M, σ)).

        :param pixel_data: A NumPy array of image pixel data
        :param bool_mask: A boolean NumPy array with same shape as pixel_data
        :param sigma: standard deviation of the gaussian filter sigma (a tuple of floats)
        :returns: float32 NumPy array, same shape as pixel_data, zero outside the mask
        :raises ValueError: if the arguments are incompatible
    """

    pixel_data = pixel_data.astype(np.float32)
    bool_mask = bool_mask.astype(np.float32)

    if bool_mask.dtype != bool:
        raise ValueError(f"mask must be boolean, got dtype {bool_mask.dtype}")
    if pixel_data.shape != bool_mask.shape:
        raise ValueError(
            f"image shape {pixel_data.shape} does not match mask shape {bool_mask.shape}"
        )


    sigma = tuple(sigma)

    if len(sigma) != pixel_data.ndim:
        raise ValueError(
            f"sigma has {len(sigma)} values but image has {pixel_data.ndim} dimensions"
        )

    if any(s < 0 for s in sigma):
        raise ValueError(f"sigma values must be non-negative, got {sigma}")

    bool_mask = np.nan_to_num(bool_mask)

    mi = np.where(pixel_data, bool_mask, 0).astype(np.float32)  # voxel-wise multiplication of pixel_data and the boolean mask

    smoothed_img = gaussian_filter(mi, sigma) # gaussian smoothing of masked image
    smoothed_mask = gaussian_filter(bool_mask, sigma) # Gaussian smoothing of mask

    ratio = np.zeros_like(smoothed_img)
    np.divide(smoothed_img,smoothed_mask, out=ratio, where=smoothed_mask>0) # ratio of gaussian smoothing between masked image and mask

    return bool_mask*ratio
