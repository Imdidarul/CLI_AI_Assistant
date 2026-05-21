import sqlite3
import json
import ollama

MEMORY_DB_PATH = "./storage/database/memories.db"

def searchMemories(query):
    results = []

    print("Loading memories...")

    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            summary,
            sensitivity,
            justification,
            people,
            projects,
            topics,
            timestamp
        FROM memories
        """)
        
        rows = cursor.fetchall()
    print("Memories loaded")
    print("Searching...")
    for row in rows:
        memory = {
            "summary": row[0],
            "sensitivity": row[1],
            "justification": row[2],
            "people": json.loads(row[3]),
            "projects": json.loads(row[4]),
            "topics": json.loads(row[5]),
            "timestamp": row[6]
        }

        memoryText = f"""
            Summary: {memory["summary"]}
            People: {memory["people"]}
            Projects: {memory["projects"]}
            Topics: {memory["topics"]}
        """

        prompt = f""" User search query:{query}
            Memory:{memoryText}

            Check if this memory is relevant.
            Answer with only yes or no.
            Do not add any explanation
            Do not add any validation.
            Rules:
            Answer yes if the memory explicitly discusses or strongly relates to the search query.
            Answer no if the memory is weak, indirect or doesnot have any connection to the search query.
            Look carefully and do not give vague answer
        """
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            options={'temperature':0}
        )
        # print(response)
        answer = response["message"]["content"].strip().lower()
        # print(answer)
        if 'yes' in answer:
            results.append(memory)
    return results