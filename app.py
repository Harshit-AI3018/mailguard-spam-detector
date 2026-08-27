from flask import Flask, render_template, request, redirect, url_for
import joblib
from database import get_connection


# =========================================
# CREATE FLASK APP
# =========================================

app = Flask(__name__)


# =========================================
# LOAD ML MODEL
# =========================================

model = joblib.load("spam_detector.pkl")


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================
# PREDICT EMAIL
# =========================================

@app.route("/predict", methods=["POST"])
def predict():

    # Get data from website
    sender = request.form["sender"]
    subject = request.form["subject"]
    body = request.form["body"]


    # ML prediction
    prediction = model.predict([body])[0]


    # Convert 1 / 0 into readable text
    if prediction == 1:
        prediction_label = "Spam"
    else:
        prediction_label = "Not Spam"


    # =====================================
    # SAVE TO POSTGRESQL
    # =====================================

    connection = get_connection()
    cursor = connection.cursor()


    query = """
        INSERT INTO emails
        (sender, subject, body, prediction)
        VALUES (%s, %s, %s, %s)
    """


    cursor.execute(
        query,
        (
            sender,
            subject,
            body,
            prediction_label
        )
    )


    connection.commit()


    cursor.close()
    connection.close()


    # =====================================
    # SHOW RESULT
    # =====================================

    return render_template(
        "index.html",
        prediction=prediction_label
    )


# =========================================
# EMAIL HISTORY
# =========================================

@app.route("/history")
def history():

    connection = get_connection()
    cursor = connection.cursor()


    query = """
        SELECT id, sender, subject, body, prediction
        FROM emails
        ORDER BY id DESC
    """


    cursor.execute(query)


    emails = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "history.html",
        emails=emails
    )


# =========================================
# DELETE EMAIL
# =========================================

@app.route("/delete/<int:email_id>", methods=["POST"])
def delete_email(email_id):

    connection = get_connection()
    cursor = connection.cursor()


    query = """
        DELETE FROM emails
        WHERE id = %s
    """


    cursor.execute(
        query,
        (email_id,)
    )


    connection.commit()


    cursor.close()
    connection.close()


    # Return to history page
    return redirect(url_for("history"))


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(debug=True)