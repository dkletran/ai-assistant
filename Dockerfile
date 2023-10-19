FROM python:3.11 as build
WORKDIR /app
RUN pip install poetry==1.6.1
COPY poetry.lock pyproject.toml ./
RUN poetry export --without dev -o requirements.txt
RUN python -m venv .venv && \
    .venv/bin/pip install -r requirements.txt

FROM python:3.11-slim as runtime
WORKDIR /app
COPY --from=build /app/.venv .venv
COPY src .
EXPOSE 8501
CMD ["/app/.venv/bin/streamlit", "run", "app.py"]