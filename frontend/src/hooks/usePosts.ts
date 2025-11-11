// frontend/src/hooks/usePosts.ts
import { useState, useEffect } from "react";
import axios from "axios";
import type { Post, Comment } from "../types";

export const usePosts = () => {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    axios.get("/posts/").then((res) => {
      setPosts(res.data);
    });
  }, []);

  const addPost = (newPost: Post) => {
    setPosts((prev) => [newPost, ...prev]);
  };

  const addComment = (postId: number, comment: Comment) => {
    if (comment.flagged) return;
    setPosts((prev) =>
      prev.map((p) =>
        p.id === postId
          ? { ...p, comments: [...(p.comments || []), comment] }
          : p
      )
    );
  };

  return { posts, addPost, addComment };
};