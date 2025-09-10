/**
 * Server: entrypoint for the service. Sets up RabbitMQ listener to the 'rpc_queue'
 * and handles request/reply semantics.
 *
 * Clean architecture:
 *  - This file composes adapters + usecases. It doesn't implement business logic.
 */

import { RabbitMQAdapter } from '../adapters/rabbitmqAdapter';
import { echoUsecase } from '../usecases/echoUsecase';
import { v4 as uuidv4 } from 'uuid';

const RPC_QUEUE = 'rpc_queue';

export async function createServer(rabbitUrl: string) {
  const adapter = new RabbitMQAdapter({ url: rabbitUrl });
  await adapter.connect(rabbitUrl);
  await adapter.assertQueue(RPC_QUEUE);
  console.log(' [x] Awaiting RPC requests');

  await adapter.consume(RPC_QUEUE, (msg) => {
    try {
      const content = msg.content.toString();
      const reqObj = JSON.parse(content);
      const correlationId = msg.properties.correlationId;
      const replyTo = msg.properties.replyTo;

      // validate/convert domain model
      const req = {
        id: reqObj.id || uuidv4(),
        payload: String(reqObj.payload || '')
      };

      const result = echoUsecase(req);
      const responseBuffer = Buffer.from(JSON.stringify(result));

      if (replyTo && correlationId) {
        adapter.sendToQueue(replyTo, responseBuffer, { correlationId });
      } else {
        console.warn('Missing replyTo or correlationId; dropping response');
      }
      adapter.ack(msg);
    } catch (err) {
      console.error('Error processing message', err);
      adapter.ack(msg);
    }
  });
}
