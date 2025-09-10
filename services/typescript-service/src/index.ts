/**
 * Application entrypoint.
 *
 * Usage:
 *   RABBITMQ_URL=amqp://guest:guest@localhost:5672 npm run dev
 *
 * This file starts the server and also demonstrates a client RPC call.
 */

import { createServer } from './interfaces/server';
import { rpcCall } from './interfaces/client';

const RABBITMQ_URL = process.env.RABBITMQ_URL ?? 'amqp://guest:guest@localhost:5672';

async function main() {
  // start server (non-blocking)
  createServer(RABBITMQ_URL).catch((err) => {
    console.error('Failed to start server', err);
    process.exit(1);
  });

  // give server a second to be ready (in prod use better readiness checks)
  setTimeout(async () => {
    try {
      console.log('Sending demo RPC call...');
      const res = await rpcCall(RABBITMQ_URL, 'Hello from demo client');
      console.log('RPC response:', res);
    } catch (err) {
      console.error('Demo RPC failed', err);
    }
  }, 1000);
}

main();
