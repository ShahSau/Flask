from flask import Flask
from helper import pets

app = Flask('__name__')

### creating home route
@app.route('/')
def index():
  return '''
  <h1> Adopt a Pet!</h1>
  <p> Browse through the links below to find your new furry friend:</p>
  <ul>
    <li><a href='/animals/dogs'>Dogs</a></li>
    <li><a href='/animals/cats'>Cats</a></li>
    <li><a href='/animals/rabbits'>Rabbits</a></li>
  </ul>
  '''
### creating animal route
@app.route('/animals/<pet_type>')
def animals(pet_type):
  html = f'<h1>List of {pet_type}</h1>'
  html+='<ul>'
  name_pet =pets[pet_type]
  for item,p in enumerate(name_pet):
    html+= f'<li><a href=/animals/{pet_type}/{str(item)}>{p["name"]}</a></li>'
  html+='</ul>'
  print(html)
  return html


### creating a pet route
@app.route('/animals/<pet_type>/<int:pet_id>')
def pet(pet_type,pet_id):
  pet = pets[pet_type][pet_id]
  return f'''
  <h1> {pet["name"]}</h1>
  <img src={pet['url']} alt='alt text'>
  <p>{pet['description']}</p>
  <ul>
  <li>{pet['breed']}</li>
  <li>{pet['age']}</li>
  '''







