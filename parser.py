import json


def load_model(path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data



def summarize_model(data):

    bbox = data.get("bbox", {})
    size = bbox.get("size", [])

    views = data.get("views", [])

    semantic = data.get("semantic_colors", {})


    summary = {

        "model_name": data.get("model_name"),

        "view_count": len(views),

        "view_names": [
            v.get("name")
            for v in views
        ],

        "bbox_size": size,

        "unit": data.get("unit"),

        "semantic_categories":
            list(semantic.keys())

    }


    return summary



if __name__ == "__main__":


    model = load_model(
        "data/Model_1779022453/metadata.json"
    )


    result = summarize_model(model)


    print("MODEL SUMMARY:")
    print(result)



    from rules import run_checks
    from report import generate_report


    issues=run_checks(model)


    from ai_explainer import explain_all


    explanations = explain_all(issues)


    generate_report(
        model,
        explanations
    )