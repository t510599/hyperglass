import type { FormData, PingQueryResponse, StringTableData, StringQueryResponse } from './data';
import type { DirectiveSelect, Directive, Link, Menu } from './config';

export function isString(a: unknown): a is string {
  return typeof a === 'string';
}

/**
 * Type Guard to determine if an argument is an object, e.g. `{}` (`Record<string, unknown>`).
 * Maintains type of object if a type argument is provided.
 */
export function isObject<T extends unknown = unknown>(
  obj: unknown,
): obj is { [P in keyof T]: T[P] } {
  return typeof obj === 'object' && obj !== null && !Array.isArray(obj);
}

export function isStructuredOutput(data: unknown): data is StringTableData {
  return (
    isObject<{ output: unknown }>(data) &&
    'output' in data &&
    isObject<{ routes: unknown }>(data.output) &&
    'routes' in data.output &&
    Array.isArray(data.output.routes)
  );
}

export function isStringOutput(data: unknown): data is StringQueryResponse {
  return (
    isObject(data) && 'output' in data && typeof (data as { output: unknown }).output === 'string'
  );
}

export function isPingOutput(data: unknown): data is PingQueryResponse {
  return (
    isObject<{ output: unknown }>(data) &&
    'output' in data &&
    isObject<{ output: unknown; latency: unknown }>(data.output) &&
    typeof data.output.output === 'string' &&
    typeof data.output.latency === 'number'
  );
}

/**
 * Determine if a form field name is a valid form key name.
 */
export function isQueryField(field: string): field is keyof FormData {
  return ['queryLocation', 'queryType', 'queryTarget'].includes(field);
}

/**
 * Determine if a directive is a select directive.
 */
export function isSelectDirective(directive: Directive): directive is DirectiveSelect {
  return directive.fieldType === 'select';
}

export function isLink(item: Link | Menu): item is Link {
  return 'url' in item;
}

export function isMenu(item: Link | Menu): item is Menu {
  return 'content' in item;
}
