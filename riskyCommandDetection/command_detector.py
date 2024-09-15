import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Function to preprocess the command
def preprocess_command(command):
    # Remove special characters and convert to lowercase
    return re.sub(r'[^a-zA-Z0-9\s]', '', command.lower())

# Function to load data from a file
def load_data_from_file(filename):
    commands = []
    labels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if '|' in line:
                command, label = line.rsplit('|', 1)
                commands.append(preprocess_command(command.strip()))
                labels.append(int(label.strip()))
    return commands, labels

# Load the data
filename = 'command.txt'  # Make sure this file exists in the same directory as the script
commands, labels = load_data_from_file(filename)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(commands, labels, test_size=0.2, random_state=42)

# Create a bag of words representation
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

# Evaluate the model
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred, target_names=['Non-Risky', 'Risky']))

# Function to classify a new command
def classify_command(command):
    preprocessed = preprocess_command(command)
    vec = vectorizer.transform([preprocessed])
    prediction = clf.predict(vec)[0]
    return "Risky" if prediction == 1 else "Non-Risky"

# Example usage
print(classify_command("ls -l"))
print(classify_command("rm -rf /"))

# Interactive command line interface
if __name__ == "__main__":
    while True:
        user_input = input("Enter a command to classify (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        print(f"Classification: {classify_command(user_input)}")