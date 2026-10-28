## README for assignment Resourceful:

* Resource name: animal 
* Attributes:

```
  id                Unique identifier 
  name              The animal's name 
  species           Species, like dog/cat/rabbit/... 
  breed             Breed 
  gender            Gender 
  age               Age in years  (float; if age < 1year, it will be a float) 
  description       A short description 
  status            Availability, such as Available or Adopted 
  image             Path to the animal's photo 
```

## Database

```sql
CREATE TABLE IF NOT EXISTS animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL,
    description TEXT,                      
    status TEXT NOT NULL,
    image TEXT NOT NULL
);
```

* everything other than description is required to have

## REST

```
* Name:               Method                  Path for all:           in server.py:
  List                GET                     /animals                do_GET
  Retrieve            GET                     ..                      do_GET
  Create              POST                    ..                      do_POST
  Replace             PUT                     ..                      do_PUT
  Delete              DELETE                  ..                      do_DELETE

```

## Description

* path: /animals

  path +  GET: list all animals  
  path +  POST: Add a new animal
* If a animal's id = 3:  

  path/3  + GET: list the animal whos id = 3  
  + PUT: edit the animal whos id = 3  
  + DLETE: delete the animal whos id = 3

--------------------------------------------------------------------------------------------------------------------------------------------
well i need to admit that in server.py i let AI wrote the def save_uploaded_files(content_type, raw). 

### List：GET /animals

`do_GET` sees the path is /animals, it then call `db.list_all()` , change each line into JSON then send back with status code 200.   
The 3 preview animal in index.html and the all animal cards listed in animals.html use this.


Retrieve 1 animal with its id：GET /animals/<id>
if i want to extract animal id=3: GET /animals/3

path will atach the id number -> /animals/3.The server uses db.get(3) to get the row. If find, response in JSON of this animal with status code 200. if not found in database, reply with {"error": "Not found"}，and status code 404。

### Create：POST /animals

In animals.html, there is a form for Edit and Add a animal to database. 
this form starts empty, when editingId === null, Submit adds a new animal (POST). 
                        when editingId !== null, Submit is editing that animal (PUT).

the request body is a animal in JSON: name、species、breed、gender、age、description、status、image, server call db.create function to add that animal, then response with taht information with status code 201, means successful create taht animal.

### Edit Replace：PUT /animals/id

in `animal.html` page, each animal card has edit/delete button, click the edit button for taht animal, all its value will appear in the form. `editingId` is taht animal's id. 
change the filed as wish then click submit, the path becoms /animals/ followed by that id. 
request body for edit still are every field. server replaces the whole existing row with these new values by calling db.replace(...). if succeeds, it will return the updated animal with status code 200; or if the id not exsit, it will return the code 404. (but this shouldn't happen)

### Delete：DELETE /animals/id

still in`animal.html` page, on each animal card, if wish to delete a animal, click delete.
then it will call comfirm(), ask "Delete + NAME?" first. After user comfirm, send delete request, with empty request body. The server calls db.delete(...)。if successful deleted, replay with 200, otherwise, if id not exsit, or path not right, returns code 404.