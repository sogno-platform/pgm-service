FROM python:3-slim as builder

COPY . /src
WORKDIR /src

RUN pip install build

RUN python -m build


FROM python:3-slim

COPY --from=builder /src/dist /dist

RUN pip install dist/*.whl

EXPOSE 80

ENV PATH /usr/local/bin:$PATH

ENTRYPOINT ["pgm-service"]

