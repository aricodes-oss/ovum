import tanstackQueryPlugin from '@tanstack/eslint-plugin-query';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTs from 'eslint-config-next/typescript';
import prettierConfig from 'eslint-config-prettier';
import prettierPlugin from 'eslint-plugin-prettier';
import reactCompilerPlugin from 'eslint-plugin-react-compiler';
import sonarjs from 'eslint-plugin-sonarjs';
import unicorn from 'eslint-plugin-unicorn';
import { defineConfig, globalIgnores } from 'eslint/config';

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  sonarjs.configs.recommended,
  unicorn.configs.recommended,
  {
    plugins: {
      'react-compiler': reactCompilerPlugin,
      '@tanstack/query': tanstackQueryPlugin,
      prettier: prettierPlugin,
    },
    rules: {
      'react-compiler/react-compiler': 'error',
      'prettier/prettier': 'error',
      '@tanstack/query/exhaustive-deps': 'error',
      '@tanstack/query/no-rest-destructuring': 'warn',
      '@tanstack/query/stable-query-client': 'error',
      'unicorn/prevent-abbreviations': 'off',
      'unicorn/filename-case': [
        'error',
        {
          cases: {
            kebabCase: true,
            pascalCase: true,
          },
        },
      ],
      'sonarjs/no-duplicate-string': 'warn',
      'sonarjs/no-clear-text-protocols': 'off',
    },
  },
  {
    files: ['api/**/*.ts', 'orval.config.ts'],
    rules: {
      'sonarjs/no-duplicate-string': 'off',
      'sonarjs/redundant-type-aliases': 'off',
      'sonarjs/no-nested-conditional': 'off',
      'sonarjs/use-type-alias': 'off',
      'sonarjs/cognitive-complexity': 'off',
      'unicorn/no-empty-file': 'off',
      'unicorn/no-abusive-eslint-disable': 'off',
      'unicorn/prefer-module': 'off',
      'unicorn/prefer-global-this': 'off',
    },
  },
  prettierConfig,
  globalIgnores(['.next/**', 'out/**', 'build/**', 'next-env.d.ts']),
]);

export default eslintConfig;
