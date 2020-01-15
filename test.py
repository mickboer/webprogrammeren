@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")


        return redirect("/")
    else:
        return render_template("register.html")