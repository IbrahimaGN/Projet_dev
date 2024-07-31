import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/consulter': 'http://localhost:5000',
      '/buy': 'http://localhost:5000',
      '/prompts': 'http://localhost:5000',
    }
  }
});
