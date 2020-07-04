FROM alpine:3.12
COPY ./requirements.txt /build/requirements.txt
RUN apk add --no-cache --update python3 postgresql py3-pip py3-six && \
    apk add --no-cache --update --virtual .build-deps python3-dev postgresql-dev gcc musl-dev && \
    pip3 install -r /build/requirements.txt && \
    apk del .build-deps
ENV PYTHONPATH="/code/src:${PYTHONPATH}"
ADD . /code/
WORKDIR /code/
ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["gunicorn", "-c", "/code/src/api/gunicorn.py", "api.wsgi:APP"]