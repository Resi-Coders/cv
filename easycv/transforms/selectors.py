from matplotlib.widgets import RectangleSelector, EllipseSelector
import matplotlib.pyplot as plt
import matplotlib as mpl

from easycv.transforms.base import Transform
from easycv.validators import Method, Number
from easycv.errors import InvalidSelectionError

from easycv.io.output import prepare_image_to_output

mpl.use("Qt5Agg")


class Select(Transform):

    inputs = {
        "method": Method(
            {"rectangle": [], "point": ["n"], "ellipse": []}, default="rectangle"
        ),
        "n": Number(only_integer=True, min_value=0, default=2),
    }

    def apply(self, image, **kwargs):
        fig, current_ax = plt.subplots()
        plt.tick_params(
            axis="both",
            which="both",
            bottom=False,
            top=False,
            left=False,
            right=False,
            labelbottom=False,
            labelleft=False,
        )

        def empty_callback(e1, e2):
            pass

        def selector(event):
            if event.key in ["Q", "q"]:
                plt.close(fig)

        res = []
        current_ax.imshow(prepare_image_to_output(image))
        plt.gcf().canvas.set_window_title("Selector")

        if kwargs["method"] == "rectangle":
            selector.S = RectangleSelector(
                current_ax,
                empty_callback,
                useblit=True,
                button=[1, 3],
                minspanx=5,
                minspany=5,
                spancoords="pixels",
                interactive=True,
            )
        elif kwargs["method"] == "ellipse":
            selector.S = EllipseSelector(
                current_ax,
                empty_callback,
                drawtype="box",
                interactive=True,
                useblit=True,
            )
        else:

            def onclick(event):
                if event.xdata is not None and event.ydata is not None:
                    res.append((round(event.xdata), round(event.ydata)))
                    plt.plot(
                        event.xdata, event.ydata, marker="o", color="cyan", markersize=4
                    )
                    fig.canvas.draw()
                    if len(res) == kwargs["n"]:
                        plt.close(fig)

            plt.connect("button_press_event", onclick)

        plt.connect("key_press_event", selector)
        plt.show(block=True)

        if kwargs["method"] == "rectangle":
            x, y = selector.S.to_draw.get_xy()
            x = int(round(x))
            y = int(round(y))
            width = round(selector.S.to_draw.get_width())
            height = round(selector.S.to_draw.get_height())

            if width == 0 or height == 0:
                raise InvalidSelectionError("Must select a rectangle.")

            return [(x, y), (x + width, y + height)]

        elif kwargs["method"] == "ellipse":
            width = round(selector.S.to_draw.width)
            height = round(selector.S.to_draw.height)
            center = [round(x) for x in selector.S.to_draw.get_center()]
            if width == 0 or height == 0:
                raise InvalidSelectionError("Must select an ellipse.")
            return {"center": center, "width": width, "height": height}
        else:
            if len(res) != kwargs["n"]:
                raise InvalidSelectionError(
                    "Must select {} points.".format(kwargs["n"])
                )
            return res