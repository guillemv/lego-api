def section_schema(section) -> dict:
    schema = {
        "containerId": section["containerId"],
        "used": section["used"],
        "uid": section["uid"]
    }

    # Agregar itemuid solo si está presente en section
    if "itemuid" in section:
        schema["itemuid"] = section["itemuid"]

    return schema


def sections_schema(sections) -> list:
    return [section_schema(section) for section in sections]