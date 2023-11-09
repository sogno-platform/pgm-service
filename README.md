# pgm-service

## Install

Create and activate a Python 3.12 virtual environment. Go to the root folder of this repository. Run

```bash
python -m pip install build
python -m build --wheel --outdir dist
docker build --no-cache -t pgm-service .
```

## Run

After you have created a docker image. You can run it.

```bash
docker run -p 80:80 pgm-service
```
