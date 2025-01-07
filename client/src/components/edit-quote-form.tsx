import { Form, redirect } from "react-router-dom";
import Modal from "./reusable/modal-wrapper";

interface EditQuoteFormProps {
  isModalOpen: boolean;
  setIsModalOpen: (isOpen: boolean) => void;
}

export default function EditQuoteForm({isModalOpen, setIsModalOpen}: EditQuoteFormProps) {
  return (
    <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Edit a Quote">
      <Form method="post" action="edit-quote-form">
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

// NOTE: request is not a real request object. It is from react-router and
// represents communication within the front end router.
export async function editQuoteAction({request}) {
  const formData = await request.formData();

  try {
    const response = await fetch(`http://localhost:5001/api/quotes/${id}`, {
      method: 'PUT',
      body: formData,
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // TODO: Update: What I really want to do is close the modal and update the quote list. Not sure how to do that.
    return redirect('/quotes');
  } catch (error) {
    // Handle error
    throw new Error(`Error submitting form:${error}`);
  }
}