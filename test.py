@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")


        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/index", methods=["GET, POST"])
def leaderbord():
    if request.method == "GET":
        leaders_dict = db.execute("SELECT score, level FROM Users")
        print(leaders_dict)
        leaders = leaders_dict.values()
        haal scores en levels er uit
        maakt top 10
   return render_template("index.html")")

one_person = db.execute("SELECT Username, score, level FROM Users")
        level_and_score = sorted(one_person, key=lambda k: (k['level'], k["score"]), reverse=True)[0:10]

        leaderboard_list = [(player["Username"], player["level"], player["score"]) for player in level_and_score]