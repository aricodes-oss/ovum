import Axios, { AxiosRequestConfig } from 'axios';
import Cookies from 'js-cookie';
import setCookieParser from 'set-cookie-parser';

export interface NextCookieOptions {
  domain?: string;
  path?: string;
  expires?: Date;
  maxAge?: number;
  httpOnly?: boolean;
  secure?: boolean;
  sameSite?: true | false | 'lax' | 'strict' | 'none';
}

interface CookieStore {
  get(name: string): unknown;
  set?(name: string, value: string, options?: NextCookieOptions): void;
}

const isServer = typeof window === 'undefined';

const baseURL = isServer ? 'http://backend:3000' : '/';

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
  let nextCookiesSet:
    | ((name: string, value: string, options?: NextCookieOptions) => void)
    | undefined;

  if (isServer) {
    try {
      // Use require() to bypass Orval's static analysis crashing on import()
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const { cookies, headers } = require('next/headers');
      const [headersList, cookiesList] = await Promise.all([headers(), cookies()]);

      const cookie = headersList.get('cookie');
      cookieStore = cookiesList as unknown as CookieStore;

      // Store reference to Next.js cookie setter
      if (typeof cookiesList.set === 'function') {
        nextCookiesSet = cookiesList.set.bind(cookiesList);
      }

      if (cookie) {
        const csrfCookie = cookieStore.get('csrftoken');
        const csrfToken =
          csrfCookie && typeof csrfCookie === 'object' && 'value' in csrfCookie
            ? (csrfCookie as { value: string }).value
            : (csrfCookie as string) || '';

        config.headers = {
          ...config.headers,
          cookie,
          'X-CSRFToken': csrfToken,
        };
      }
    } catch {
      // During orval generation or other non-Next.js environments, this might fail
      // We just skip the server-side cookie logic
    }
  } else {
    config.headers = {
      ...config.headers,
      'X-CSRFToken': (cookieStore.get('csrftoken') as string) || '',
    };
  }

  const response = await client({ ...config, ...options });

  // Forward Set-Cookie headers from Backend -> Next.js Server -> Browser
  if (isServer && nextCookiesSet && response.headers && response.headers['set-cookie']) {
    const setCookieHeaders = response.headers['set-cookie'];
    const parsedCookies = setCookieParser.parse(setCookieHeaders);

    for (const cookie of parsedCookies) {
      nextCookiesSet(cookie.name, cookie.value, {
        domain: cookie.domain,
        path: cookie.path,
        expires: cookie.expires,
        maxAge: cookie.maxAge,
        httpOnly: cookie.httpOnly,
        secure: cookie.secure,
        sameSite: cookie.sameSite?.toLowerCase() as NextCookieOptions['sameSite'],
      });
    }
  }

  return response.data;
};

export default client;
