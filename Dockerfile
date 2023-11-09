FROM python:3-slim

COPY dist /dist

RUN pip install dist/*.whl

EXPOSE 80

ENV PATH /usr/local/bin:$PATH

ENTRYPOINT ["pgm-service"]

