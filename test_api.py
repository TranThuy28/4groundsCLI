import requests

# Use the exact ngrok URL with the /predict endpoint appended
url = 'https://58a8-34-87-145-67.ngrok-free.app/predict'  # Ensure /predict is added at the end

# Define the question you want to send to the model
question = "what is git clone?"

# Prepare the payload
payload = {"question": question}

# Send a POST request to the Colab API
try:
    response = requests.post(url, json=payload)
    
    # Check if the response is successful
    if response.status_code == 200:
        print("Response:", response.json()['response'])
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response Text:", response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
