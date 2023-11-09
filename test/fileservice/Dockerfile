FROM python:3.12

RUN python -m pip install fastapi; mkdir /data
COPY fileservice.py fileservice.py

EXPOSE 8080
ENV DATA_DIR=/data
CMD [ "python", "-m", "uvicorn", "fileservice:app", "--host", "0.0.0.0", "--port", "8080" ]
