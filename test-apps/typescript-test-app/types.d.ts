// Type declarations for the TypeScript test app
// This file is intentionally minimal to demonstrate TypeScript issues

declare module 'axios';
declare module 'fs';
declare module 'path';
declare module 'crypto';
declare module 'http';

// Add Node.js global objects
interface NodeRequire {
  (id: string): any;
}
declare var require: NodeRequire;
declare var Buffer: any;
