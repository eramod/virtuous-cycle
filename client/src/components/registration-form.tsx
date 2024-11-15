import { Form } from "react-router-dom";

export default function RegistrationForm() {
  return (
    <Form method="post" action="/register">
      {/* <label>
        Email
        <input type="email" name="email" />
      </label> */}
      <label>
        First Name:
        <input type="text" name="first_name" />
      </label>
      <label>
        Last Name:
        <input type="text" name="last_name" />
      </label>
      {/* <label>
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
      </label> */}
      <button type="submit">Register</button>
    </Form>
  )
}