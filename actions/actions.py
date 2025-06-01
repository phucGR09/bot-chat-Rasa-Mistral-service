import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load Mistral model (chỉnh đúng path đến file gguf)

class ActionAskMusicBot(Action):
    def name(self):
        return "action_ask_music_bot"

    def run(self, dispatcher : CollectingDispatcher, tracker: Tracker, domain : dict)-> list:
        user_input = tracker.latest_message.get("text")

        response = requests.post(
            "http://localhost:8000/generate",
            json={
                "prompt": user_input, 
                "max_tokens": 150
            })
        if response.status_code == 200:
            response_text = response.json()["text"]
        else:
            response_text = "Mình không thể xử lý câu hỏi lúc này."

        dispatcher.utter_message(text=response_text)
        return []
    
class ActionControlMusic(Action):
    def name(self):
        return "action_control_music"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message.get("intent", {}).get("name")
        song_name = next(tracker.get_latest_entity_values("song"), None)

        payload = {
            "intent": intent,
            "song_name": song_name
        }

        try:
            requests.post("http://localhost:3000/api/music-action", json=payload)
        except:
            dispatcher.utter_message(text="Không thể gửi lệnh về app.")
            return []

        dispatcher.utter_message(text="Đã gửi yêu cầu đến app.")
        return []
