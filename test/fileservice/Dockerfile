FROM python:3.10

RUN python -m pip install fastapi uvicorn && mkdir /data
COPY fileservice.py fileservice.py

EXPOSE 8080
ENV DATA_DIR=/data
CMD [ "python", "-m", "uvicorn", "fileservice:app", "--host", "0.0.0.0", "--port", "8080" ]
