FROM python:3-slim as builder

COPY . /src
WORKDIR /src

RUN pip install build

RUN python -m build


FROM python:3-slim

COPY --from=builder /src/dist /dist

RUN pip install --no-cache-dir --no-compile dist/*.whl

EXPOSE 80

ENV PATH /usr/local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["pgm-service"]

