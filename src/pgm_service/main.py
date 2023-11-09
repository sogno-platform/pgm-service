import uvicorn


def run():
    print("Starting unvicorn service.")
    uvicorn.run("pgm_service.app:app", port=5000, log_level="info")
