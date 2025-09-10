/**
 * RabbitMQ adapter
 * - Responsible for connecting to RabbitMQ and providing helpers to publish/consume.
 * - Keeps amqplib usage isolated (Infrastructure layer).
 */

import * as amqp from 'amqplib';

export type RabbitConfig = {
  url: string;
};

export class RabbitMQAdapter {
  private conn?: amqp.Connection;
  private channel?: amqp.Channel;
  constructor(private config: RabbitConfig) {}

  async connect(url: string): Promise<void> {
      this.conn = await amqp.connect(url) as unknown as amqp.Connection;
      if (!this.conn) throw new Error('Failed to connect to RabbitMQ');
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      this.channel = await (this.conn as any).createChannel();
      if (!this.channel) throw new Error('Failed to create channel');
  }

  async assertQueue(queueName: string) {
    if (!this.channel) throw new Error('Channel not initialized');
    await this.channel.assertQueue(queueName, { durable: false });
  }

  async consume(queueName: string, onMessage: (msg: amqp.ConsumeMessage) => void) {
    if (!this.channel) throw new Error('Channel not initialized');
    await this.channel.consume(queueName, (msg) => {
      if (msg) {
        onMessage(msg);
      }
    }, { noAck: false });
  }

  async sendToQueue(queueName: string, content: Buffer, opts?: amqp.Options.Publish) {
    if (!this.channel) throw new Error('Channel not initialized');
    this.channel.sendToQueue(queueName, content, opts);
  }

  ack(msg: amqp.ConsumeMessage) {
    if (!this.channel) throw new Error('Channel not initialized');
    this.channel.ack(msg);
  }

  close() {
    if (this.conn) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      return (this.conn as any).close();
    }
  }
}
