-- name: CreateUser :one
INSERT INTO users (id, created_at, updated_at, name)
VALUES (
    $1,
    $2,
    $3,
    $4
)
RETURNING *;

-- name: GetUser :one
SELECT * FROM users
WHERE name = $1
LIMIT 1;

-- name: GetUsers :many
SELECT id, created_at, updated_at, name FROM users;

-- name: DeleteAllUsers :exec
DELETE FROM users;

-- name: CreateFeed :one
INSERT INTO feeds (id, created_at, updated_at, name, url, user_id)
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING id, created_at, updated_at, name, url, user_id;

-- name: GetFeedsWithUser :many
SELECT feeds.id, feeds.created_at, feeds.updated_at, feeds.name, feeds.url, users.name AS user_name
FROM feeds
JOIN users ON feeds.user_id = users.id;

-- name: CreateFeedFollow :one
WITH inserted_feed_follow AS (
    INSERT INTO feed_follows (id, created_at, updated_at, user_id, feed_id)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, created_at, updated_at, user_id, feed_id
)
SELECT
    inserted_feed_follow.id,
    inserted_feed_follow.created_at,
    inserted_feed_follow.updated_at,
    users.name AS user_name,
    feeds.name AS feed_name
FROM inserted_feed_follow
JOIN users ON inserted_feed_follow.user_id = users.id
JOIN feeds ON inserted_feed_follow.feed_id = feeds.id;

-- name: GetFeedByUrl :one
SELECT id, name FROM feeds WHERE url = $1 LIMIT 1;

-- name: GetFeedFollowsForUser :many
SELECT feed_follows.id, feed_follows.created_at, feed_follows.updated_at, users.name AS user_name, feeds.name AS feed_name
FROM feed_follows
JOIN users ON feed_follows.user_id = users.id
JOIN feeds ON feed_follows.feed_id = feeds.id
WHERE users.name = $1;

-- name: DeleteFeedFollow :exec
DELETE FROM feed_follows 
WHERE user_id = (SELECT id FROM users WHERE users.name = $1)
AND feed_id = (SELECT id FROM feeds WHERE url = $2);

-- name: MarkFeedFetched :exec
UPDATE feeds 
SET last_fetched_at = now(), updated_at = now() 
WHERE id = $1;

-- name: GetNextFeedToFetch :one
SELECT id, url, name 
FROM feeds 
ORDER BY last_fetched_at NULLS FIRST, updated_at ASC 
LIMIT 1;

-- name: CreatePost :exec
INSERT INTO posts (id, created_at, updated_at, title, url, description, published_at, feed_id)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
ON CONFLICT (url) DO NOTHING;

-- name: GetPostsForUser :many
SELECT posts.id, posts.created_at, posts.updated_at, posts.title, posts.url, posts.description, posts.published_at, posts.feed_id
FROM posts
JOIN feed_follows ON posts.feed_id = feed_follows.feed_id
JOIN users ON feed_follows.user_id = users.id
WHERE users.name = $1
ORDER BY posts.published_at DESC
LIMIT $2;