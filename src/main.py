from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from decouple import config


app = FastAPI()

# Allow port for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


redis = get_redis_connection(
    host=config('REDIS_HOST'),
    port=config('REDIS_PORT'),
    password=config('REDIS_PASSWORD'),
    decode_responses=config('REDIS_DECODE_RESPONSES')
)


# Model
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


# Endpoints
@app.get('/')
async def root():
    return {"message": "Hello!"}


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
