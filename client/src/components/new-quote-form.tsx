import { Form, redirect } from "react-router-dom";
import Modal from "./reusable/modal-wrapper";

interface NewQuoteFormProps {
  isModalOpen: boolean;
  setIsModalOpen: (isOpen: boolean) => void;
}

export default function NewQuoteForm({isModalOpen, setIsModalOpen}: NewQuoteFormProps) {

  return (
    <Modal isOpen={isModalOpen}
      onClose={() => setIsModalOpen(false)}
      title="Add a Quote">
      <Form method="post" action="new-quote-form">
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
    </Modal>
  )
}
// Question: Should I be using the route action to submit this form? Maybe not, since it's a modal?

// NOTE: request is not a real request object. It is from react-router and
// represents communication within the front end router.
import { ActionFunctionArgs } from "react-router-dom";

export async function createQuoteAction({ request }: ActionFunctionArgs) {
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

    return redirect('/quotes');
  } catch (error) {
    // Handle error
    throw new Error(`Error submitting form:${error}`);
  }
}