# Python implementation

Run the following commands from this directory. Python 3.12 or later and [uv](https://docs.astral.sh/uv/) are required.

Install the project and its development dependencies:

```sh
uv sync --locked
```

Start the API server:

```sh
uv run python -m smartest_ai_testbook
```

The server listens on port `3002` by default. Set the `PORT` environment variable to use another port.

Run the tests:

```sh
uv run pytest tests -v

# or, from root: 

uv run --project python pytest -v
```

`uv run` synchronizes the environment before running a command.
