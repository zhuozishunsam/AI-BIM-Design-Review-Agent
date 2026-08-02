def explain_issue(issue):

    """
    Convert technical BIM findings
    into architectural explanation.
    """

    explanations = {


        "Unit Normalization":

        """
        The BIM model is created using Revit internal feet units.
        Before cross-platform analysis or simulation,
        unit normalization is recommended to avoid geometric inconsistency.
        """,



        "Scale Proportion":

        """
        The building shows a strong vertical proportion.
        This may influence perceived spatial balance
        and requires further architectural review.
        """,



        "Camera Scale":

        """
        The selected viewpoints may be too distant
        for evaluating human-scale spatial experience.
        Additional closer views are recommended.
        """

    }


    return explanations.get(
        issue["type"],
        "Further architectural interpretation is required."
    )



def explain_all(issues):

    results=[]


    for issue in issues:

        results.append(
            {
                "issue":issue["type"],
                "explanation":
                    explain_issue(issue)
            }
        )


    return results