def color_schema(color) -> dict:
    return {"ID": color["ID"],
            "Name": color["Name"],
            "Supracolor": color["Supracolor"],
            "RGB": color["RGB"],
            "Bricklink": color["Bricklink"],
            }


def colors_schema(colors) -> list:
    return [color_schema(color) for color in colors]