import random
number = [0,1,2,3,4,5,6,7,8,9]
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.armadillo_model import Armadillo

@app.route('/armadillo_competition/playground/select')
def playground():
    session.clear()
    session['points'] = '***'
    session['pratice'] = True
    return render_template('playground.html')

@app.route('/armadillo_competition/playground/reveal') #Shows if you won the pratice game or not
def pg_reveal():
    return render_template('playground_reveal.html', win_lose=session['win_lose'], what_game=session['what_game'], 
    points=session['points'], sc_guess=session['sc_guess'], one=session['one'], two=session['two'], three=session['three'],
    four=session['four'], five=session['five'], six=session['six'], seven=session['seven'], eight=session['eight'], 
    nine=session['nine'], ten=session['ten']
    )
