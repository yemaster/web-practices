FROM golang:1.25.2-alpine as builder

WORKDIR /builder

COPY authorizer/go.mod authorizer/go.sum ./
RUN go mod download

COPY authorizer/. ./
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o authorizer

FROM python:3.13-alpine

WORKDIR /app

COPY --from=builder /builder/authorizer ./authorizer/authorizer
COPY ./vault ./vault

RUN pip install --no-cache-dir -r vault/requirements.txt

COPY entrypoint.sh /

RUN adduser -S -H authorizer &&\
    adduser -S -H vault &&\
    chown -R authorizer:nobody /app/authorizer &&\
    chown -R vault:nobody /app/vault &&\
    chmod -R 700 /app/authorizer &&\
    chmod -R 700 /app/vault &&\
    chmod 700 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]