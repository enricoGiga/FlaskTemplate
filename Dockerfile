FROM python:3.12-alpine
LABEL maintainer="ENRICO GIGANTE"
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 5000
# by default we don't running our dockerfile in development mode
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# the path is the env variab that's automatically created on Linux OS
# so whenever we luch a python command it will run automatically from our python environment
ENV PATH="/py/bin:$PATH"
CMD ["flask", "run", "--host", "0.0.0.0"]