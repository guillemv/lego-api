def container_schema(container) -> dict:
    return {"id": container["id"],
            "size": container["size"],

            }


def containers_schema(containers) -> list:
    return [container_schema(container) for container in containers]