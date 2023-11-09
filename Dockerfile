FROM python:3-slim

COPY dist /dist

RUN pip install dist/*.whl

EXPOSE 5000

ENV PATH /usr/local/bin:$PATH

ENTRYPOINT ["pgm-service"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
