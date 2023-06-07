from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from faker import Faker
from typing import List, Any

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
fake = Faker()


#contactInfo
@app.get('/contactInfo/{amount}', response_model=List[Any])
def get_fake_data(amount: int):
    data = []
    for _ in range(amount):
        item = {'name': fake.name(), 'email': fake.email(), 'phone': fake.phone_number(), 'address': fake.address(), 'job': fake.job(), 'company': fake.company(), 'ssn': fake.ssn()}
        data.append(item)
    return data


@app.get('/{provider}/{amount}', response_model=List[Any])
def get_fake_data(provider: str, amount: int):
    faker_func = getattr(fake, provider, None)
    if faker_func is None:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not found")
    return [faker_func() for _ in range(amount)]

@app.get('/providers', response_model=List[str])
def get_providers():
    return [provider for provider in dir(fake) if provider[0].islower()]
