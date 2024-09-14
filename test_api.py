import requests

# Use the exact ngrok URL with the /predict endpoint
url = 'https://132e-34-87-145-67.ngrok-free.app/predict'  # Append /predict to the ngrok URL

# Define the message you want to send to the model
messages = [
    {"role": "user", "content": "calculate 1+1."}
]

# Send a POST request to the Colab API
try:
    response = requests.post(url, json={"messages": messages})
    
    # Check if the response is successful
    if response.status_code == 200:
        print("Response:", response.json()['response'])
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response Text:", response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
