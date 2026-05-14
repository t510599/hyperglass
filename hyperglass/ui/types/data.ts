export interface FormData {
  queryLocation: string[];
  queryType: string;
  queryTarget: string[];
}

export type FormQuery = Swap<FormData, 'queryLocation', string>;

export type StringTableData = Swap<QueryResponse, 'output', StructuredResponse>;

export type StringQueryResponse = Swap<QueryResponse, 'output', string>;

export type PingQueryResponse = Swap<QueryResponse, 'output', PingResponse>;

export type ErrorLevels = 'success' | 'warning' | 'error';
