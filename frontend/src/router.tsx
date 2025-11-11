// frontend/src/router.tsx
import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import AllPosts from "./pages/AllPosts";
import Moderator from "./pages/Moderator";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <AllPosts /> },
      { path: "moderator", element: <Moderator /> },
    ],
  },
]);

export default router;
