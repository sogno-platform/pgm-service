FROM python:3

WORKDIR /code

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir power-grid-model fastapi "uvicorn[standard]"

COPY ./app /code/app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
