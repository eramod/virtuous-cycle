import { Form, redirect } from "react-router-dom";

export default function NewQuoteForm() {
  return (
    <Form method="post">
      <label>
        Content:
        {/* TODO: Change this to a different type to fit more text, is it textbox? */}
        <input type="text" required name="content" />
      </label>
      <label>
        Attribution:
        <input type="text" name="attribution" />
      </label>
      <button type="submit">Add Quote</button>
    </Form>
  )
}
// NOTE: request is not a real request object. It is from react-router and
// represents communication within the front end router.
export async function createQuoteAction({request}) {
  const formData = await request.formData();

  try {
    const response = await fetch('http://localhost:5001/api/quotes/', {
      method: 'POST',
      body: formData,
      credentials: 'include',
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