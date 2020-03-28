import cv2

from easycv.transforms.base import Transform
from easycv.validators import Option, Number


class Blur(Transform):
    """
    Blur is a transform that applies blur on a image

    :param method: Method of the blur to be aplied, defaults to "uniform"
    :type method: :class:`str`, optional
    :param size: Size of operator, defaults to 5
    :type size: :class:`int`, optional
    :param sigma: Sigma value, defaults to 0
    :type sigma: :class:`int`, optional
    :param sigma_color: Sigma for color space, defaults to 75
    :type sigma_color: :class:`int`, optional
    :param sigma_space: Filter sigma in coordinate space, defaults to 75
    :type sigma_space: :class:`int`, optionals
    """

    default_args = {
        "method": Option(["uniform", "gaussian", "median", "bilateral"], default=1),
        "size": Number(min_value=1, only_integer=True, only_odd=True, default=5),
        "sigma": Number(min_value=0, default=0),
        "sigma_color": Number(min_value=0, default=75),
        "sigma_space": Number(min_value=0, default=75),
    }

    def apply(self, image, **kwargs):
        if kwargs["method"] == "uniform":
            return cv2.blur(image, (kwargs["size"], kwargs["size"]))
        elif kwargs["method"] == "gaussian":
            return cv2.GaussianBlur(
                image, (kwargs["size"], kwargs["size"]), kwargs["sigma"]
            )
        elif kwargs["method"] == "median":
            return cv2.medianBlur(image, kwargs["size"])
        else:
            return cv2.bilateralFilter(
                image, kwargs["size"], kwargs["sigma_color"], kwargs["sigma_space"]
            )