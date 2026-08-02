from openai import OpenAI
import os


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aigc789.top/v1"
)



def generate_ai_review(summary, explanations):


    prompt = f"""

You are an expert architectural reviewer.

Analyze this BIM design review result.

Model information:

{summary}


Detected findings:

{explanations}


Please provide an architectural interpretation.

Focus on:

1. Spatial characteristics
2. BIM interoperability
3. Possible design implications

Do not simply repeat the rules.
Explain the architectural meaning.

"""


    response = client.chat.completions.create(

        model="gpt-4o",

        messages=[

            {
                "role":"system",
                "content":
                "You are an expert architect and BIM consultant."
            },

            {
                "role":"user",
                "content":prompt
            }

        ],

        temperature=0.3
    )


    # compatible with different API gateways

    if hasattr(response, "choices"):

        return response.choices[0].message.content


    else:

        return str(response)