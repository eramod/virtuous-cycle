import { Outlet, Link, useLoaderData } from "react-router-dom";
import LogoutForm from "../components/logout-form";

export type User = {
  id: string,
  email: string,
} | null;

export default function Root() {
  // TODO: Figure out React Router types
  const user: User = useLoaderData() as any as User;

  return (
    <>
      <nav>
        <ul>
          {!user &&
            <li>
              <Link to={'register'}>Sign up</Link>
            </li>}

          {!user &&
            <li>
              <Link to={'login'}>Login</Link>
            </li>
          }

          {user &&
            <li>
              <LogoutForm />
          </li>}
          <li>
            <Link to={'quotes'}>Quotes</Link>
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
