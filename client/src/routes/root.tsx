import { Outlet, Link } from "react-router-dom";

export default function Root() {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to={`register`}>Sign up</Link>
          </li>
          <li>
            <Link to={`login`}>Login</Link>
          </li>
        </ul>
      </nav>
      <main>
        <Outlet />
      </main>
      <div id="detail"></div>
    </>
  );
}
