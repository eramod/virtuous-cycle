import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from 'react-router-dom';
import Root from './routes/root.tsx';
import ErrorPage from './error-page.tsx';
import Register from './routes/register.tsx';
import Login from './routes/login.tsx';
import Quotes from './routes/quotes.tsx';
import { registerAction } from './components/registration-form.tsx';
import { loginAction } from './components/login-form.tsx';
import { createQuoteAction } from './components/new-quote-form.tsx';

const router = createBrowserRouter(
  createRoutesFromElements (
    <Route
      path="/"
      element={<Root />}
      errorElement={<ErrorPage />} >

      <Route
        path="register"
        element={<Register />}
        action={registerAction}/>

      <Route
        path="login"
        element={<Login />}
        action={loginAction} />

      <Route
        path="quotes"
        element={<Quotes />}
        action={createQuoteAction} />
    </Route>
  )
);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
