import json
import ollama

def process(content, eventType):
    prompt = f"""Analyze the log Event Type:{eventType} and Content: {content}
        Output only valid JSON
        Do not include explanations
        Do not include markdowns
        Do not add text before or after json(like ```json) return just the json.
        First extract the information and create a one line summary then 
        give a senstivity tier based on these:
        secret: API keys, secret tokens, private keys, database passwords, credentials
        confidential: Intellectual property, financial metrics, proprietary internal business details
        personal: Private conversations, logs, health/medical context, identity documents
        public: Publicly accessible information, general documentation, reference websites

        After that output in this exact JSON structure:-
        {{
        "people": ["Names"],
        "projects": ["System or Project"],
        "topics": ["Topics discussed"],
        "summary": "One line summary",
        "sensitivity": "secret OR confidential OR personal OR public",
        "justification": "Why this sesitivity tier"
        }}
    """
    print("Processing started:-")
    response = ollama.chat(
        model='phi3:mini',
        messages=[
            {'role':'user','content':prompt}
        ],
        options={'temperature':0.0}
    )
    output = response['message']['content'].strip()
    output = output.replace("```json","")
    output = output.replace("```","")
    output = output.strip()
    # print(output)
    return json.loads(output)

# with open('mock_events.json',"r") as file:
#     events = json.load(file)
# for event in events:
#     process(
#         content=event["content"],
#         eventType= event["type"]
    # )