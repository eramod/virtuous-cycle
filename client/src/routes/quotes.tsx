import { useEffect, useState } from "react"
import NewQuoteForm from "../components/new-quote-form";

interface Quote {
  content: string,
  attribution?: string | null
}

export default function Quotes() {
  const [quotes, setQuotes] = useState<Quote[] | null>(null);
  const [shouldShowQuoteForm, setShouldShowQuoteForm] = useState(false)

  function handleClick(event: Event) {
    event.preventDefault();
    setShouldShowQuoteForm(!shouldShowQuoteForm);
  }

  useEffect(() => {
    fetch('http://localhost:5001/api/quotes')
      .then(res => res.json())
      .then(json => {
        console.log("Response: ", json)
        setQuotes(json.body)
      })

  }, [setQuotes])

  return (
    <>
      <button type="button" onClick={handleClick}>Add a quote</button>
      {shouldShowQuoteForm ?
        <NewQuoteForm /> :
        'Quote form hidden'}
      <ul>
        {quotes?.map(quote =>
          <li>{quote.content}</li>
        )}
      </ul>
      </>
  )
}