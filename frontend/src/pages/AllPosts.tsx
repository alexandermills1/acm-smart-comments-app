// frontend/src/pages/AllPosts.tsx
import { CreatePostForm } from "../components/CreatePostForm";
import { PostItem } from "../components/PostItem";
import { usePosts } from "../hooks/usePosts";

const AllPosts = () => {
  const { posts, addPost, addComment } = usePosts();

  return (
    <>
      <h1>Create Post</h1>
      <CreatePostForm onPostCreated={addPost} />

      <h1>All Posts</h1>
      <div>
        {posts.map((post) => (
          <PostItem
            key={post.id}
            post={post}
            onCommentAdded={addComment}
          />
        ))}
      </div>
    </>
  );
};

export default AllPosts;