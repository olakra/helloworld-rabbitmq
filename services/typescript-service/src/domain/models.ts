/**
 * Domain models
 *
 * This is intentionally tiny; domain may grow for real apps.
 */

export type EchoRequest = {
  id: string;
  payload: string;
};

export type EchoResponse = {
  id: string;
  payload: string;
  echoedAt: string; // ISO timestamp
};
