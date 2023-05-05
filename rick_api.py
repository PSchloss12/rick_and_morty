from flask import Flask, request, render_template, flash
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
from db_manager import db_session
from rick_classes import Character, Location, LOCATION_URL
from random import randint
from sqlalchemy import select
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = 'meow'
Bootstrap(app)
Markdown(app)

# collect info from db
characters = db_session.query(Character).all()
locations = db_session.query(Location).all()

@app.route('/') # return index for home page
def home():
    return render_template('index.html')

@app.route('/characters/', methods = ['POST','GET'])
def gallery():
    # post request comes from character search
    if request.method == 'POST':
        name = request.form['name']
        matches=[]
        for c in characters: # search for char
            if re.search(name,c.name, re.IGNORECASE):
                matches.append(c)
        if len(matches)>0: # divide up responce into three cols
            div = int(len(matches)/3)
            r = len(matches)%3
            if r==0:
                first_col = matches[0:div]
                second_col = matches[div:2*div]
                third_col = matches[2*div:]
            elif r==1:
                first_col = matches[0:div+1]
                second_col = matches[div+1:2*div+1]
                third_col = matches[2*div+1:]
            else:
                first_col = matches[0:div+1]
                second_col = matches[div+1:2*div+2]
                third_col = matches[2*div+2:]
        else: # return none with banner
            flash(f'No search results found for {name}!', 'alert-info')
            first_col=[]
            second_col=[]
            third_col=[]
    else: # randomize 9 characters, all cols from same episode
        first = randint(0, len(characters)+1)
        second = randint(0, len(characters)+1)
        third = randint(0, len(characters)+1)
        num = 3
        first_col=characters[first:first+num]
        second_col=characters[second:second+num]
        third_col=characters[third:third+num]
    # return template
    return render_template('gallery.html', first_col=first_col, 
                           second_col=second_col,
                           third_col=third_col)

@app.route('/characters/<int:char_id>/')
def character(char_id: int):
    # find character to display from db
    char = db_session.execute(select(Character).filter_by(id=char_id)).first()[0]
    char.scrape(eps=True, locs=True) # include episode and location info
    return render_template('character.html', char=char)

@app.route('/locations/')
def location_list():
    # display lists of all locations broken into four columns
    div = int(len(locations)/4)
    first_col = locations[:div]
    second_col = locations[div:2*div]
    third_col = locations[2*div:3*div]
    fourth_col = locations[3*div:]
    return render_template('loc_list.html', first_col=first_col, 
                           second_col=second_col, third_col=third_col,
                           fourth_col=fourth_col)

@app.route('/locations/<int:loc_id>/')
def location(loc_id: int):
    # display specific location info
    loc = Location(LOCATION_URL+f'/{loc_id}')
    loc.scrape() # call api
    chars = [int(url.split('/')[-1]) for url in loc.characters]
    loc.characters=[]
    for i in chars: # fetch characters at location from db
        try:
            loc.characters.append(db_session.execute(select(Character).filter_by(id=i)).first()[0])
        except TypeError as ex: #catch NoneType
            continue
    
    div = int(len(loc.characters)/3)
    r = len(loc.characters)%3
    if r==0: # separate chars into cols
        first_col = loc.characters[0:div]
        second_col = loc.characters[div:2*div]
        third_col = loc.characters[2*div:]
    elif r==1:
        first_col = loc.characters[0:div+1]
        second_col = loc.characters[div+1:2*div+1]
        third_col = loc.characters[2*div+1:]
    else:
        first_col = loc.characters[0:div+1]
        second_col = loc.characters[div+1:2*div+2]
        third_col = loc.characters[2*div+2:]
    # return template
    return render_template('location.html', location=loc, first_col=first_col, 
                           second_col=second_col, third_col=third_col)

@app.route('/locations/None/')
def null_location():
    return render_template('null.html') # if user attempts to go to non existent loc

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='12322')