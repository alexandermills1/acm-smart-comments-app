// frontend/src/components/AddCommentForm.tsx
import { useState } from "react";
import axios from "axios";
import type { Comment } from "../types";

type Props = {
  postId: number;
  onCommentAdded: (c: Comment) => void;
  onCancel: () => void;
};

export const AddCommentForm = ({
  postId,
  onCommentAdded,
  onCancel,
}: Props) => {
  const [author, setAuthor] = useState("");
  const [text, setText] = useState("");

  const handleSubmit = () => {
    if (!author.trim() || !text.trim()) return;
    axios
      .post<Comment>(`/posts/${postId}/comments/`, { author, text })
      .then((res) => {
        const c = res.data;
        if (!c.flagged) onCommentAdded(c);  // Now valid
        onCancel();
      });
  };

  return (
    <>
      <input
        type="text"
        placeholder="Your name"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
      />
      <textarea
        placeholder="Write a comment..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};