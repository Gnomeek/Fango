# Fango
An easy-to-use Python HTTP framework based on Flask blueprint with some Django features, e.g., DRF, middleware, DAO

## Where Fango comes from
`Fango` is the combination of `Flask` and `Django` since `Fango` is based on `Flask Blueprint` while it still has `Django` features like:
1. DRF
2. middleware
3. ORM

## How to use Fango
Consider `Fango` as a boilerplate, two demos are attached in this repo, i.e., apps/pingpong and apps/store

### apps/pingpong
This app implements simple function that when a request is received, server responds with a simple "pong"
```
➜ curl http://127.0.0.1:5000/api/pingpong/ping
```

### apps/store
This app implements `GET` and `POST` method to allow request to put item into DB and search item with item ID

```
➜ curl -sSX POST -H "Content-Type: application/json" -d '{"name": "fluent python", "price": 30.99, "volume": 5}' http://127.0.0.1:5000/api/store/items
➜ curl http://127.0.0.1:5000/api/store/items\?_id\=1
```


### Detailed Instruction
#### 1. Construct folders
#### 2. Implement your views
#### 3. Write your DB model under dal if necessary
#### 4. Register your views in `__init__.py` under specify app folder
#### 5. Register your app in `server.py`

#### Explanation
#### 1. Construct folders
in `apps` folder, `store` folder and following folder are constructed as below:
```
➜ tree apps/store
apps/store
├── __init__.py
├── dal
│   ├── __init__.py
│   └── store_model.py
└── views
    ├── __init__.py
    └── store.py

5 directories, 5 files

```
#### 2. Implement your views
View class should include following attributes:
1. `__methods__ = ["GET", "POST"]` to include all implemented RESTFul methods
2. `OBJ_MODEL = StoreStorage` to mark corresponding ORM model of view
3. implement your `post` method
4. implement your `get_queryset` method, `get` method is implicitly implemented in `libs.viewset.ModelViewSet`

#### 3. Write your DB model under dal if necessary
just like `SQLAlchemy`, a CommonFieldsMixin is provided(including autoincrement ID and create time) under `utils.db.orm_model_base.CommonFieldsMixin`
simple `create`, `filter` method is provided in `utils.db.model.Model`
#### 4. Register your views in `__init__.py` under specify app folder
```python
from flask import Blueprint

from apps.store.views.store import StoreView
from libs.router import register_api
bp = Blueprint("store", __name__)

register_api(app=bp, view=StoreView, endpoint="store", url="/items")
```
#### 5. Register your app in `server.py`
```python
import flask

from apps.store import bp as store_app

server = flask.Flask(__name__)
server.register_blueprint(store_app, url_prefix="/api/store")
```

#### 6. Finale
Thus, your store app is bound with uri `api/store`, your view of store app is bound to uri `api/store/items` test your view with following curl:
```
curl -sSX POST -H "Content-Type: application/json" -d '{"name": "fluent python", "price": 30.99, "volume": 5}' http://127.0.0.1:5000/api/store/items
curl http://127.0.0.1:5000/api/store/items\?_id\=1
```
