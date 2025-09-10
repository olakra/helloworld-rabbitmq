/**
 * RabbitMQ adapter
 * - Responsible for connecting to RabbitMQ and providing helpers to publish/consume.
 * - Keeps amqplib usage isolated (Infrastructure layer).
 */

import amqp, { Connection, Channel, ConsumeMessage } from 'amqplib';
import { URL } from 'url';

export type RabbitConfig = {
  url: string;
};

export class RabbitMQAdapter {
  private conn?: Connection;
  private channel?: Channel;
  constructor(private config: RabbitConfig) {}

  async connect() {
    const url = new URL(this.config.url);
    this.conn = await amqp.connect(url.toString());
    this.channel = await this.conn.createChannel();
  }

  async assertQueue(queueName: string) {
    if (!this.channel) throw new Error('Channel not initialized');
    await this.channel.assertQueue(queueName, { durable: false });
  }

  async consume(queueName: string, onMessage: (msg: ConsumeMessage) => void) {
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

  ack(msg: ConsumeMessage) {
    if (!this.channel) throw new Error('Channel not initialized');
    this.channel.ack(msg);
  }

  close() {
    if (this.conn) {
      return this.conn.close();
    }
  }
}
