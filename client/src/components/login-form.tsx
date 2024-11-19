import { Form, redirect } from "react-router-dom";

export default function LoginForm() {
  return (
    <Form method="post" action="/login">
      <label>
        Email:
        <input type="text" name="email" />
      </label>
      <label>
        Password:
        <input type="text" name="password" />
      </label>
      <button type="submit">Login</button>
    </Form>
  )
}

export async function loginAction({request}) {
  const formData = await request.formData();

  try {
    const response = await fetch('http://localhost:5001/auth/login', {
      method: 'POST',
      body: formData
    });

    // Handle network errors
    if (!response.ok) {
      throw new Error("Network response was not OK");
    }

    // Redirect to the user's home page upon success
    return redirect("/")

  } catch(error) {
    // Handle HTTP errors
    throw new Error(`Error submitting form:${error}`);
  }
}