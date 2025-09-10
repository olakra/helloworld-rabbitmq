#!/usr/bin/env bash
set -e
host="${1:-rabbitmq}"
port="${2:-5672}"
echo "Waiting for $host:$port..."
until nc -z "$host" "$port"; do
  sleep 0.5
done
echo "RabbitMQ is up"
