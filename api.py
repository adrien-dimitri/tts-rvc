import requests
import json
import time

url = "http://127.0.0.1:8000/generate"

payload = json.dumps({
  "speaker_name": "freeman",
  "input_text": "Welcome to the Virtual Reality AI Museum, where technology and history intertwine to offer an immersive journey through the realms of artificial intelligence (AI). As you step into this digital sanctuary, prepare to be transported into a realm where the past, present, and future of AI converge.",
  "emotion": "Calm",
  "speed": 0.5
})
headers = {
  'Content-Type': 'application/json'
}

start_time = time.time()  # Start the timer

response = requests.request("POST", url, headers=headers, data=payload)

end_time = time.time()  # Stop the timer

if response.status_code == 200:
    audio_content = response.content
    
    # Save the audio to a file
    with open("generated_audio.wav", "wb") as audio_file:
        audio_file.write(audio_content)
        
    print("Audio saved successfully.")
    print("Time taken:", end_time - start_time, "seconds")
else:
    print("Error:", response.text)
