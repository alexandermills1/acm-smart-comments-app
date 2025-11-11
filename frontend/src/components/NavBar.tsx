// frontend/src/components/NavBar.tsx
import { Link } from "react-router-dom";

export const NavBar = () => {
  return (
    <nav>
      <div>
        <Link to="/">HOME</Link>
        <Link to="/moderator">Moderator</Link>
      </div>
    </nav>
  );
};