FROM python:3.12-alpine
LABEL maintainer="ENRICO GIGANTE"
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY flask_template /app

WORKDIR /app
EXPOSE 5000
# by default we don't running our dockerfile in development mode
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache tzdata && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime
RUN cp /etc/localtime /etc/localtime
# the path is the env variab that's automatically created on Linux OS
# so whenever we luch a python command it will run automatically from our python environment
ENV PATH="/py/bin:$PATH"
ENV TZ=Europe/Dublin
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]