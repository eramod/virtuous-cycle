import { useEffect, useState } from "react"
import NewQuoteForm from "../components/new-quote-form";

interface Quote {
  id: string,
  content: string,
  attribution?: string | null
}

export default function Quotes() {
  const [quotes, setQuotes] = useState<Quote[] | null>(null);
  const [shouldShowQuoteForm, setShouldShowQuoteForm] = useState<boolean>(false);

  useEffect(() => {
    fetch('http://localhost:5001/api/quotes/', {
      credentials: 'include'
    })
      .then(res => res.json())
      .then(json => {
        setQuotes(json.body)
      })
      .catch(error => {
        console.error('Error fetching quotes:', error)
      })

  }, [setQuotes])

  return (
    <>
      <button type="button" onClick={() => setShouldShowQuoteForm(true)}>
        Add a quote
      </button>
      {/* TODO: Figure out how to close modal */}
      {shouldShowQuoteForm &&
      <NewQuoteForm isModalOpen={shouldShowQuoteForm} setIsModalOpen={setShouldShowQuoteForm}/>}
      <ul>
        {quotes?.map(quote =>
          <li key={quote.id}>
            {quote.content}
          </li>
        )}
      </ul>
      </>
  )
}