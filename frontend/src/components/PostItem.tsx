// frontend/src/components/PostItem.tsx
import { useState } from "react";
import type { Post, Comment } from "../types";  // <-- Add Comment
import { AddCommentForm } from "./AddCommentForm";

type Props = {
  post: Post;
  onCommentAdded: (postId: number, c: Comment) => void;
};

export const PostItem = ({ post, onCommentAdded }: Props) => {
  const [showForm, setShowForm] = useState(false);
  const visible = (post.comments ?? []).filter((c) => !c.flagged);  // Now valid

  return (
    <div className="post-item">
      <h2>{post.title}</h2>
      <p>{post.body}</p>

      <div>
        <strong>Comments:</strong>
        {visible.length === 0 ? (
          <p>No comments yet.</p>
        ) : (
          <ul>
            {visible.map((c) => (
              <li key={c.id}>
                <strong>{c.author}</strong>: {c.text}
              </li>
            ))}
          </ul>
        )}
      </div>

      {showForm ? (
        <AddCommentForm
          postId={post.id}
          onCommentAdded={(c) => onCommentAdded(post.id, c)}
          onCancel={() => setShowForm(false)}
        />
      ) : (
        <button onClick={() => setShowForm(true)}>Add Comment</button>
      )}

      <hr />
    </div>
  );
};