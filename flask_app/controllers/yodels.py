from flask_app import app
from flask import render_template, request, redirect, session
from flask_mail import Mail, Message

mail = Mail(app)

from flask_app.models.user import User
from flask_app.models.yodel import Yodel

from flask import flash


# ================================================
# Send Yodel Routes
# ================================================


@app.route("/send_yodel", methods=["POST"])
def add_yodel():
    if not Yodel.validate_yodel(request.form):
        return redirect("/dashboard")

    data = {
        "recipient": request.form['recipient'],
        "content": request.form['content'],
        "public": request.form['public'],
        "user_id": request.form['user_id'],
    }
    Yodel.save(data)

    recipient_email = request.form.get("recipient")
    email_content = request.form.get("content")

    msg = Message(
                'Yodel-Ay-Hee-Hoo',
                sender = 'ee3397196@gmail.com',
                recipients = [recipient_email]
                )
    msg.body = email_content
    mail.send(msg)
    return redirect("/dashboard")


# ================================================
# View Public Yodel Routes
# ================================================
@app.route("/popular_yodels")
def public_yodels():
    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")
    data = {
        "id" : session["user_id"]
    }

    logged_user = User.get_one(data)

    yodel = Yodel.all_public_yodels()
    return render_template("live.html", user = logged_user, yodel = yodel)


# ================================================
# Delete Show Routes
# ================================================

@app.route("/yodel/delete/<int:id>")
def delete_yodel(id):
    data = {
        "id" : id
    }
    Yodel.delete(data)
    return redirect("/popular_yodels")



