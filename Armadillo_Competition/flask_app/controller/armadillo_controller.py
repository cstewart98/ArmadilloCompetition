import random
number = [0,1,2,3,4,5,6,7,8,9]
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.armadillo_model import Armadillo

@app.route('/') #Just redirects to a diffrent link w/ the home page of game
def start():
    session.clear()
    return redirect('/armadillo_competition/home') #The actual home page; resetting session

@app.route('/armadillo_competition/you_lose') #Takes you to the "You lose" page
def you_lose():
    return render_template('you_lose.html')

@app.route('/armadillo_competition/home') #The ACTUAL home page of game 
def home():
    session['points'] = 0
    return render_template('index.html')

@app.route('/armadillo_competition/add_user')
def add_user():
    session['pratice'] = False
    name = session['name']
    points = session['points']

    data = {
        'name': name,
        'points': points,
    }

    user_id = Armadillo.create(data)
    session['user_id'] = user_id
    return redirect("/armadillo_competition/leaderboard")

@app.route('/armadillo_competition/leaderboard') #Jumps to the Leaderboard page
def leaderboard():
    all_score = Armadillo.get_all()
    return render_template('leaderboard.html', all_score=all_score)

@app.route('/armadillo_competition/signup') #Explains the rules & User enter a name
def signup():
    return render_template('signup.html')

@app.route('/armadillo_competition/validator', methods=['POST'])
def user_reg():
    if not Armadillo.validator(request.form):
        return redirect('/armadillo_competition/signup')
    else:
        session['name'] = request.form['name']
        return redirect('/armadillo_competition/speed_counter/rules')

@app.route('/armadillo_competition/speed_counter/rules') #Explains the rules of "Speed Counter"
def game_one_rules():
    session['what_game'] = 'Speed Counter'
        
    session['one']=random.choice(number)
    session['two']=random.choice(number)
    session['three']=random.choice(number)
    session['four']=random.choice(number)
    session['five']=random.choice(number)
    session['six']=random.choice(number)
    session['seven']=random.choice(number)
    session['eight']=random.choice(number)
    session['nine']=random.choice(number)
    session['ten']=random.choice(number)
    session['check'] = session['one'] + session['two'] + session['three'] + session['four'] + session['five'] + session['six'] + session['seven'] + session['eight'] + session['nine'] + session['ten'] #Getting the actual answer to "Speed Counter"
    return render_template('speed_counter_rules.html')

@app.route('/armadillo_competition/speed_counter/play') #Play "Speed Counter"
def speed_counter():
    return render_template('speed_counter.html', one=session['one'], two=session['two'], three=session['three'], four=session['four'], five=session['five'], six=session['six'], seven=session['seven'], eight=session['eight'], nine=session['nine'], ten=session['ten'], points=session['points'])

@app.route('/armadillo_competition/speed_counter/check', methods=['POST']) #Check to see if your answer is correct
def sc_check():

    # if session['pratice'] == True: #Check to see if you're in Pratice Mode/Playground
    #     session['sc_guess'] = request.form['sc_guess']

    #     if session['sc_guess'] == '': #If you enter a blank response, you lose automatically
    #         session['sc_guess'] = '?'
    #         session['win_lose'] = 'YOU LOSE!'
    #         return redirect('/armadillo_competition/playground/reveal')
    #     elif int(request.form['sc_guess']) == session['check']: #Got the answer correct
    #         session['what_game'] = 'Speed Counter'
    #         session['win_lose'] = 'YOU WIN!'
    #     else: #Got the answer wrong
    #         session['win_lose'] = 'YOU LOSE!'
    #     return redirect('/armadillo_competition/playground/reveal')
            

    if request.form['sc_guess'] == '': #If you enter a blank request.form, then you lose
        return redirect('/armadillo_competition/you_lose')
    if int(request.form['sc_guess']) == session['check']:
        session['points'] += 250
        return redirect('/armadillo_competition/shuffle_the_es/rules') #If right, go to next game
    else:
        return redirect('/armadillo_competition/you_lose') #If wrong, go to "You lose" page
    
@app.route('/armadillo_competition/shuffle_the_es/rules') #Show the rules to "Shuffle the E's"
def ste():
    
    
    
    
    
    
    
    
    
    
    
    
    
    session['letters'] = ['Eeeee', 'eEeee', 'eeEee', 'eeeEe', 'eeeeE', 'Eeeee', 'eEeee', 'eeEee', 'eeeEe', 'eeeeE']
    session['double'] = ''
    session['repeat'] = 0
    return render_template('shuffle_the_es_rules.html')

@app.route("/armadillo_competition/shuffle_the_es/play")
def shuffle_the_es():
    session['lookat'] = random.choice(session['letters'])
    if session['double'] == session['lookat']:
        return redirect("/armadillo_competition/shuffle_the_es/play")
    return render_template('shuffle_the_es.html', points=session['points'], letters=session['lookat'])

@app.route('/test')
def test():
    session['repeat'] += 1
    if session['repeat'] != 20:
        return redirect('/armadillo_competition/shuffle_the_es/play')
    else:
        return redirect('/armadillo_competition/shuffle_the_es/guess')

@app.route("/armadillo_competition/shuffle_the_es/guess")
def ste_guess():
    return render_template('shuffle_the_es_guess.html', points=session['points'])

@app.route("/armadillo_competition/shuffle_the_es/check", methods=['POST'])
def check():
    session['ste_number'] = int(request.form['ste_number'])
    index = session['ste_number'] - 1
    if session['ste_number'] > 5 or session['ste_number'] < 1: #Checking to see if your answer is where E is at
        return redirect('/armadillo_competition/you_lose')

    if session['lookat'][index] == 'E':
        session['points'] += 250
        return redirect('/armadillo_competition/an_eye_for_numbers/rules')
    else:
        return redirect('/armadillo_competition/you_lose')

@app.route("/armadillo_competition/an_eye_for_numbers/rules") #Go to rules for "An Eye for Numbers"
def aefn_rules():
    session['long_number'] = random.randrange(1000000000,9999999999)
    return render_template('an_eye_for_numbers_rules.html')

@app.route('/armadillo_competition/an_eye_for_numbers/play')
def aefn():
    return render_template('an_eye_for_numbers.html', points=session['points'], long_number=session['long_number'])

@app.route('/armadillo_competition/an_eye_for_numbers/guess')
def aefn_input():
    return render_template('an_eye_for_numbers_guess.html', points=session['points'])

@app.route('/armadillo_competition/an_eye_for_numbers/check', methods=['POST'])
def aefn_check():
    matches = 0
    session['aefn_guess'] = request.form['aefn_guess']
    stype = type(session['aefn_guess'])
    one = str(session['long_number']) 
    two = str(session['aefn_guess'])
    three = [1,2,3,4,5,6,7,8,9]

    for x in three: #Checking if your guess[x] = long_number[x]
        if one[x] == two[x]:
            matches += 1 #Adds point for whenever they match

    if matches > 5:
        session['points'] += 250
        return redirect('/armadillo_competition/odd_one_out/rules')
    else:
        return redirect('/armadillo_competition/you_lose')
    
@app.route('/armadillo_competition/odd_one_out/rules')
def ooo_rules():
    session['gridArr'] = []
    bunch_let = 99
    grid_let = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    many_let = random.choice(grid_let)
    grid_let.remove(many_let)
    session['odd_let'] = random.choice(grid_let)

    #Adds a bunch of many_let's to gridArr & then add odd_let
    while bunch_let != 0:
        session['gridArr'].append(many_let)
        bunch_let -= 1

    session['gridArr'].append(session['odd_let'])
    random.shuffle(session['gridArr']) 
    return render_template('odd_one_out_rules.html')

@app.route("/armadillo_competition/odd_one_out/play")
def ooo_play():
    return render_template('odd_one_out.html', gridArr=session['gridArr'], points=session['points'])

@app.route("/armadillo_competition/odd_one_out/check", methods=['POST'])
def ooo_check():
    session['odd'] = request.form['odd']
    if session['odd'] == session['odd_let']:#Check to see if your answer is the Odd One Out
        session['points'] += 250
        return redirect('/armadillo_competition/mastermind/rules')
    else:
        return redirect('/armadillo_competition/you_lose')

@app.route('/armadillo_competition/mastermind/rules')
def mm_rules():
    session['bank'] = []
    code = 4
    digits = ['1','2','3','4','5','6','7','8','9','0']
    session['attempts'] = 9
    session['codeA']=random.choice(digits) #Sets up the desired combination
    session['codeB']=random.choice(digits)
    session['codeC']=random.choice(digits)
    session['codeD']=random.choice(digits)
    session['code'] = session['codeA']+session['codeB']+session['codeC']+session['codeD']
    print(session['code'])

    session['digitA'] = '*'
    session['digitB'] = '*'
    session['digitC'] = '*'
    session['digitD'] = '*'
    
    return render_template('mastermind_rules.html')

@app.route('/armadillo_competition/mastermind/play')
def mm():
    session['combo'] = session['digitA'] + session['digitB'] + session['digitC'] + session['digitD']
    if session['attempts'] == 0:
        return redirect('/armadillo_competition/you_lose')
    return render_template('mastermind.html', points=session['points'], combo=session['combo'],attempts=session['attempts'], bank=session['bank'])

@app.route('/armadillo_competition/mastermind/check', methods=['POST'])
def mm_check():
    session['mm_guess1']=request.form['mm_guess1']
    session['mm_guess2']=request.form['mm_guess2']
    session['mm_guess3']=request.form['mm_guess3']
    session['mm_guess4']=request.form['mm_guess4']
    righto= 0

    session['digitA']=''
    session['digitB']=''
    session['digitC']=''
    session['digitD']=''
    session['combo']=''
    session['my_guess'] = session['mm_guess1'] + session['mm_guess2'] + session['mm_guess3'] + session['mm_guess4']
    session['bank'].append(session['my_guess'])

    if session['mm_guess1'] == session['codeA']:
        session['digitA'] = session['mm_guess1']
        righto +=1
    else:
        session['digitA'] = '*'

    if session['mm_guess2'] == session['codeB']:
        session['digitB'] = session['mm_guess2']
        righto += 1
    else:
        session['digitB'] = '*'

    if session['mm_guess3'] == session['codeC']:
        session['digitC'] = session['mm_guess3']
        righto += 1
    else:
        session['digitC'] = '*'

    if session['mm_guess4'] == session['codeD']:
        session['digitD'] = session['mm_guess4']
        righto += 1
    else:
        session['digitD'] = '*'

    session['combo'] = session['digitA'] + session['digitB'] + session['digitC'] + session['digitD']
    
    if righto == 4:
        session['points'] += 250
        return redirect('/armadillo_competition/rock_paper_scissors/rules')

    
    session['attempts'] -= 1
    return redirect('/armadillo_competition/mastermind/play')

@app.route('/armadillo_competition/rock_paper_scissors/rules') #Go to the "Rock, Paper, Scissors" game
def rps_rules():

    return render_template('rock_paper_scissors_rules.html')

@app.route('/armadillo_competition/rock_paper_scissors/play')
def rps():
    return render_template('rock_paper_scissors.html', points=session['points'])

@app.route('/armadillo_competition/rock_paper_scissors/reveal', methods=['POST'])
def rps_reveal():
    weapon = ['Rock', 'Paper', 'Scissors']
    session['you_rps'] = request.form['you_rps']
    session['com_rps'] = random.choice(weapon)
    return render_template('rock_paper_scissors_results.html', points=session['points'], you_rps=session['you_rps'], com_rps=session['com_rps'])

@app.route("/armadillo_competition/rock_paper_scissors/final") #Consequence of results
def rps_conseq():
    if session['you_rps'] == session['com_rps']: #If tied, go back & play again
        return redirect("/armadillo_competition/rock_paper_scissors/play")
    
    if session['you_rps'] =='Rock':
        if session['com_rps'] == 'Paper':
            return redirect('/armadillo_competition/you_lose')
        else:
            session['points'] += 250
            return redirect('/armadillo_competition/speed_counter/rules')

    if session['you_rps'] =='Paper':
        if session['com_rps'] == 'Scissors':
            return redirect('/armadillo_competition/you_lose')
        else:
            session['points'] += 250
            return redirect('/armadillo_competition/speed_counter/rules')

    if session['you_rps'] =='Scissors':
        if session['com_rps'] == 'Rock':
            return redirect('/armadillo_competition/you_lose')
        else:
            session['points'] += 250
            return redirect('/armadillo_competition/speed_counter/rules')
@app.route("/unaviable") #When a place isn't complete yet 
def wait():
    session.clear()
    return render_template('wait.html')