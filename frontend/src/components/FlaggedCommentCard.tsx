// frontend/src/components/FlaggedCommentCard.tsx
import axios from "axios";
import type { Comment } from "../types";

type Props = {
  comment: Comment;
  postId: number;
  onRemoved: (commentId: number, postId: number) => void;
};

export const FlaggedCommentCard = ({ comment, postId, onRemoved }: Props) => {
  const handleUnflag = () => {
    axios
      .patch(`/comments/${comment.id}/unflag/`, { flagged: false })
      .then(() => onRemoved(comment.id, postId));
  };

  const handleDelete = () => {
    if (!window.confirm("Delete this comment permanently?")) return;
    axios.delete(`/comments/${comment.id}/unflag/`).then(() => {
      onRemoved(comment.id, postId);
    });
  };

  return (
    <div
      style={{
        border: "2px solid red",
        padding: "8px",
        margin: "8px 0",
        borderRadius: "4px",
      }}
    >
      <p>
        <strong>{comment.author}</strong>: {comment.text}
      </p>
      <button onClick={handleUnflag}>Unflag</button>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
};