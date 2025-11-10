FROM python:3.14.0-slim-bookworm AS build

WORKDIR /app

RUN pip install build
COPY . .
RUN python -m build --wheel

RUN apt-get update
RUN apt-get install -y sqlite3
RUN sqlite3 database.db < schema.sql
RUN sqlite3 database.db < init.sql

FROM python:3.14.0-slim-bookworm AS run

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /app/dist/*.whl .

RUN apt-get update
RUN apt-get install -y sqlite3
COPY --from=build /app/database.db .
COPY --from=build /app/recipes/templates ./recipes/templates/

RUN pip install *.whl

RUN pip install waitress

EXPOSE 8080
ENTRYPOINT ["waitress-serve"]
CMD ["--call", "recipes:create_app"]