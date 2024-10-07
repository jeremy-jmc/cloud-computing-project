FROM golang:1.23.2


WORKDIR /app

COPY . .

RUN go get github.com/gorilla/mux && go get github.com/lib/pq && go get github.com/rs/cors

EXPOSE 8002

CMD ["go", "run", "main.go"]