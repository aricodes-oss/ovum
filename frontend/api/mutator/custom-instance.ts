import Axios, { AxiosRequestConfig } from 'axios';
import Cookies from 'js-cookie';

interface CookieStore {
  get(name: string): unknown;
}

const isServer = typeof window === 'undefined';

const baseURL = isServer ? 'http://backend:3000/api' : '/';

const client = Axios.create({
  baseURL,
});

/**
 * Custom instance for Orval mutator.
 * Handles CSRF tokens and server-side cookies for Next.js 16.
 */
export const customInstance = async <T>(
  config: AxiosRequestConfig,
  options?: AxiosRequestConfig,
): Promise<T> => {
  let cookieStore = Cookies as CookieStore;

  if (isServer) {
    try {
      // Use require() to bypass Orval's static analysis crashing on import()
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const { cookies, headers } = require('next/headers');
      const [headersList, cookiesList] = await Promise.all([headers(), cookies()]);

      const cookie = headersList.get('cookie');
      cookieStore = cookiesList as unknown as CookieStore;

      if (cookie) {
        config.headers = {
          ...config.headers,
          cookie,
          'X-CSRFToken': (cookieStore.get('csrftoken') as string) || '',
        };
      }
    } catch (error) {
      // During orval generation or other non-Next.js environments, this might fail
      // We just skip the server-side cookie logic
    }
  } else {
    config.headers = {
      ...config.headers,
      'X-CSRFToken': (cookieStore.get('csrftoken') as string) || '',
    };
  }

  return (await client({ ...config, ...options })).data;
};

export default client;
