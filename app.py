from pickle import GET
from traceback import print_tb
from unicodedata import name
from flask import Flask, flash, redirect, render_template, request, url_for, session
import db as fb
import requests as req
import random
import IST_Time as TIME
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = "~!@#$%^&*&^%$#$%^&"


@app.route("/", methods=["GET", "POST"])
@app.route("/login")
def start():
    if request.method == "POST":
        try:
            number = int(request.form.get("mobile"))
            roll = int(request.form.get("roll"))
        except:
            flash("ENTER VAILD DETAILS")
            return render_template("form.html", title="home")

        try:
            retrive_data = dict(fb.db.child("users").child(str(roll)).get().val())
            print(retrive_data)
            session["retrive_data"] = retrive_data
        except:
            flash("ENTER A VALID ROLL NUMBER")
            return render_template("form.html", title="home")

        if str(retrive_data["MOB"]) == str(number):
            number = str(number)
            verification = random.randint(105545, 987512)
            message_var = verification
            try:
                r = req.get(
                    f"https://www.fast2sms.com/dev/bulkV2?authorization=api_key&sender_id=Cghpet&message={message_var}&language=english&flash=0&numbers={number}"
                )
                # print(r.json())
                dict1 = r.json()
            except:
                flash("SMS NOT WORKING")
                return render_template("form.html", title="home")

            if dict1["message"] == ["SMS sent successfully."]:
                # print("Success")
                flash("OTP SENT")
                session["roll"] = roll
                session["verification"] = verification
                session["count"] = 0  # modify count here fix count session
                # print("VERIFY : ", verification)
                return redirect(
                    url_for("start1")
                )  # url_for('start1', VERIFY= verification, DATA=roll))

            elif dict1["message"] == "Invalid Numbers":
                flash("ENTER VAILD NUMBER")
                return render_template("form.html", title="home")
            else:
                print(verification)
                session["roll"] = roll
                session["verification"] = verification
                session["count"] = 0  # modify count here fix count session
                # print("VERIFY : ", verification)
                flash("SMS NOT SENT, SEE ON TERMINAL")
                return redirect(
                    url_for("start1")
                )  # url_for('start1', VERIFY= verification, DATA=roll))

                # print("FAIL")
                # flash ('ENTER VAILD DETAILS')
                # return render_template('form.html', title = 'home')
        else:
            flash("YOU ARE NOT ARE REGISTERED.")
            return render_template("form.html", title="home")

    else:
        if (
            "roll" in session
            and "verification_done" in session
            and "retrive_data" in session
        ):
            flash("YOU ARE ALREADY LOGGED IN")
            return redirect(url_for("start2"))
        return render_template("form.html", title="home")


@app.route("/OTP", methods=["GET", "POST"])
def start1():
    #     session['count']= 0 #modify count here fix count session
    # VERIFY = request.args.get('VERIFY')
    # DATA = request.args.get('DATA')
    if request.method == "POST":
        verify_token = request.form.get("OTP")
        # print(verify_token)
        # flash (f'OTP SENT TO {number}')
        try:
            verify_token
        #             print(verify_token)
        except:
            flash("ENTER VALID VALUE")
            return render_template("otp.html", title="OTP VERIFY")
        # return render_template('otp.html', title='OTP VERIFY')
        if int(verify_token) == int(session["verification"]):
            flash("WELCOME TO THE ISSUING SYSTEM")
            session["verification_done"] = "DONE"
            session.pop("count", None)  # fix count
            # VERIFY = 0
            return redirect(url_for("start2"))
        else:
            session["count"] = int(session["count"]) + 1  # modify count
            if session["count"] == 2:
                flash("FAILD ATTEMPT TRY AGAIN LATER")  # modify count
                session.pop("retrive_data", None)
                session.pop("roll", None)
                session.pop("verification", None)
                session.pop("count", None)  # fix count in session
                return redirect(url_for("start"))  # count
            flash("FAIL, TRY AGAIN")
            # return redirect(url_for('start'))
            return render_template("otp.html", title="OTP VERIFY")
    else:
        if "roll" not in session:
            flash("ENTER MOBILE NUMBER FIRST.")
            return redirect(url_for("start"))

        else:
            if (
                "roll" in session
                and "verification_done" in session
                and "retrive_data" in session
            ):
                flash("YOU ARE ALREADY LOGGED IN!")
                return redirect(url_for("start2"))
            if "roll" in session:
                # flash(f'HI {VERIFY}')
                return render_template("otp.html", title="OTP VERIFY")
            else:
                return redirect(url_for("start"))


@app.route("/details", methods=["GET", "POST"])
def start2():
    # DATA = request.args.get('DATA')
    book = ["BOOK1", "BOOK2", "BOOK3", "BOOK4"]
    if request.method == "POST":
        # print(request.form.get('select_book'))
        a = request.form.get("select_book")
        a = str(a)
        if a in book:
            if (
                int(session["retrive_data"]["NOC"]) > 0
                and int(session["retrive_data"][f"{a}"]["NO_ISSUE"]) <= 1
            ):
                # print(a)
                ISSUE_TODAY = TIME.ISSUE()
                # print(ISSUE_TODAY)
                fb.db.child("users").child(
                    f"{session['retrive_data']['Roll_No']}"
                ).child(f"{a}").update({"DATE_REISSUE": f"{ISSUE_TODAY}"})
                ISSUE_EXPIRE = TIME.REISSUE(ISSUE_TODAY)
                # print(f'\n{ISSUE_EXPIRE}')
                fb.db.child("users").child(
                    f"{session['retrive_data']['Roll_No']}"
                ).child(f"{a}").update({"DATE_RETURN": f"{ISSUE_EXPIRE}"})
                session["NOC"] = int(session["retrive_data"]["NOC"]) - 1
                fb.db.child("users").child(
                    f"{session['retrive_data']['Roll_No']}"
                ).update({"NOC": f'{session["NOC"]}'})
                session["NOC_BOOK_SELECT"] = (
                    int(session["retrive_data"][f"{a}"]["NO_ISSUE"]) + 1
                )
                fb.db.child("users").child(
                    f"{session['retrive_data']['Roll_No']}"
                ).child(f"{a}").update({"NO_ISSUE": f'{session["NOC_BOOK_SELECT"]}'})
                flash("BOOK WAS REISSUED")
                session.pop("NOC", None)
                session.pop("NOC_BOOK_SELECT", None)
                if (
                    "retrive_data" in session
                    and "roll" in session
                    and "verification_done" in session
                ):  # count
                    try:
                        retrive_data = dict(
                            fb.db.child("users").child(str(session["roll"])).get().val()
                        )
                        session["retrive_data"] = retrive_data
                    except:
                        flash("FAIL TRY AGAIN LATER")
                        session.pop("retrive_data", None)
                        session.pop("roll", None)
                        session.pop("verification", None)
                        session.pop("verification_done", None)
                        return redirect(url_for("start"))
                    return render_template(
                        "details.html",
                        title="Details",
                        data=session["retrive_data"],
                        book=["BOOK1", "BOOK2", "BOOK3", "BOOK4"],
                    )
                    # return redirect(url_for('start2'))
            else:
                flash("MAX ISSUE REACHED")
                return redirect(url_for("start2"))

            # print('TRUE')
        logout = request.form.get("logout")
        session.pop("retrive_data", None)
        session.pop("roll", None)
        session.pop("verification", None)
        session.pop("verification_done", None)
        return redirect(url_for("start"))

    if (
        "retrive_data" in session
        and "roll" in session
        and "verification_done" in session
    ):  # count
        if str(session["roll"]) == str(session["retrive_data"]["Roll_No"]):
            try:
                retrive_data = dict(
                    fb.db.child("users").child(str(session["roll"])).get().val()
                )
                session["retrive_data"] = retrive_data
                return render_template(
                    "details.html",
                    title="Details",
                    data=session["retrive_data"],
                    book=["BOOK1", "BOOK2", "BOOK3", "BOOK4"],
                )
            except:
                flash("FAIL TRY AGAIN LATER")
                session.pop("retrive_data", None)
                session.pop("roll", None)
                session.pop("verification", None)
                session.pop("verification_done", None)
                return redirect(url_for("start"))
                # return render_template('details.html', title='Details', data = session['retrive_data'], book = ['BOOK1', 'BOOK2','BOOK3', 'BOOK4'])
    else:
        flash("LOGIN FIRST")
        return redirect(url_for("start"))


@app.errorhandler(404)
@app.errorhandler(500)
def anything(e):
    return redirect(url_for("start"))


if __name__ == "__main__":
    app.run()
