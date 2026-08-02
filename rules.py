"""
Spatial BIM Intelligence Agent
Rule-based design review engine
"""


def check_scale_proportion(data):

    """
    Check building height-to-footprint ratio.
    Detect potentially slender massing.
    """

    issues = []

    bbox = data.get("bbox", {})
    size = bbox.get("size", [])

    if len(size) == 3:

        width = size[0]
        depth = size[1]
        height = size[2]

        footprint = min(width, depth)

        if footprint > 0:

            ratio = height / footprint


            if ratio > 3:

                issues.append(
                    {
                        "type": "Scale Proportion",
                        "severity": "Medium",
                        "object": "Building",
                        "value": round(ratio,2),
                        "message":
                        (
                            f"Building height-to-width ratio is "
                            f"{ratio:.2f}. "
                            "The massing may appear vertically dominant "
                            "and requires spatial proportion review."
                        )
                    }
                )


    return issues



def check_view_coverage(data):

    """
    Check whether enough viewpoints are available
    for architectural evaluation.
    """

    issues = []

    views = data.get("views", [])

    view_names = [
        v.get("name","")
        for v in views
    ]


    required_views = [
        "front",
        "back",
        "left",
        "right"
    ]


    missing = [
        v for v in required_views
        if v not in view_names
    ]


    if len(missing) > 0:

        issues.append(
            {
                "type":"View Coverage",
                "severity":"Low",
                "object":"Visualization",
                "value":missing,
                "message":
                (
                    "Some orthographic views are missing. "
                    "Incomplete viewpoints may limit "
                    "architectural review."
                )
            }
        )


    return issues



def check_unit_consistency(data):

    """
    Check BIM unit normalization.
    """

    issues=[]

    unit=data.get("unit","")


    if "feet" in unit.lower():

        issues.append(
            {
                "type":"Unit Normalization",
                "severity":"Low",
                "object":"BIM Model",
                "value":unit,
                "message":
                (
                    "The model uses Revit internal feet units. "
                    "Unit conversion is recommended before "
                    "cross-platform BIM analysis."
                )
            }
        )


    return issues




def check_camera_distance(data):

    """
    Estimate whether camera views are too far
    for human-scale spatial evaluation.
    """

    issues=[]

    views=data.get("views",[])

    bbox=data.get("bbox",{})

    size=bbox.get("size",[])


    if len(size)==3 and len(views)>0:

        height=size[2]


        for view in views:

            camera=view.get("camera",[])
            target=view.get("target",[])


            if len(camera)==3 and len(target)==3:

                distance=(
                    (camera[0]-target[0])**2 +
                    (camera[1]-target[1])**2 +
                    (camera[2]-target[2])**2
                )**0.5


                if distance > height * 8:

                    issues.append(
                        {
                            "type":"Camera Scale",
                            "severity":"Low",
                            "object":view.get("name"),
                            "value":round(distance,2),
                            "message":
                            (
                                "Camera distance is relatively large "
                                "compared with building height. "
                                "Human-scale spatial perception "
                                "may be difficult to evaluate."
                            )
                        }
                    )

                    break


    return issues




def run_checks(data):

    results=[]


    results.extend(
        check_scale_proportion(data)
    )


    results.extend(
        check_view_coverage(data)
    )


    results.extend(
        check_unit_consistency(data)
    )


    results.extend(
        check_camera_distance(data)
    )


    return results