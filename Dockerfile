FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY --chown=node:node . ./
CMD ["/bin/bash","docker-entrypoint.sh"]