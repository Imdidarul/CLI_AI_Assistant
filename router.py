import json

SETTINGS_PATH = "settings.json"

def loadSettings():
    with open(SETTINGS_PATH,"r") as file:
        return json.load(file)

def determineRoute(sensitivity):
    settings = loadSettings()

    result = {
        "route": None,
        "reason": []
    }

    if not settings["cloud_ai_enabled"]:
        result["route"] = "local_ai"
        result["reason"].append('Cloud AI disabled in settings')
        return result
    
    if sensitivity == "secret":
        if settings["send_secret_data_to_cloud"]:
            result["route"] = "cloud_ai"
            result["reason"].append("Secret data is allowed to be sent to ckoud")
        else:
            result["route"] = "local_ai"
            result["reason"].append("Secret data is blocked from being sent to cloud")
    elif sensitivity == "confidential":
        if settings["send_confidential_data_to_cloud"]:
            result["route"] = "cloud_ai"
            result["reason"].append("Confidential data is allowed to be sent to ckoud")
        else:
            result["route"] = "local_ai"
            result["reason"].append("Confidential data is blocked from being sent to cloud")
    elif sensitivity == "personal":
        if settings["send_personal_data_to_cloud"]:
            result["route"] = "cloud_ai"
            result["reason"].append("Personal data is allowed to be sent to ckoud")
        else:
            result["route"] = "local_ai"
            result["reason"].append("Personal data is blocked from being sent to cloud")
    else:
        result["route"] = "cloud_ai"
        result["reason"].append("Public data is unrestricted")
    return result