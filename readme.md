# **Local AI CLI Assistant**



A local AI CLI Assistant that ingests activity logs then extracts structured json using local LLM, classifies the sensitivity of the data, stores the data and this data can be semantically searched through CLI.



### **FEATURES**



**- Local ingestion of JSON events**

**- AI-powered structured memory extraction using Ollama (`phi3:mini`)**

**- Sensitivity classification:**

&#x20; **- `secret`**

&#x20; **- `confidential`**

&#x20; **- `personal`**

&#x20; **- `public`**

**- Separation of raw events and structured memories**

**- Local SQLite persistence**

**- Semantic memory search**

**- Local-first AI routing policy**

**- Data deletion support**

**- Full local data wipe support**





### **Architecture**





mock\_events.json

&#x20;       ↓

cliMine.py

&#x20;       ↓

extractLocally.py

&#x20;       ↓

router.py

&#x20;       ↓

storageMine.py

&#x20;       ↓

SQLite Databases









### **Project Structure**

**project/**



**│**

**├── cli.py**

**├── extractLocally.py**

**├── search.py**

**├── storage.py**

**├── router.py**

**├── settings.json**

**├── mock\_events.json**

**│**

**├── storage/**

**│   └── database/**

**│       ├── rawEvents.db**

**│       └── memories.db**

**│**

**└── README.md**





### **REQUIREMENTS**



**Python**

**Python 3.10+**



##### **Install dependencies**



**pip install ollama**



**Install Ollama:**



**https://ollama.com/download**



**Pull the model:**



**ollama pull phi3:mini**



**Start Ollama:**



**ollama serve**









##### **Configuration**



Create `settings.json`

{

&#x20;   "cloud\_ai\_enabled": true,

&#x20;   "send\_personal\_data\_to\_cloud": false,

&#x20;   "send\_confidential\_data\_to\_cloud": false,

&#x20;   "send\_secret\_data\_to\_cloud": false

}



This file controls AI routing behavior.



create mock\_events.json



\[

&#x20;   {

&#x20;       "type":"transcript",

&#x20;       "app":"Slack",

&#x20;       "source":"Engineering Channel",

&#x20;       "content":"Rahul said we should not expose the Stripe secret key in our frontend.",

&#x20;       "timestamp":"2026-05-19T10:30:00Z"

&#x20;   }

]











##### **Running the Application**



###### **Ingest events**



Example:-

python cliMine.py



Processes events and stores extracted memories.





###### **Search memories**



Example:-

python cliMine.py search "Stripe"



Example Output:-

\[

&#x20;   {

&#x20;       "people":\["Rahul"],

&#x20;       "projects":\["pricing page payment intent creation"],

&#x20;       "topics":\["Stripe","Backend Security"],

&#x20;       "summary":"Discussed moving payment intent creation to backend.",

&#x20;       "sensitivity":"secret",

&#x20;       "timestamp":"2026-05-19T10:30:00Z"

&#x20;   }

]



###### 

###### 

###### **Delete memories before timestamp**



Example:-

python cliMine.py delete-before "2026-05-19T11:00:00Z"



Deletes all memories and raw event data from the database before the given timestamp.





###### **Delete memories after timestamp**



Example:-

python cliMine.py delete-after "2026-05-19T11:00:00Z"



Deletes all memories and raw event data from the database after the given timestamp.





###### **Wipe all data**



Example:-

python cliMine.py wipe-all



Deletes all raw events and memories from the database.









##### **Privacy \& Security Design**



###### **Data Separation**



Raw historical logs and extracted memories are stored independently:



rawEvents.db contains:-

\- original event payloads

\- unprocessed workstation activity



memories.db contains:-

\- extracted structured memory objects

\- sensitivity labels

\- summarized information





###### **Sensitivity Classification**



The data are classified into:-

|Secret 	| API keys, credentials, tokens 	|

|Confidential 	| Internal business information 	|

|Personal 	| Health data, private conversations 	|

|Public 	| General public information 		|













