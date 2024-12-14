import { Form, redirect } from "react-router-dom";

export default function RegistrationForm() {

  return (
    <Form method="post" action="/register">
      <label>
        Email
        <input type="email" name="email" />
      </label>
      <label>
        First Name:
        <input type="text" name="first_name" />
      </label>
      <label>
        Last Name:
        <input type="text" name="last_name" />
      </label>
      <label>
        Phone Number:
        <input type="tel" name="phone_number" />
      </label>
      <label>
        Password:
        <input id="pasword" type="text" name="password" />
      </label>
      <label>
        Confirm Password:
        <input type="text" name="confirm_password" />
      </label>
      <button type="submit">Register</button>
    </Form>
  )
}
// NOTE: request is not a real request object. It is from react-router and
export async function registerAction({request}) {
  const formData = await request.formData();

  try {
    const response = await fetch('http://localhost:5001/auth/register', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // Handle success
    return redirect('/login');
  } catch (error) {
    // Handle error
    throw new Error(`Error submitting form:${error}`);
  }
}