// frontend/src/hooks/useFlaggedComments.ts
import { useState, useEffect } from "react";
import axios from "axios";
import type { Post, Comment } from "../types";

export const useFlaggedComments = () => {
  const [posts, setPosts] = useState<readonly Post[]>([]);

  useEffect(() => {
    axios.get<Comment[]>("/flagged-comments/").then((res) => {
      const postMap = new Map<number, Post & { comments: Comment[] }>();

      res.data.forEach((comment) => {
        if (!postMap.has(comment.post)) {
          postMap.set(comment.post, {
            id: comment.post,
            title: `Post #${comment.post}`,
            body: "",
            comments: [],
          });
        }

        const entry = postMap.get(comment.post)!;
        entry.comments.push(comment);
      });

      const postIds = Array.from(postMap.keys());
      if (postIds.length === 0) {
        setPosts([]);
        return;
      }

      axios.get<Post[]>("/posts/").then((allPostsRes) => {
        const allPosts = allPostsRes.data;
        postIds.forEach((id) => {
          const fullPost = allPosts.find((p) => p.id === id);
          if (fullPost) {
            const entry = postMap.get(id)!;
            entry.title = fullPost.title;
            entry.body = fullPost.body;
          }
        });
        setPosts(Array.from(postMap.values()));
      });
    });
  }, []);

  const removeComment = (commentId: number, postId: number) => {
    setPosts((prev) =>
      prev.map((p) =>
        p.id === postId
          ? { ...p, comments: (p.comments ?? []).filter((c) => c.id !== commentId) }
          : p
      )
    );
  };

  return { posts, removeComment };
};