def item_schema(item) -> dict:
    return {"id": item["id"],
            "color": item["color"],
            "uid": item["uid"],
            "supracolor": item["supracolor"],
            "units": item["units"],
            "box": item["box"],
            "colorid": item["colorid"],
            "section": item["section"]
            }


def items_schema(items) -> list:
    return [item_schema(item) for item in items]