// frontend/src/components/CreatePostForm.tsx
import { useState, type FormEvent } from "react";  // type-only import
import axios from "axios";
import type { Post } from "../types";

type Props = {
  onPostCreated: (post: Post) => void;
};

export const CreatePostForm = ({ onPostCreated }: Props) => {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    axios
      .post<Post>("/posts/create/", { title, body })
      .then((res) => {
        const newPost = { ...res.data, comments: res.data.comments ?? [] };
        onPostCreated(newPost);
        setTitle("");
        setBody("");
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Post title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Post body"
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button type="submit">Create Post</button>
    </form>
  );
};