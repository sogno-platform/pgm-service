import uvicorn


def run():
    print("Starting unvicorn service.")
    uvicorn.run("pgm_service.app:app", host="0.0.0.0", port=80, log_level="info")
