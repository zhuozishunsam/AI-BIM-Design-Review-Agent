import os
from parser import load_model, summarize_model
from rules import run_checks


DATA_DIR = "data"


def analyze_all_models():

    results = []


    for folder in os.listdir(DATA_DIR):

        model_path = os.path.join(
            DATA_DIR,
            folder,
            "metadata.json"
        )


        if os.path.exists(model_path):

            print(
                "\nAnalyzing:",
                folder
            )


            model = load_model(model_path)


            summary = summarize_model(model)


            issues = run_checks(model)


            results.append(
                {
                    "model":folder,
                    "summary":summary,
                    "issues":issues
                }
            )


    return results



if __name__=="__main__":


    results = analyze_all_models()


    print("\n")
    print("="*60)
    print("BATCH BIM REVIEW SUMMARY")
    print("="*60)


    for r in results:

        print("\nMODEL:")
        print(r["model"])


        if len(r["issues"])==0:

            print(
                "✓ No issues detected"
            )

        else:

            print(
                "Issues:"
            )

            for issue in r["issues"]:

                print(
                    "-",
                    issue["type"]
                )