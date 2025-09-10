/**
 * Use-case (application layer)
 * - Implements business logic for echoing a message
 * - Pure function, easy to unit test (TDD)
 */

import { EchoRequest, EchoResponse } from '../domain/models';

export function echoUsecase(req: EchoRequest): EchoResponse {
  // business rules could go here
  const now = new Date().toISOString();
  return {
    id: req.id,
    payload: req.payload,
    echoedAt: now
  };
}
