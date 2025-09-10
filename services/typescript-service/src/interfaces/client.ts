/**
 * Simple RPC client for testing/demo.
 * Sends a request to RPC_QUEUE and waits for reply on an exclusive temporary queue.
 */

import amqp from 'amqplib';
import { v4 as uuidv4 } from 'uuid';
import { EchoRequest, EchoResponse } from '../domain/models';

export async function rpcCall(rabbitUrl: string, payload: string, timeoutMs = 5000): Promise<EchoResponse> {
  const conn = await amqp.connect(rabbitUrl);
  const ch = await conn.createChannel();
  const q = await ch.assertQueue('', { exclusive: true }); // reply queue
  const correlationId = uuidv4();

  return new Promise<EchoResponse>((resolve, reject) => {
    const timer = setTimeout(() => {
      ch.close().catch(() => {});
      conn.close().catch(() => {});
      reject(new Error('RPC timeout'));
    }, timeoutMs);

    ch.consume(q.queue, (msg) => {
      if (msg && msg.properties.correlationId === correlationId) {
        clearTimeout(timer);
        try {
          const resp = JSON.parse(msg.content.toString()) as EchoResponse;
          resolve(resp);
        } catch (e) {
          reject(e);
        } finally {
          ch.ack(msg);
          ch.close().catch(() => {});
          conn.close().catch(() => {});
        }
      }
    }, { noAck: false }).then(() => {
      const req: EchoRequest = { id: correlationId, payload };
      ch.sendToQueue('rpc_queue', Buffer.from(JSON.stringify(req)), {
        correlationId,
        replyTo: q.queue
      });
    }).catch(reject);
  });
}
