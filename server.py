from http.server import BaseHTTPRequestHandler, HTTPServer
from email.parser import BytesParser
from email.policy import default
import json
import os
import re
from database import AnimalDatabase

db = AnimalDatabase()

COLUMNS = ("id", "name", "species", "breed", "gender", "age", "description", "status", "image")

def row_to_obj(row):
    return dict(zip(COLUMNS, row))

def save_uploaded_files(content_type, raw):
    header = ("Content-Type: " + content_type + "\r\n\r\n").encode()
    message = BytesParser(policy=default).parsebytes(header + raw)
    folder = os.path.join(os.path.dirname(__file__), "images")
    os.makedirs(folder, exist_ok=True)
    saved = []
    for part in message.iter_parts():
        filename = part.get_filename()
        if not filename:
            continue
        filename = os.path.basename(filename)
        filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
        if not filename:
            continue
        stem, ext = os.path.splitext(filename)
        path = os.path.join(folder, filename)
        number = 1
        while os.path.exists(path):
            filename = stem + "-" + str(number) + ext
            path = os.path.join(folder, filename)
            number += 1
        payload = part.get_payload(decode=True)
        if not payload:
            continue
        with open(path, "wb") as image_file:
            image_file.write(payload)
        saved.append("images/" + filename)
    return saved

class Request_Handler(BaseHTTPRequestHandler):
    def do_GET(self):                                               # list/retrive
        parse = self.path.split("/")

        if parse == ["", "animals"]:
            animals = []
            for row in db.list_all():
                animals.append(row_to_obj(row))
            body = json.dumps(animals).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        if len(parse) == 3 and parse[1] == "animals":
            animal_id = int(parse[2])
            row = db.get(animal_id)
            if row is None:
                body = json.dumps({"error": "Not found"}).encode()
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

            body = json.dumps(row_to_obj(row)).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        body = json.dumps({"error": "Not found"}).encode()
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
        
    def do_POST(self):                                                     # Create
        if self.path == "/upload":
            length = int(self.headers["Content-Length"])
            raw = self.rfile.read(length)
            saved = save_uploaded_files(self.headers.get("Content-Type", ""), raw)
            body = json.dumps({"saved": saved}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path != "/animals":
            body = json.dumps({"Error 404: not fund"}).encode()
            self.send_response(404)
            self.send_header("Content-Type", "application/json")                                       
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return
        
        length = int(self.headers["Content-Length"])
        raw = self.rfile.read(length)
        data = json.loads(raw)
        animal = (
            data["name"],
            data["species"],
            data["breed"],
            data["gender"],
            float(data["age"]),
            data["description"],
            data["status"],
            data["image"],
        )

        new_id = db.create(animal)
        row = db.get(new_id)

        body = json.dumps(row_to_obj(row)).encode()
        self.send_response(201)
        self.send_header("Content-Type", "application/json")                                     
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_PUT(self):                                                      # Replace
        parse = self.path.split("/")                                       # after parsing: [ "", "animals",3(id)]
        if len(parse) != 3 or parse[1] != "animals":
            body = json.dumps({"Error 404: not fund"}).encode()
            self.send_response(404)
            self.send_header("Content-Type", "application/json")                                       
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        animal_id = int(parse[2])

        length = int(self.headers["Content-Length"])
        raw = self.rfile.read(length)
        data = json.loads(raw)
        animal = (
            data["name"],
            data["species"],
            data["breed"],
            data["gender"],
            float(data["age"]),
            data["description"],
            data["status"],
            data["image"],
        )

        changed = db.replace(animal_id, animal)
        if changed == 0: 
            body = json.dumps({"error": "Not found"}).encode()
            self.send_response(404)
            self.send_header("Content-Type", "application/json")                                     
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return 

        row = db.get(animal_id)
        body = json.dumps(row_to_obj(row)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_DELETE(self):
        parse = self.path.split("/")                                       # after parsing: [ "", "animals",3(id)]
        if len(parse) != 3 or parse[1] != "animals":
            body = json.dumps({"Error 404: not fund"}).encode()
            self.send_response(404)
            self.send_header("Content-Type", "application/json")                                       
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        animal_id = int(parse[2])        
        changed = db.delete(animal_id)

        if changed == 0: 
            body = json.dumps({"error": "Not found"}).encode()
            self.send_response(404)
            self.send_header("Content-Type", "application/json")                                     
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return 

        body = json.dumps({"deleted": animal_id}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    HTTPServer(("", 8000), Request_Handler).serve_forever()
    