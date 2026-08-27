import joblib
from database import get_connection


# Load ML model
model = joblib.load("spam_detector.pkl")


# Get email details from user
sender = input("Enter sender email: ")
subject = input("Enter email subject: ")
body = input("Enter email body: ")


# ML prediction
prediction = model.predict([body])[0]

if prediction == 1:
    prediction_label = "Spam"
else:
    prediction_label = "Not Spam"

print("\n-----------------------------")
print("Prediction:", prediction)
print("-----------------------------")


# Save to PostgreSQL
connection = get_connection()
cursor = connection.cursor()

query = """
    INSERT INTO emails
    (sender, subject, body, prediction)
    VALUES (%s, %s, %s, %s)
"""

cursor.execute(
    query,
    (sender, subject, body, str(prediction))
)

connection.commit()

cursor.close()
connection.close()

print("Email saved to PostgreSQL!")