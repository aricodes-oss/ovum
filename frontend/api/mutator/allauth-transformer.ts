import type {
  OpenAPIObject,
  PathItemObject,
  OperationObject,
  ParameterObject,
  ReferenceObject,
} from 'openapi3-ts/oas30';

/**
 * Transforms the django-allauth OpenAPI schema to:
 * - Prepend /api and hardcode {client} as browser
 * - Remove the {client} path parameter from functions
 * - Set readable operationIds for hook generation
 * - Remove problematic $refs in the description
 */
export default function allauthTransformer(schema: OpenAPIObject): OpenAPIObject {
  const newPaths: Record<string, PathItemObject> = {};

  for (const [pathKey, pathObj] of Object.entries(schema.paths || {})) {
    // Replace {client} with browser and prepend /api
    const newPathKey = '/api' + pathKey.replace('{client}', 'browser');

    // Create a shallow copy of the path object
    const newPathObj: PathItemObject = { ...(pathObj as PathItemObject) };

    // Determine if this path has multiple HTTP methods
    const httpMethods = ['get', 'post', 'put', 'delete', 'patch'];
    const methodsInPath = Object.keys(newPathObj).filter((k) =>
      httpMethods.includes(k.toLowerCase()),
    );
    const hasMultipleMethods = methodsInPath.length > 1;

    // Build the base Operation ID from the URL path
    const pathCleaned = pathKey
      .replace('/_allauth/{client}/v1/', '')
      .replace('/_allauth/browser/v1/', '');
    // Split on slashes, dashes, or underscores
    const pathParts = pathCleaned.split(/[-_/]/).filter(Boolean);
    const baseId = pathParts.map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join('');

    for (const [method, methodObj] of Object.entries(newPathObj)) {
      if (typeof methodObj === 'object' && methodObj !== null) {
        // Set operationId to override Orval's default naming (which includes ApiAllauthBrowserV1)
        if (httpMethods.includes(method.toLowerCase())) {
          const typedMethodObj = methodObj as OperationObject;
          const operationId = hasMultipleMethods
            ? method.toLowerCase() + baseId
            : baseId.charAt(0).toLowerCase() + baseId.slice(1);

          typedMethodObj.operationId = operationId;

          if (typedMethodObj.parameters) {
            // Filter out the Client parameter ref
            typedMethodObj.parameters = typedMethodObj.parameters.filter(
              (p: ParameterObject | ReferenceObject) =>
                (p as ReferenceObject).$ref !== '#/components/parameters/Client',
            );

            if (typedMethodObj.parameters.length === 0) {
              delete typedMethodObj.parameters;
            }
          }
        }
      }
    }

    newPaths[newPathKey] = newPathObj;
  }

  schema.paths = newPaths;

  if (schema.info && schema.info.description) {
    // Avoid $ref loading issues for description.md
    schema.info.description = 'django-allauth headless API modified for ovum';
  }

  return schema;
}
