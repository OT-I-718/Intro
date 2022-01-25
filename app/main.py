import uvicorn
import logging
from fastapi import FastAPI
from pydantic import BaseModel, Field
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from app.config import DBConfig


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
# initialize app
app = FastAPI()

# get the database collection reference
# we could have .env/os file to keep the secret keys information for actual application
cred = credentials.Certificate(DBConfig.SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_ref = db.collection(DBConfig.INCREMENT_TABLE)


# Item model
class Item(BaseModel):
    name: str = Field(example='foo', regex='[a-z_]{3,15}')  # field regex
    value: int = Field(example=4, gt=0, lt=10)  # 0 < value < 10


@app.get('/')
def get_tag_stats():
    docs = collection_ref.stream()
    res = {}
    for doc in docs:
        res.update(doc.to_dict())
    return res


@app.put('/')
def increment_count(item: Item):
    docs = collection_ref.stream()
    value = item.value
    for doc in docs:
        if doc.id == item.name:
            value += doc.to_dict().get(item.name)
            break
    doc_ref = collection_ref.document(item.name)
    res = {item.name: value}
    doc_ref.set(res)
    logger.info('increment count for {0} has been updated to {1}'.format(item.name, value))
    return res

'''if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)'''