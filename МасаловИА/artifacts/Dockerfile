FROM golang:1.25 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go clean -modcache
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o smart-cart ./cmd/server

FROM alpine:3.19
WORKDIR /app
RUN adduser -D appuser
COPY --from=builder /app/smart-cart .
USER appuser
EXPOSE 8080
CMD ["./smart-cart"]