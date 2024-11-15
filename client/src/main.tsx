import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  createRoutesFromElements,
  redirect,
  RouterProvider,
  Route
} from 'react-router-dom';
import Root from './routes/root.tsx';
import ErrorPage from './error-page.tsx';
import Register from './routes/register.tsx';
import Login from './routes/login.tsx';

const router = createBrowserRouter(
  createRoutesFromElements (
    <Route path="/" element={<Root />} errorElement={<ErrorPage />}>
      <Route path="register" element={<Register />} action={handleFormSubmission} />
      <Route path="login" element={<Login />} />
    </Route>
  )

);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);

async function handleFormSubmission(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
  const formData = new FormData(event.target);

  try {
    const response = await fetch('http://127.0.0.1:5000/auth/register', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      console.log(response)
      throw new Error('Network response was not ok');
    }

    // Handle success (redirect, update state, etc.)
    return redirect('/success');
  } catch (error) {
    console.log(error)
    // Handle error
    console.error('Error submitting form:', error);
  }
}


// Pass to createBrowserRouter
// [
//   {
//     path: "/",
//     element: <Root />,
//     errorElement: <ErrorPage />,
//     children: [
//       {
//         path: "register",
//         element: <Register />,
//         action: async function (event) {
//           event.preventDefault();
//           const formData = new FormData(event.target);

//           try {
//             const response = await fetch('/api/submit', {
//               method: 'POST',
//               body: formData,
//             });

//             if (!response.ok) {
//               throw new Error('Network response was not ok');
//             }

//             // Handle success (redirect, update state, etc.)
//             return redirect('/success');
//           } catch (error) {
//             // Handle error
//             console.error('Error submitting form:', error);
//           }
//         }
//       },
//       {
//         path: "login",
//         element: <Login />
//       }
//     ]
//   },
// ]
