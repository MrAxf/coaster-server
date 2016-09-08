import json, string
from flask import Flask, request, Response
from mongoalchemy.session import Session
from mongoalchemy.document import Document
from mongoalchemy.fields import *
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.config["mongoDB-name"] = "Coaster-DB"
db = Session.connect(app.config["mongoDB-name"])

class User(Document):
    name = StringField()
    password = StringField()
    likes = ListField(StringField(), default_empty=True)
    favs = ListField(StringField(), default_empty=True)

    def json(self):
        if len(self.likes) != 0:
            likesList = '["'+'", "'.join(self.likes)+'"]'
        else:
            likesList = "[]"

        if len(self.favs) != 0:
            favsList = '["'+'", "'.join(self.favs)+'"]'
        else:
            favsList = "[]"
        return json.loads('{"mongo_id": "'+str(self.mongo_id)+'", "name": "'+self.name+'", "likes": '+likesList+', "favs": '+favsList+'}')


class Comment(Document):
    userId = StringField()
    comment = StringField()

class Coaster(Document):
    nombre = StringField()
    tipo = StringField()
    velocidad = FloatField()
    altura = IntField(default=0)
    loops = IntField()
    drops = IntField()
    glateral = FloatField()
    maxgvertical = FloatField()
    mingvertical = FloatField()
    addedBy = StringField()
    intensidad = StringField()
    comentarios = ListField(DocumentField(Comment), default_empty=True)
    likes = IntField(default=0)

    def json(self):
        comentariosList = []
        for comentario in self.comentarios:
            comentariosList.append('{"userId": "'+comentario.userId+'", "comment": "'+comentario.comment+'"}')

        return json.loads('{"mongo_id": "'+str(self.mongo_id)+'", "altura": "'+str(self.altura)+'", "nombre": "'+self.nombre+'", "tipo": "'+self.tipo+'", "velocidad": "'+str(self.velocidad)+'", "loops": "'+str(self.loops)+'", "drops": "'+str(self.drops)+'", "glateral": "'+str(self.glateral)+'", "maxgvertical": "'+str(self.maxgvertical)+'", "mingvertical": "'+str(self.mingvertical)+'", "addedBy": "'+str(self.addedBy)+'", "intensidad": "'+str(self.intensidad)+'", "comentarios": ['+ ','.join(comentariosList) +'], "likes": '+str(self.likes)+'}')

@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    if not data["name"] or not data["password"]:
        return buildResponse(json.dumps({"err": 1}))
    user = db.query(User).filter(User.name == data["name"]).first()
    if user:
        return buildResponse(json.dumps({"err": 2}))

    password = sha256_crypt.encrypt(data["password"])

    user = User(name = data["name"], password = password)
    db.save(user)
    return buildResponse(json.dumps({"err": 0}))

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    if not data["name"] or not data["password"]:
        return buildResponse(json.dumps({"err": 1}))
    user = db.query(User).filter(User.name == data["name"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 2}))
    if not sha256_crypt.verify(data["password"], user.password):
        return buildResponse(json.dumps({"err": 2}))

    return buildResponse(json.dumps({"err": 0, "user": user.json()}))

@app.route('/coasters', methods=['GET', 'POST'])
def getCoasters():
    data = request.get_json()
    if not data["userId"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    user = db.query(User).filter(User.mongo_id == data["userId"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 2}))


    if not data["nameFilter"]:
        nameReg = r'.*'
    else:
        nameReg = r''+ data["nameFilter"]

    if not data["typeFilter"]:
        typeReg = r'.*'
    else:
        typeReg = r''+data["typeFilter"]

    if not data["fav"]:
        coasters = db.query(Coaster).filter(Coaster.nombre.regex(nameReg, ignore_case=True), Coaster.tipo.regex(typeReg, ignore_case=True))
    else:
        coasters = db.query(Coaster).filter(Coaster.nombre.regex(nameReg, ignore_case=True), Coaster.tipo.regex(typeReg, ignore_case=True), Coaster.mongo_id.in_(*user.favs))

    coasterList = []

    for coaster in coasters:
        coasterList.append(coaster.json())

    return buildResponse(json.dumps({"err": 0, "coasters": coasterList}))

@app.route('/coasters/<coaster_id>', methods=['GET', 'POST'])
def getCoaster(coaster_id):
    data = request.get_json(coaster_id)
    if not data["userId"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    if not all(c in string.hexdigits for c in coaster_id):
        return buildResponse(json.dumps({"err": 3}))

    coaster = db.query(Coaster).filter(User.mongo_id == coaster_id).first()
    if not coaster:
        return buildResponse(json.dumps({"err": 4}))

    return buildResponse(json.dumps({"err": 0, "coaster": coaster.json()}))

@app.route('/coasters/<coaster_id>/delete', methods=['GET', 'POST'])
def deleteCoaster(coaster_id):
    data = request.get_json(coaster_id)
    if not data["userId"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    if not all(c in string.hexdigits for c in coaster_id):
        return buildResponse(json.dumps({"err": 3}))

    coaster = db.query(Coaster).filter(User.mongo_id == coaster_id).first()
    if not coaster:
        return buildResponse(json.dumps({"err": 4}))

    db.remove(coaster)

    return buildResponse(json.dumps({"err": 0}))

@app.route('/coasters/post', methods=['GET', 'POST'])
def addCoaster():
    data = request.get_json()
    if not data["nombre"] or not data["tipo"] or not data["velocidad"] or not data["loops"] or not data["drops"] or not data["glateral"] or not data["maxgvertical"] or not data["mingvertical"] or not data["userId"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    user = db.query(User).filter(User.mongo_id == data["userId"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 2}))
    coaster = Coaster(nombre = data["nombre"], tipo = data["tipo"], velocidad = data["velocidad"], loops = data["loops"], drops = data["drops"], glateral = data["glateral"], maxgvertical = data["maxgvertical"], mingvertical = data["mingvertical"], addedBy = data["userId"])
    intensidad = coaster.velocidad + coaster.drops*5 +coaster.loops*5 + coaster.glateral*10 + coaster.maxgvertical*10 + coaster.mingvertical*10
    if intensidad < 200:
        coaster.intensidad = "Familiar"
    elif intensidad < 400:
        coaster.intensidad = "Media"
    elif intensidad >= 400:
        coaster.intensidad = "Extrema"
    db.save(coaster)

    return buildResponse(json.dumps({"err": 0, "coaster": coaster.json()}))

@app.route('/coasters/<coaster_id>/update', methods=['GET', 'POST'])
def updateCoaster(coaster_id):
    data = request.get_json()
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 1}))
    user = db.query(User).filter(User.mongo_id == data["userId"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in coaster_id):
        return buildResponse(json.dumps({"err": 2}))

    coaster = db.query(Coaster).filter(User.mongo_id == coaster_id).first()

    if str(user.mongo_id) != coaster.addedBy:
        return buildResponse(json.dumps({"err": 3}))

    if data["nombre"]:
        coaster.nombre = data["nombre"]
    if data["tipo"]:
        coaster.tipo = data["tipo"]
    if data["altura"]:
        coaster.altura = data["altura"]
    if data["velocidad"]:
        coaster.velocidad = data["velocidad"]
    if data["drops"]:
        coaster.drops = data["drops"]
    if data["loops"]:
        coaster.loops = data["loops"]
    if data["glateral"]:
        coaster.glateral = data["glateral"]
    if data["maxgvertical"]:
        coaster.maxgvertical = data["maxgvertical"]
    if data["mingvertical"]:
        coaster.mingvertical = data["mingvertical"]


    intensidad = coaster.velocidad + coaster.drops*5 +coaster.loops*5 + coaster.glateral*10 + coaster.maxgvertical*10 + coaster.mingvertical*10
    if intensidad < 200:
        coaster.intensidad = "Familiar"
    elif intensidad < 400:
        coaster.intensidad = "Media"
    elif intensidad >= 400:
        coaster.intensidad = "Extrema"
    db.update(coaster)

    return buildResponse(json.dumps({"err": 0, "coaster": coaster.json()}))

@app.route('/coasters/<coaster_id>/comment', methods=['GET', 'POST'])
def commentCoaster(coaster_id):
    data = request.get_json(coaster_id)
    if not data["userId"] or not data["comment"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    user = db.query(User).filter(User.mongo_id == data["userId"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 2}))
    if not all(c in string.hexdigits for c in coaster_id):
        return buildResponse(json.dumps({"err": 3}))

    coaster = db.query(Coaster).filter(User.mongo_id == coaster_id).first()
    if not coaster:
        return buildResponse(json.dumps({"err": 4}))

    comment = Comment(userId=data["userId"], comment=data["comment"])

    coaster.comentarios.append(comment)
    db.update(coaster)

    return buildResponse(json.dumps({"err": 0}))

@app.route('/coasters/<coaster_id>/like', methods=['GET', 'POST'])
def likeCoaster(coaster_id):
    data = request.get_json(coaster_id)
    if not data["userId"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    user = db.query(User).filter(User.mongo_id == data["userId"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 2}))
    if not all(c in string.hexdigits for c in coaster_id):
        return buildResponse(json.dumps({"err": 3}))

    coaster = db.query(Coaster).filter(User.mongo_id == coaster_id).first()
    if not coaster:
        return buildResponse(json.dumps({"err": 4}))

    if coaster_id in user.likes:
        user.likes.remove(coaster_id)
        coaster.likes -= 1
    else:
        user.likes.append(coaster_id)
        coaster.likes += 1
    db.update(user)
    db.update(coaster)

    return buildResponse(json.dumps({"err": 0}))

@app.route('/coasters/<coaster_id>/fav', methods=['GET', 'POST'])
def favCoaster(coaster_id):
    data = request.get_json(coaster_id)
    if not data["userId"]:
        return buildResponse(json.dumps({"err": 1}))
    if not all(c in string.hexdigits for c in data["userId"]):
        return buildResponse(json.dumps({"err": 2}))
    user = db.query(User).filter(User.mongo_id == data["userId"]).first()
    if not user:
        return buildResponse(json.dumps({"err": 2}))
    if not all(c in string.hexdigits for c in coaster_id):
        return buildResponse(json.dumps({"err": 3}))

    coaster = db.query(Coaster).filter(User.mongo_id == coaster_id).first()
    if not coaster:
        return buildResponse(json.dumps({"err": 4}))

    if coaster_id in user.favs:
        user.favs.remove(coaster_id)
    else:
        user.favs.append(coaster_id)
    db.update(user)

    return buildResponse(json.dumps({"err": 0}))


@app.route('/clearUsers', methods=['GET', 'POST'])
def clearUsers():
    db.clear_collection(User)
    return buildResponse(json.dumps({"err": 0}))

@app.route('/clearCoasters', methods=['GET', 'POST'])
def clearCoasters():
    db.clear_collection(Coaster)
    return buildResponse(json.dumps({"err": 0}))

def buildResponse(data):
    resp = Response(data, mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    app.debug = True
    app.run()
