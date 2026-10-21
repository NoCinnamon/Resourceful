# Resourceful

sqlite3 is how your Python program reaches data/animals.db, and SQL is the language it uses to read or change the rows.

That file is the saved list of animals. The table says which fields each animal has. An INSERT adds one, a SELECT reads them, an UPDATE changes one, and a DELETE removes one. When the program stops, the rows stay in the file.

The website needs this so the animal list is still there after a refresh. The page will ask the server for those rows, and the server will use sqlite3 and SQL to get them from animals.db.