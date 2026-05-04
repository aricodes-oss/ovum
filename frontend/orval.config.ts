import { defineConfig } from 'orval';

export default defineConfig({
  backend: {
    input: 'http://backend:3000/api/schema/',
    output: {
      target: './api/backend.ts',
      client: 'react-query',
      httpClient: 'axios',
      override: {
        namingConvention: {
          enum: 'camelCase',
        },
        mutator: {
          path: './api/mutator/custom-instance.ts',
          name: 'customInstance',
        },
      },
    },
  },
  allauth: {
    input: {
      target:
        'https://django-allauth.readthedocs.io/en/latest/headless/openapi-specification/openapi.yaml',
      // We must disable validation because the official allauth OpenAPI spec
      // contains an external reference to `description.md` which isn't valid JSON/YAML,
      // causing the default validation pipeline to crash.
      unsafeDisableValidation: true,
      override: {
        transformer: './api/mutator/allauth-transformer.ts',
      },
    },
    output: {
      target: './api/allauth.ts',
      client: 'react-query',
      httpClient: 'axios',
      override: {
        namingConvention: {
          enum: 'camelCase',
        },
        mutator: {
          path: './api/mutator/custom-instance.ts',
          name: 'customInstance',
        },
      },
    },
  },
});
