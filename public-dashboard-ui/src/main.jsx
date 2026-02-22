import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'

// In prod, VITE_BASE_PATH is "/dashboard/" — this ensures the router
// generates links like /dashboard/about instead of /about.
// Locally it falls back to "/" so dev-server routing works unchanged.
const basePath = import.meta.env.VITE_BASE_PATH || '/'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter basename={basePath}>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
