import json
import sys
from extractLocally import process
from storage import(
    createDatabases,
    saveRawEvent,
    saveMemory,
    deleteMemoriesBefore,
    deleteMemoriesAfter,
    wipeAll
)
from search import searchMemories
from router import determineRoute



def processLocally(memory,event):
    saveMemory(
        memory,
        event["timestamp"]
    )
    print("Processing done and data saved successfully")


def search(query):
    results = searchMemories(query)
    print(json.dumps(results, indent=4))

def deleteBefore(timestamp):
    print(f"Deleting all memories before:-{timestamp}")
    deleteMemoriesBefore(timestamp)

def deleteAfter(timestamp):
    print(f"Deleting all memories after:-{timestamp}")
    deleteMemoriesAfter(timestamp)

def wipe():
    print("Deleting all data")
    wipeAll()


def ingest():
    print("Loading events")

    with open("mock_events.json","r") as file:
        events = json.load(file)
    
    for event in events:
        print("Processing Data")
        saveRawEvent(event)

        try:
            memory = process(
                content=event["content"],
                eventType=event["type"]
            )
            routingDecision = determineRoute(
                memory["sensitivity"]
            )
            print(json.dumps(routingDecision, indent=4))

            if routingDecision["route"] == "local_ai":
                processLocally(memory, event)
            elif routingDecision["route"] == "cloud_ai":
                print("Processing in cloud")
            elif routingDecision["route"] == "blocked":
                print("Blocked by policy")
                continue
        except Exception as e:
            print(f"Processing could not be done: {e}")

if __name__ == "__main__":
    print("Creating databases")
    createDatabases()
    if len(sys.argv) > 2 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:])
        search(query)
    elif len(sys.argv) > 2 and sys.argv[1] == "delete-before":
        timestamp = sys.argv[2]
        deleteBefore(timestamp)
    elif len(sys.argv) > 2 and sys.argv[1] == "delete-after":
        timestamp = sys.argv[2]
        deleteAfter(timestamp)
    elif len(sys.argv) > 1 and sys.argv[1] == "wipe-all":
        wipe()
    else:
        ingest()