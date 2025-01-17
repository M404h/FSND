#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from forms import *
from flask_migrate import Migrate
from sqlalchemy.orm import relationship, backref

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# connecte to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres=db.Column(db.String())
    web_link = db.Column(db.String(120))
    looking_for_talent=db.Column(db.Boolean(), default=False)
    seeking_description=db.Column(db.String())

    shows = db.relationship("Show", backref="Venue",lazy=True)

    #implemented any missing fields, as a database migration using Flask-Migrate


      
class Artist(db.Model):
    __tablename__ = "Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    web_link = db.Column(db.String(120))
    looking_for_venues=db.Column(db.Boolean(), default=False)
    seeking_description=db.Column(db.String())
    shows = db.relationship("Show", backref="Artist",lazy=True)

    #implement any missing fields, as a database migration using Flask-Migrate



class Show(db.Model):
  __tablename__ = "Show"

  id = db.Column(db.Integer, primary_key=True)
  artist_id=db.Column(db.Integer , db.ForeignKey("Artist.id"))
  venue_id=db.Column(db.Integer, db.ForeignKey("Venue.id"))
  start_time=db.Column(db.DateTime)

#Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

  artistFK = db.relationship("Artist", backref="Artist_fk",lazy=True)
  venueFK = db.relationship("Venue", backref="Venue_fk",lazy=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  data=[]
  city_query = db.session.query(Venue.city, Venue.state).distinct().all()

  for c in city_query:
    venue_array = []
    venue_data = Venue.query.filter_by(state=c.state).filter_by(city=c.city).all()

    for v in venue_data:
      new_shows_num = Show.query.filter_by(venue_id=v.id).filter_by(Show.start_time >= datetime.now()).count()
      
      venue_array.append({
      "id":v.id, 
      "name": v.name, 
      "num_upcoming_shows": new_shows_num
      })

      for d in venue_array:
        data.append({
          "city":d.city, 
          "state":d.state, 
          "venues":venue_array, 
          "num_upcoming_shows":new_shows_num
          })


    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues(): # not working 
  # TODO implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venue_array =[]
  get_data = request.form.get('search_term')
  venue_data = Venue.query.filter(Venue.name.match("'%${get_data}%'")).all()
  venue_num=len(venue_data)

  for v in venue_data:
      venue_object= {
        "id": v.id,
        "name": v.name,
        "num_upcoming_show": 0
      }
      venue_array.append(venue_object)


  response={
    "count":venue_num,
    "data": venue_array
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id

  data =[]
  venue_query = Venue.query.filter_by(Venue.id == venue_id).all()

  data.append({
    
  })

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  data=[]
  artist_query = db.session.query(Artist.name).all()
  for a in artist_query:
      artist_object={
        "id": a.id,
        "name": a.name
      }
      
      data.append(artist_object)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # replace with real artist data from the artist table, using artist_id
  artist_query = Artist.query.filter_by(Artist.id == artist_id).all()

  data=[]

  data.append({
    "id": artist_query.id,
    "name": artist_query.name,
    "city": artist_query.city,
    "state": artist_query.state,
    "phone": artist_query.phone,
    "genres": artist_query.genres,
    "image_link":artist_query.image_link,
    "facebook_link": artist_query.facebook_link,
    "web_link": artist_query.web_link,
    "looking_for_venues":artist_query.looking_for_venues,
    "seeking_description":artist_query.seeking_description,
  })
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_query = Artist.query.filter_by(Artist.id == artist_id).all()
  artist={
    "id": artist_query.id,
    "name": artist_query.name,
    "city": artist_query.city,
    "state": artist_query.state,
    "phone": artist_query.phone,
    "genres": artist_query.genres,
    "image_link":artist_query.image_link,
    "facebook_link": artist_query.facebook_link,
    "web_link": artist_query.web_link,
    "looking_for_venues":artist_query.looking_for_venues,
    "seeking_description":artist_query.seeking_description,
  }
  
  # populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #num_shows should be aggregated based on number of upcoming shows per venue.
  data=[] 
  show_query=Show.query.all() 
  for s in show_query:
    data.append({
      "venue_id"s.Venue.id:,
      "venue_name":
      "artist_id":
      "artist_name":
      "artist_image_link":
      "start_time":
    })
   
   
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
