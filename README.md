# Prometheus FastApi Pusher

## install

```bash
./venv/bin/python3 -m pip install -e git+https://github.com/dreamhunter2333/fastapi_prometheus_pusher.git#egg=fastapi_prometheus_pusher
```

```python
from fastapi_prometheus_pusher import FastApiPusher

app = FastAPI()


@app.on_event("startup")
async def startup():
    FastApiPusher(
        excluded_handlers="health_check"
    ).start(app, "localhost:9091", "awsl")
```

## ref

- [dmontagu/fastapi-utils](https://github.com/dmontagu/fastapi-utils)
- [trallnag/prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
