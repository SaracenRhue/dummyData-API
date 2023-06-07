from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from faker import Faker
from typing import List, Any
import random

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
fake = Faker()


@app.get('/movie/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1):
    data = []
    for _ in range(amount):
        item = {
        "id": fake.unique.random_number(digits=5),
        "title": fake.catch_phrase(),
        "year": fake.year(),
        "length": f"{random.randint(90, 150)} min",
        "rating": round(random.uniform(1, 10), 2),
        "description": fake.text(),
        "image": fake.image_url(),
    }
        data.append(item)
    return data

@app.get('/gene/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1 ):
    data = []
    for i in range(amount):
        gene = {}
        gene['name'] = f'Gene{i+1}'

        num_variants = random.randint(1, 5)
        variants = []
        for j in range(num_variants):
            variant = {}
            variant['name'] = f'Variant{j+1}'
            variant['txStart'] = random.randint(1, 1_000_000)
            variant['txEnd'] = variant['txStart'] + random.randint(1, 1_000_000)

            num_exons = random.randint(1, 10)
            variant['exonCount'] = num_exons
            variant['exonStarts'] = sorted(random.sample(range(variant['txStart'], variant['txEnd']), num_exons))
            variant['exonEnds'] = sorted(random.sample(range(variant['txStart'], variant['txEnd']), num_exons))

            variants.append(variant)

        gene['variants'] = variants
        data.append(gene)

    return data

@app.get('/userProfile/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1 ):
    data = []
    for _ in range(amount):
        item = {'username': fake.user_name(), 'name': fake.name(), 'email': fake.email(), 'password': fake.password(), 'dob': fake.date_of_birth(), 'bio': fake.text(), 'address': fake.address()}
        data.append(item)
    return data

@app.get('/order/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1):
    data = []
    for _ in range(amount):
        item = {'orderId': fake.uuid4(), 'product': fake.word(), 'quantity': fake.random_int(min=1, max=10), 'price': fake.pydecimal(left_digits=2, right_digits=2, positive=True), 'shippingAddress': fake.address(), 'status': fake.random_element(elements=('Pending', 'Shipped', 'Delivered', 'Returned'))}
        data.append(item)
    return data

@app.get('/socialMediaPost/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1):
    data = []
    for _ in range(amount):
        item = {'username': fake.user_name(), 'post': fake.text(), 'likes': fake.random_int(min=0, max=10000), 'comments': fake.random_int(min=0, max=5000), 'shares': fake.random_int(min=0, max=5000), 'timestamp': fake.date_time_this_year()}
        data.append(item)
    return data

@app.get('/image/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1):
    data = []
    for _ in range(amount):
        item = {'name': fake.name(), 'url': fake.image_url()}
        data.append(item)
    return data

@app.get('/productInfo/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1):
    data = []
    for _ in range(amount):
        item = {'name': fake.name(), 'price': fake.pydecimal(left_digits=2, right_digits=2, positive=True), 'color': fake.color_name(), 'size': fake.random_int(min=1, max=10)}
        data.append(item)
    return data

@app.get('/contactInfo/{amount}', response_model=List[Any])
def get_fake_data(amount: int = 1):
    data = []
    for _ in range(amount):
        item = {'name': fake.name(), 'email': fake.email(), 'phone': fake.phone_number(), 'address': fake.address(), 'job': fake.job(), 'company': fake.company(), 'ssn': fake.ssn()}
        data.append(item)
    return data

@app.get('/{provider}/{amount}', response_model=List[Any])
def get_fake_data(provider: str, amount: int = 1):
    faker_func = getattr(fake, provider, None)
    if faker_func is None:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not found")
    return [faker_func() for _ in range(amount)]

@app.get('/providers', response_model=List[str])
def get_providers():
    return [provider for provider in dir(fake) if provider[0].islower()]
