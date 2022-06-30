import csv 
from demographic import output
from content import get_recommendations

allarticles = []
likedarticles = []
notlikedarticles = []

with open("articles.csv",encoding = "utf-8") as a:
    reader = csv.reader(a)
    data = list(reader)
    allarticles= data[1:]

from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/getarticle")
def getarticle():
    
    return jsonify({
        "data":allarticles[0],
        "status":"success"
    })

@app.route("/likedarticle",methods = ["POST"])
def likedarticle():
    movie = allarticles[0]
    likedarticles.append(movie)
    allarticles.pop(0)
    return jsonify({
        "status":"success"
    }),201

@app.route("/unlikedarticle",methods = ["POST"])
def unlikedarticle():
    movie = allarticles[0]
    notlikedarticles.append(movie)
    allarticles.pop(0)
    return jsonify({
        "status":"success"
    }),201

@app.route("/populararticles")
def popularmovies():
    moviedata = []
    for movie in output:
        data = {
            "title": movie[1],
            "url": movie[0],
            "text": movie[2],
            "lang": movie[3],
            "total_events": movie[4],
        }
        moviedata.append(data)
    return jsonify({
        "data":moviedata,
        "status":"success"
    }),200

@app.route("/recommendedarticles")
def recommended():
    allrecommended = []
    for i in likedarticles:
        output = get_recommendations(i[4])
        for i in output:
            allrecommended.append(i)
    import itertools
    allrecommended.sort()
    allrecommended = list(i for i,_ in itertools.groupby(allrecommended))
    moviedata = []
    for movie in allrecommended:
        data = {
            "title": movie[1],
            "url": movie[0],
            "text": movie[2],
            "lang": movie[3],
            "total_events": movie[4],
        }
        moviedata.append(data)
    return jsonify({
        "data":moviedata,
        "status":"success"
    }),200

if __name__=="__main__":
    app.run()