import { echoUsecase } from '../src/usecases/echoUsecase';

describe('echoUsecase', () => {
  it('returns an EchoResponse with same payload and timestamp', () => {
    const req = { id: '1', payload: 'hello' };
    const resp = echoUsecase(req);
    expect(resp.id).toBe('1');
    expect(resp.payload).toBe('hello');
    expect(typeof resp.echoedAt).toBe('string');
    expect(new Date(resp.echoedAt).toString()).not.toBe('Invalid Date');
  });
});
