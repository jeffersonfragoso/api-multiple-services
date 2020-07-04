FROM alpine:3.12
COPY ./requirements.txt /build/requirements.txt
RUN apk add --no-cache --update python3 && \
    apk add --no-cache --update --virtual .build-deps py3-pip && \
    pip3 install -r /build/requirements.txt && \
    apk del .build-deps
ENV PYTHONPATH="/code/src:${PYTHONPATH}"
ADD . /code/
WORKDIR /code/
ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["/code/src/run_service"]