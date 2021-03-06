import cv2
import numpy as np
from skimage.filters import unsharp_mask

from easycv.transforms.base import Transform
from easycv.transforms.color import GrayScale
import easycv.transforms.edges
from easycv.validators import Number, Type


class Blur(Transform):
    """
    Blur is a transform that blurs an image.

    \t**∙ uniform** - Uniform Filter\n
    \t**∙ gaussian** - Gaussian-distributed additive noise\n
    \t**∙ median** - Median Filter\n
    \t**∙ bilateral** - Edge preserving blur\n

    :param method: Blur method to be used, defaults to "uniform"
    :type method: :class:`str`, optional
    :param size: Kernel size, defaults to auto
    :type size: :class:`int`, optional
    :param sigma: Sigma value, defaults to 0
    :type sigma: :class:`int`, optional
    :param sigma_color: Sigma for color space, defaults to 75
    :type sigma_color: :class:`int`, optional
    :param sigma_space: Sigma for coordinate space, defaults to 75
    :type sigma_space: :class:`int`, optional
    :param truncate: Truncate the filter at this many standard deviations., defaults to 4
    :type truncate: :class:`int`, optional
    """

    methods = {
        "uniform": {"arguments": ["size"]},
        "gaussian": {"arguments": ["size", "sigma", "truncate"]},
        "median": {"arguments": ["size"]},
        "bilateral": {"arguments": ["size", "sigma_color", "sigma_space"]},
    }
    default_method = "gaussian"

    arguments = {
        "size": Number(min_value=1, only_integer=True, only_odd=True, default="auto"),
        "sigma": Number(min_value=0, default=1),
        "sigma_color": Number(min_value=0, default=75),
        "sigma_space": Number(min_value=0, default=75),
        "truncate": Number(min_value=0, default=4),
    }

    def process(self, image, **kwargs):
        if kwargs["method"] == "uniform":
            return cv2.blur(image, (kwargs["size"], kwargs["size"]))
        elif kwargs["method"] == "gaussian":
            if kwargs["size"] == "auto":
                kwargs["size"] = 2 * int(kwargs["sigma"] * kwargs["truncate"] + 0.5) + 1
            return cv2.GaussianBlur(
                image, (kwargs["size"], kwargs["size"]), kwargs["sigma"]
            )
        elif kwargs["method"] == "median":
            return cv2.medianBlur(image, kwargs["size"])
        else:
            if kwargs["size"] == "auto":
                kwargs["size"] = 5
            return cv2.bilateralFilter(
                image, kwargs["size"], kwargs["sigma_color"], kwargs["sigma_space"]
            )


class Sharpness(Transform):
    """
    Sharpness is a transform that measures how sharpen an image is. Images are classified as \
    sharpen when above a certain value of sharpness given by the threshold. \
    Currently supported interpolation methods:

    \t**∙ laplace** - Uses laplacian to calculate Sharpness\n
    \t**∙ fft** - Uses Fast Fourier Transform to calculate Sharpness\n

    :param threshold: Threshold to classify images as sharpen, defaults to 100 (for fft this \
    should be arround 10)
    :type threshold: :class:`int`/:class:`float`, optional
    :param size: Radius around the centerpoint to zero out the FFT shift
    :type size: :class:`int`, optional
    """

    methods = {
        "laplace": {"arguments": ["threshold"]},
        "fft": {"arguments": ["size", "threshold"]},
    }
    default_method = "laplace"

    arguments = {
        "threshold": Number(min_value=0, default=100),
        "size": Number(min_value=0, only_integer=True, default=60),
    }

    outputs = {"sharpness": Number(), "sharpen": Type(bool)}

    def process(self, image, **kwargs):
        grayscale = GrayScale().apply(image)

        if kwargs["method"] == "laplace":
            sharpness = (
                easycv.transforms.edges.Gradient(method="laplace")
                .apply(grayscale)
                .var()
            )
        else:
            h, w = grayscale.shape
            centerx, centery = (int(w / 2.0), int(h / 2.0))
            fft = np.fft.fft2(grayscale)
            fft_shift = np.fft.fftshift(fft)
            size = kwargs["size"]
            fft_shift[
                centery - size : centery + size, centerx - size : centerx + size
            ] = 0
            fft_shift = np.fft.ifftshift(fft_shift)
            recon = np.fft.ifft2(fft_shift)
            sharpness = np.mean(20 * np.log(np.abs(recon)))

        return {"sharpness": sharpness, "sharpen": sharpness >= kwargs["threshold"]}


class Sharpen(Transform):
    """
    Sharpen is a transform that sharpens an image.

    :param sigma: Kernel sigma, defaults to 1
    :type sigma: :class:`float`, optional
    :param amount: Amount to sharpen, defaults to 1
    :type amount: :class:`float`, optional
    :param multichannel: `True` if diferent processing for each color layer `False` otherwise
    :type multichannel: :class:`bool`
    """

    arguments = {
        "sigma": Number(min_value=0, default=1),
        "amount": Number(default=1),
        "multichannel": Type(bool, default=False),
    }

    def process(self, image, **kwargs):
        kwargs["radius"] = kwargs.pop("sigma")
        return unsharp_mask(image, preserve_range=True, **kwargs)
