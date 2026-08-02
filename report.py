def generate_report(model, issues):

    print("\n")
    print("=" * 60)
    print("AI BIM DESIGN REVIEW REPORT")
    print("=" * 60)


    print("\nMODEL:")
    print(model.get("model_name"))


    print("\nMODEL INFORMATION:")


    bbox = model.get("bbox", {})
    size = bbox.get("size", [])


    if size:

        print(
            f"- Building dimension: "
            f"{round(size[0],2)} x "
            f"{round(size[1],2)} x "
            f"{round(size[2],2)}"
        )


    print(
        f"- View count: "
        f"{len(model.get('views',[]))}"
    )


    print(
        f"- Semantic categories: "
        f"{len(model.get('semantic_colors',{}))}"
    )


    print("\nDESIGN REVIEW:")


    if len(issues) == 0:


        print(
            """
✓ No critical issues detected.

Design Characteristics:

- The BIM model contains sufficient metadata
  for spatial review.

- The current geometry does not trigger
  major proportion warnings.

- The model representation appears suitable
  for further AI-assisted analysis.
            """
        )

        return



    for i, issue in enumerate(issues):

        print("\n")

        print(
            f"{i+1}. {issue['issue']}"
        )


        print(
            "AI Explanation:"
        )


        print(
            issue["explanation"]
        )


        print(
            "-" * 40
        )