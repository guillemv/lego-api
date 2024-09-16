def box_schema(box) -> dict:
    return {"id": box["id"],
            "size": box["size"],
            "supracolor": box["supracolor"],
            }


def boxes_schema(boxes) -> list:
    return [box_schema(box) for box in boxes]