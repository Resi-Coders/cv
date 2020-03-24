import cv2

from cv.transforms.base import Transform
from cv.validators import Option, Number


class Blur(Transform):
    """
    This class represents an **Blur**.

    Blur is a transform applies blur on a image

    :param method: Method of blur
    :type method: :class:`str`
    :param size: Size of operator
    :type size: :class:`int`
    :param sigma: Sigma value
    :type sigma: :class:`int`
    :param sigma_color: Sigma for color space
    :type sigma_color: :class:`int`
    :param sigma_space: Filter sigma in coordinate space
    :type sigma_space: :class:`int`
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
