import json
import os
from db import db
from db import Library
from db import Favorite
from flask import Flask
from flask import request
import datetime as dt
import googlemaps
import base64

key = os.environ["API_KEY"]

"""
Calling google maps api to turn the address of each of the selected
Cornell Libraries to Static Google Map Images.
"""
map_client = googlemaps.Client(key)
library_address = ["161 Ho Plaza, Ithaca, NY 14853",  # Olin Library
                   "160 Ho Plaza, Ithaca, NY 14853",  # Uris Library
                   "237 Mann Dr, Ithaca, NY 14853",  # Mann Library
                   "521 Ives Hall, Ithaca, NY 14853",  # Catherwood Library
                   "947 University Ave, Ithaca, NY 14853",  # Mui Ho Fine Arts Library
                   "G80 Statler Hall, Ithaca, NY 14853",  # Nestle Library
                   "420 Mallott Hall, Ithaca, NY 14853",  # Math Library
                   "101 Lincoln Hall, Ithaca, NY 14853",  # Sydney Cox Library
                   "Cornell Law School, Myron Taylor Hall, Law Library, Ithaca, NY 14853"]  # Law Library


all_libraries = {
    "libraries": [
        {"name": "Olin Library", "description": "It took seven years of planning and $5.7 million to build Olin Library, the first library specifically designed as a research facility. In the words of Anne R. Kenney, Carl A. Kroch University Librarian: “Today Olin remains a vital place for research and study, with between 3,000 and 11,000 visitors a day at peak academic times. The mind boggles at what the next 50 years will bring, but I’m betting Olin Library will still be a place that draws those who value the life of the mind.”",
            "open_hour": 8, "close_hour": 24, "map_image": ""},
        {"name": "Uris Library", "description": "Uris Library opened in 1891 as Cornell’s first library building. Designed by William Henry Miller, Cornell’s first student of architecture, in the Richardsonian Romansque style, the library garnered national acclaim for its combination of beauty and utility. The University Library, as it was known, was refurbished in 1962 with funds from Harold ’26 and Percy Uris, and was renamed in recognition of their generous contribution. Uris also contains the A.D. White Library. , a library within a library designed by Cornell’s first president, Andrew Dickson White, to hold his personal collection after he donated it to the university. It currently holds books on the history of the book and publishing. In an underground addition is the “Cocktail Lounge,” a unique 24-hour study area where contemporary design meets the Richardsonian Romanesque style. ",
            "open_hour": 8, "close_hour": 23, "map_image": ""},
        {"name": "Mann Library", "description": "Albert R. Mann Library is an open, trusted and welcoming home for research and discovery in the life sciences, agriculture, applied social sciences and human ecology. As a New York State land-grant library, we actively support the needs of all who seek knowledge and foster the open exchange of diverse ideas to improve the lives of people everywhere. Recognizing that the information landscape is ever changing, we preserve knowledge and strive to be innovative in our approach to its dissemination and in service to our patrons, particularly our partners in the College of Agriculture and Life Sciences and College of Human Ecology.",
            "open_hour": 8, "close_hour": 22, "map_image": ""},
        {"name": "Catherwood Library", "description": "The Martin P. Catherwood Library in Cornell University’s ILR School is the most comprehensive resource on labor and employment in North America. The ILR School was established by an act of the New York State Legislature in 1944. The Temporary Board of Trustees mandated “the provision of information” as one of three core services, declaring that “it will be essential to develop at the earliest possible moment a comprehensive library.” Today, the Catherwood Library is a service-oriented organization, offering expert research support through reference services, instruction, online guides, and access to premier collections. The collection consists of 250,000 volumes and 1500 serial subscriptions along with essential academic and practitioner databases and special format materials such as media and microforms. ILR collection strengths are in the areas of labor and employment, including collective bargaining, human resource studies, international and comparative industrial relations, labor disputes and history, labor economics, organizational behavior, and trade union issues. While many of these resources are academic in origin, Catherwood also collects directly from unions, corporations, governments, and non-profit organizations.", "open_hour": 8, "close_hour": 20, "map_image": ""},
        {"name": "Mui Ho Fine Arts Library", "description": "One of the largest academic art and architecture libraries in the Northeast, the Mui Ho Fine Arts Library offers an ever-expanding collection of materials on architecture, art, city and regional planning, landscape architecture, and photography in various formats and in multiple languages. Housed in the library and at the Annex, our collection grows by approximately 4,000 titles each year and comprises more than 267,000 volumes and subscriptions to more than 850 periodical titles. In print and online, we provide discipline-focused resources to search for publications, including the Avery Index to Architectural Periodicals, Urban Studies Abstracts, and Art & Architecture Source. We license various image collections from Artstor, and provide access to thousands of Cornell’s digital images.",
            "open_hour": 9, "close_hour": 22, "map_image": ""},
        {"name": "Nestlé Library", "description": "The Nestlé Library provides valuable research support to students, faculty, and all other members of the School of Hotel Administration (SHA) community. With specialized knowledge of all aspects of the hospitality and real estate industry, library staff are dedicated to serving the educational interests of the students, and the research and teaching interests of the school’s faculty. Organized shortly after the founding of the program in hospitality management at Cornell University in 1922, the library is an integral part of the school. The library contributes to the creation and dissemination of knowledge in the hospitality industry by connecting faculty members, students, and industry executives with hospitality industry information resources.",
         "open_hour": 8, "close_hour": 23.5, "map_image": ""},
        {"name": "Math Library", "description": "The Math Library supports research and instruction in mathematics and statistics for the Cornell community. The collection consists of works on mathematics, statistics, applied mathematics, mathematics education and the history of mathematics. It also has materials for instructional and career needs as well as popular, expository and recreational literature of a mathematical nature.",
            "open_hour": 9, "close_hour": 20, "map_image": ""},
        {"name": "Sydney Cox Library",
            "description": "Located on the second and third floors of Lincoln Hall, the Sidney Cox Library of Music and Dance provides listening and viewing facilities, workstations, laptops, and wireless Internet access, as well as a variety of study spaces. As the music collections grew, space in Lincoln Hall became more crowded.  The stacks were closed, with materials paged by student assistants, and user seating was limited.  After a long fund-raising campaign, Lincoln Hall was renovated and expanded, reopening in Fall 2000.  The renovation increased Music Library space by some 70%, providing ample and much-needed study space, and allowing most of the collection to be housed in open stacks.  In honor of a major contribution to the renovation, the Music Library was named in honor of Sidney Cox (’47; MA’48; 1922-2005), a composer, collector, and long-time supporter of the Music Department.", "open_hour": 8, "close_hour": 20, "map_image": ""},
        {"name": "Law Library", "description": "Through creative services and strategic partnerships, Cornell University Law Library advances excellence in legal scholarship, research, and teaching.", "open_hour": 8,
            "close_hour": 20, "map_image": ""}
    ]
}

"""
Adding the static google maps image url to each library
"""
count = 0
for x in library_address:
    rep = map_client.geocode(x)

    lat = rep[0]["geometry"]["location"]["lat"]
    lng = rep[0]["geometry"]["location"]["lng"]

    image_address = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=17&size=400x400&markers=size:mid%7Ccolor:red%7C{lat},{lng}&key={key}"
    all_libraries["libraries"][count]["map_image"] = image_address
    count = count + 1

"""---------------------------------------------------------------"""

app = Flask(__name__)
db_filename = "libraries.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/api/library/", methods=["POST"])
def create_library():
    """
    Endpoint for creating a Library.
    """
    body = json.loads(request.data)
    name = body.get("name")
    description = body.get("description")
    open_hour = body.get("open_hour")
    close_hour = body.get("close_hour")
    map_image = body.get("map_image")
    if name is None or description is None or open_hour is None or close_hour is None or map_image is None:
        return failure_response("Bad library", 400)
    new_library = Library(name=name, description=description,
                          open_hour=open_hour, close_hour=close_hour, map_image=map_image)
    db.session.add(new_library)
    db.session.commit()
    return success_response(new_library.serialize(), 201)


@app.route("/api/library/populate/")
def populate_libraries():
    """
    Endpoint for populating the Libraries table with the libraries included in
    the JSON above called [all_libraries].
    """
    libraries = all_libraries.get("libraries")
    for x in libraries:
        new_library = Library(name=x.get("name"), description=x.get("description"),
                              open_hour=x.get("open_hour"), close_hour=x.get("close_hour"), map_image=x.get("map_image"))
        db.session.add(new_library)
    db.session.commit()
    library = [library.serialize() for library in Library.query.all()]
    return success_response({"library": library})


@app.route("/api/library/")
def get_libraries():
    """
    Endpoint for getting all libraries.
    """
    library = [library.serialize() for library in Library.query.all()]
    return success_response({"library": library})


@app.route("/api/library/<int:library_id>/")
def get_library(library_id):
    """
    Endpoint for getting a specific library by its id.
    """
    library = Library.query.filter_by(id=library_id).first()
    if library is None:
        return failure_response("Library not found!")
    return success_response(library.serialize())


@app.route("/api/library/<int:library_id>/maps/")
def get_map(library_id):
    """
    Endpoint for getting a google static map corresponding to a library 
    by the library's id.
    """
    library = Library.query.filter_by(id=library_id).first()
    if library is None:
        return failure_response("Library not found!")
    base64_bytes = base64.b64encode(bytes(library.map_image, 'ascii'))
    base64_string = base64_bytes.decode("ascii")
    map = {"url": base64_string}
    return success_response(base64_string)


@app.route("/api/library/<int:library_id>/hours/")
def hours(library_id):
    """
    Endpoint for getting a library's hours by the library's id.
    """
    library = Library.query.filter_by(id=library_id).first()
    if library is None:
        return failure_response("Library not found!")
    open = library.open_hours
    close = library.close_hours
    if int(open) >= 12:
        open_12 = str(int(open) - 12) + " PM"
    else:
        open_12 = open + " AM"
    if int(close) >= 12:
        close_12 = str(int(close) - 12) + " PM"
    else:
        close_12 = close + " AM"
    final_hours = {"hours": f"{open_12} - {close_12}"}
    return success_response(final_hours)


@app.route("/api/library/<int:library_id>/time/")
def is_open(library_id):
    """
    Endpoint that checks if a given library (selected by its library id) 
    is open or closed at the current hour of checking.
    """
    library = Library.query.filter_by(id=library_id).first()
    if library is None:
        return failure_response("Library not found!")
    open = library.open_hours
    close = library.close_hours

    current_datetime = dt.datetime.now()
    string_date = current_datetime.strftime("%I%P")
    if string_date[-1] == "P":
        cur_time = int(string_date[:-1]) + 12
    else:
        cur_time = int(string_date[:-1])
    if (open <= cur_time) and (close > cur_time):
        return True
    return False


@app.route("/api/library/favorites/")
def get_favorites():
    """
    Endpoint that returns all the libraries that were selected as 
    favorites by the user.
    """
    favorites = [favorite.serialize() for favorite in Favorite.query.all()]
    return success_response({"favorites": favorites})


@app.route("/api/library/favorites/", methods=["POST"])
def add_favorite():
    """
    Endpoint that adds a library to the Favorite table.
    """
    body = json.loads(request.data)
    library_id = body.get("library_id")
    if library_id is None:
        return failure_response("Bad favorite", 400)
    new_favorite = Favorite(library_id=library_id)
    db.session.add(library_id)
    db.session.commit()
    return success_response(new_favorite.serialize(), 201)


@app.route("/api/library/favorite/", methods=["DELETE"])
def delete_favorite():
    """
    Endpoint that deletes a library from the Favorite table.
    """
    body = json.loads(request.data)
    library_id = body.get("library_id")
    if library_id is None:
        return failure_response("Course not found!")
    favorite = Favorite.query.filter_by(library_id=library_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return success_response(favorite.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
