import { NavigateFunction, useNavigate } from "react-router-dom";

export default function LogOutForm() {
  const navigate: NavigateFunction = useNavigate();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:5001/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });

      // Handle network errors
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      console.log('Logged out successfully');
      // Redirect to the home page upon success
      return navigate("/")

    } catch(error) {
      // Handle HTTP errors
      throw new Error(`Error submitting form:${error}`);
    }
  }

  return (
    <form method="post" onSubmit={handleSubmit}>
      <button type="submit">Sign Out</button>
    </form>
  )
}