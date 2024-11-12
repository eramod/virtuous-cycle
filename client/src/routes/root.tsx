export default function Root() {
  return (
    <>
      <nav>
        <ul>
          <li>
            <a href={`/contacts/1`}>Login</a>
          </li>
          <li>
            <a href={`/contacts/2`}>Sign up</a>
          </li>
        </ul>
      </nav>
      <main>
        <h1>Welcome to Virtuous Cycle!</h1>
        {/* TODO: Add Login route here */}
      </main>
      <div id="detail"></div>
    </>
  );
}
