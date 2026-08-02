import streamlit as st
import json
import os


from rules import run_checks
from parser import summarize_model
from ai_explainer import explain_all


# optional GPT layer

try:
    from ai_multimodal import generate_ai_review
    AI_AVAILABLE = True

except Exception:

    AI_AVAILABLE = False



# =========================
# Page Config
# =========================

st.set_page_config(

    page_title="AI BIM Design Review Agent",

    page_icon="🏗️",

    layout="wide"

)



# =========================
# Title
# =========================

st.title(
    "🏗️ AI BIM Design Review Agent"
)


st.write(
    """
An AI-assisted system for BIM metadata analysis 
and architectural design review.
"""
)



# =========================
# Upload
# =========================

uploaded_file = st.file_uploader(

    "Upload metadata.json",

    type=["json"]

)



if uploaded_file:


    data = json.load(uploaded_file)


    summary = summarize_model(data)


    issues = run_checks(data)


    explanations = explain_all(issues)



    # =========================
    # Model Information
    # =========================

    st.divider()


    st.header(
        "🏢 Model Information"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "Views",

            summary["view_count"]

        )


    with col2:

        st.metric(

            "Semantic Categories",

            len(summary["semantic_categories"])

        )


    with col3:

        st.metric(

            "Issues Detected",

            len(explanations)

        )



    st.subheader(
        "Model Name"
    )


    st.write(
        summary["model_name"]
    )



    st.subheader(
        "Detected Building Elements"
    )


    st.write(

        " | ".join(
            summary["semantic_categories"]
        )

    )



    # =========================
    # Views
    # =========================


    st.divider()


    st.header(
        "👁️ Model Views"
    )


    model_name = summary["model_name"]


    image_folder = os.path.join(

        "data",

        model_name,

        "screenshots"

    )


    view_names = [

        "front",

        "back",

        "left",

        "right",

        "oblique_lb",

        "oblique_rb",

        "oblique_lt",

        "oblique_rt"

    ]



    cols = st.columns(4)



    for i, view in enumerate(view_names):


        image_path = None


        if os.path.exists(image_folder):


            for file in os.listdir(image_folder):


                if file.startswith(view):


                    image_path = os.path.join(

                        image_folder,

                        file

                    )

                    break



        with cols[i % 4]:


            if image_path:


                st.image(

                    image_path,

                    caption=view,

                    use_container_width=True

                )



    # =========================
    # Scale
    # =========================


    st.divider()


    st.header(
        "📐 Building Scale"
    )


    size = summary["bbox_size"]


    if len(size)==3:


        c1,c2,c3 = st.columns(3)


        with c1:

            st.metric(

                "Width",

                f"{size[0]:.2f}"

            )


        with c2:

            st.metric(

                "Depth",

                f"{size[1]:.2f}"

            )


        with c3:

            st.metric(

                "Height",

                f"{size[2]:.2f}"

            )



    # =========================
    # Rule Review
    # =========================


    st.divider()


    st.header(
        "🔍 Rule-based Review"
    )


    if len(explanations)==0:


        st.success(
            "✓ No critical issues detected."
        )


    else:


        for item in explanations:


            st.warning(

                item["issue"]

            )


            st.info(

                item["explanation"]

            )



    # =========================
    # GPT Interpretation
    # =========================


    st.divider()


    st.header(

        "🤖 AI Architectural Interpretation"

    )



    if AI_AVAILABLE:


        try:


            ai_review = generate_ai_review(

                summary,

                explanations

            )


            st.success(

                ai_review

            )


        except Exception as e:


            st.warning(

                "AI explanation unavailable."

            )


            st.write(e)



    else:


        st.info(

            """
GPT interpretation layer is optional.

The current prototype already provides
BIM parsing, rule-based reasoning,
and architectural explanation.
"""
        )