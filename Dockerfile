FROM python:3-slim

COPY dist /dist

RUN pip install --no-cache-dir --no-compile dist/*.whl

EXPOSE 80

ENV PATH /usr/local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["pgm-service"]

