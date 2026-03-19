import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import './index.css'
import App from './App.jsx'
import { RouterProvider } from 'react-router-dom'
import { router } from './router/index.jsx'
import configureStore from './redux/store.js'

const store = configureStore()

// Wait for session restoration before first render
;(async () => {
  try {
    await store.dispatch(authenticate())
  } catch (err) {
    // ignore - app can continue if restore fails
    console.warn('session restore failed', err)
  }

  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <Provider store={store}>
        <RouterProvider router={router} />
      </Provider>
    </StrictMode>,
  )
})()
