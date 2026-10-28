import sqlite3
import csv


class AnimalDatabase:
    def __init__(self, db="data/animals.db"):
        self.db = db

    def connect(self):
        con = sqlite3.connect(self.db)
        return con

    def create_table(self):
        con = self.connect()
        con.execute("""
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
            )
        """)
        columns = [row[1] for row in con.execute("PRAGMA table_info(animals)")]             # PRAGMA schema.table_info(table-name);
        if "image" not in columns:
            con.execute("ALTER TABLE animals ADD COLUMN image TEXT")
        con.commit()
        con.close()

    def list_all(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM animals") 
        list = cur.fetchall()
        con.close()
        return list

    def get(self, animal_id):
        con = self.connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM animals WHERE id = ?", (animal_id,)) 
        row = cur.fetchone()
        con.close() 
        return row

    def create(self, animal):
        con = self.connect()
        cur = con.cursor()
        cur.execute("INSERT INTO animals (name, species, breed, gender, age, description, status, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", animal)
        con.commit()
        rowId = cur.lastrowid
        con.close()
        return rowId

    def replace(self, animal_id, animal):
        con = self.connect()
        cur = con.cursor()
        cur.execute(
            "UPDATE animals SET name = ?, species = ?, breed = ?, gender = ?, age = ?, description = ?, status = ?, image = ? WHERE id = ?",
            (*animal, animal_id)
        )
        con.commit()
        rowCount = cur.rowcount
        con.close()
        return rowCount

    def delete(self, animal_id):
        con = self.connect()
        cur = con.cursor()
        cur.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
        rowId = cur.rowcount
        con.commit()
        con.close()
        return rowId

    def delete_all(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute("DELETE FROM animals")
        cur.execute("DELETE FROM sqlite_sequence WHERE name = 'animals'")
        con.commit()
        con.close()
        

if __name__ == "__main__":
    db = AnimalDatabase()
    db.create_table()

    con = db.connect()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM animals")
    count = cur.fetchone()[0]
    if count == 0:
        with open("animal-list.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            data = []
            for name, species, breed, gender, age, description, status, image in reader:
                data.append(
                    (None, 
                    name, 
                    species, 
                    breed, 
                    gender, 
                    float(age), 
                    description or None, 
                    status,
                    image or None)
                )
        
            cur.executemany("INSERT INTO animals VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    
    con.commit()
    con.close()
    # db.get(1)
    # db.create(("Smokey", "Dog", "Border Collie", "Male", 2, "cutest forevery", "Available"))
    # db.delete(1)
    # db.replace(10, ("Rockey", "Dog", "Border Collie", "Male", 2, "Funny dog", "Available", "images/dog-Rockey"))
    for animal in db.list_all():
        print(animal)

    