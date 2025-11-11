// frontend/src/types/index.ts
export interface Comment {
  id: number;
  post: number;
  author: string;
  text: string;
  created_at: string;
  flagged: boolean;
}

export interface Post {
  id: number;
  title: string;
  body: string;
  comments?: Comment[];
}