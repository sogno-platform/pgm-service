from fastapi import FastAPI

app = FastAPI(title=" API") 


from payment_calculation.router import router
app.include_router(router, prefix="/api")
