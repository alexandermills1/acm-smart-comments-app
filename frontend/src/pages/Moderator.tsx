// frontend/src/pages/Moderator.tsx
import { useFlaggedComments } from "../hooks/useFlaggedComments";
import { FlaggedCommentCard } from "../components/FlaggedCommentCard";

const Moderator = () => {
  const { posts, removeComment } = useFlaggedComments();

  return (
    <>
      <h1>Flagged for Review</h1>
      <p>Comments flagged by users or moderators appear here.</p>

      {posts.length === 0 ? (
        <div>
          <em>No flagged comments at this time.</em>
        </div>
      ) : (
        <div>
          {posts.map((post) => (
            <div key={post.id}>
              <h3>{post.title}</h3>
              {(post.comments ?? []).map((comment) => (
                <FlaggedCommentCard
                  key={comment.id}
                  comment={comment}
                  postId={post.id}
                  onRemoved={removeComment}
                />
              ))}
            </div>
          ))}
        </div>
      )}
    </>
  );
};

export default Moderator;