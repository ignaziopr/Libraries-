# Libraries+

Download Libraries+ to learn more about your favorite Cornell Libraries! Use it to find the library's location, rent a study room, find its hours, and more.
Link to the iOS github: https://github.com/gabegod14/culibraries-

<img width="200" alt="Screen Shot 2022-12-02 at 10 57 14 PM" src="https://user-images.githubusercontent.com/97565265/205421702-f250bc98-fa6d-47c2-8e1c-59b2a5ceb4f0.png">

<img width="200" alt="Screen Shot 2022-12-02 at 10 57 02 PM" src="https://user-images.githubusercontent.com/97565265/205421706-8e12777f-a066-4034-88b6-9e45c9f999c6.png">


Libraries+ consists of a login screen, a library selection screen, and a library information screen. The app is centered around
learning more about select libraries that Cornell University offers. Some of its features include providing library information, 
pictures, open and closing times, "starring" Libraries and adding them to a list of favorites, a Google Map Static image of its location, 
and the option to view availible study rooms and reserve them. 

The db.py file provided consists of two tables, Library and Favorite. Library
takes in a name, description, open hour, close hour, and a map image, while Favorite takes in a library id. If the star icon is clicked next
to a library's name in the library information screen, the library will be added to Favorite. If it is clicked a second time, the library
will be removed from Favorite.

The app.py file relies on the Google Maps Static API. Calling the geocode function after passing a list of library addresses returns a latitude
and longitude, which is later passed into a string that represents the google maps image pertaining to that address. This string is later added to a
JSON containing the rest of the parameters of the Library table, and through endpoints this JSON is used to populate the Library table.

The endpoints included are:
- /api/library/: Endpoint for getting all libraries.
- /api/library/ [POST]: Endpoint for creating a Library.
- /api/library/populate/: Endpoint for populating the Libraries table with the libraries included in the JSON above called [all_libraries].
-/api/library/<int:library_id>/: Endpoint for getting a specific library by its id.
-/api/library/<int:library_id>/maps/: Endpoint for getting a google static map corresponding to a library by the library's id.
-/api/library/<int:library_id>/hours/: Endpoint for getting a library's hours by the library's id.
-/api/library/<int:library_id>/time/: Endpoint that checks if a given library (selected by its library id) is open or closed at the current hour of checking.
-/api/library/favorites/: Endpoint that returns all the libraries that were selected as favorites by the user.
-/api/library/favorites/ [POST]: Endpoint that adds a library to the Favorite table.
-/api/library/favorites/ [DELETE]: Endpoint that deletes a library from the Favorite table.

-----------------------------------
Libraries+ addressess each of the Backend requirements by:
1. At least 4 routes (1 must be GET, 1 must be POST, 1 must be DELETE) -> See endpoints above.
2. At least 2 tables in database with a relationship between them -> Library and Favorite, Favorite having a one to one relationship with Library
and taking a library_id as one of its parameters.
3. API specification explaining each implemented route -> See endpoints above.
4. Implementation of images and/or authentication (only 1 required) -> Google Maps Static API Images.

Thank you for everything! I really enjoyed the Backend Course and hopefully you're in a good mood when grading this :)
