package cli

import (
	"context"
	"database/sql"
	"fmt"
	"gator/internal/database"
	"gator/internal/rss"
	"log"
	"time"

	"github.com/google/uuid"
)

// ScrapeFeeds fetches RSS feeds and prints post titles.
func ScrapeFeeds(s *State) {
	ctx := context.Background()

	// Get the next feed to fetch
	feed, err := s.DB.GetNextFeedToFetch(ctx)
	if err != nil {
		log.Println("No feeds available to fetch.")
		return
	}

	fmt.Printf("\n🔄 Fetching feed: %s (%s)\n", feed.Name, feed.Url)

	// Mark feed as fetched
	err = s.DB.MarkFeedFetched(ctx, feed.ID)
	if err != nil {
		log.Printf("Error marking feed as fetched: %v\n", err)
		return
	}

	// Fetch and parse the feed
	rssFeed, err := rss.FetchFeed(ctx, feed.Url)
	if err != nil {
		log.Printf("Error fetching RSS feed: %v\n", err)
		return
	}
	/*
		// Print post titles
		fmt.Println("\n📢 Latest Posts:")
		for _, item := range rssFeed.Channel.Item {
			fmt.Printf("- %s\n", item.Title)
		} */

	// Save posts
	for _, item := range rssFeed.Channel.Item {
		// Parse published_at
		publishedAt, err := time.Parse(time.RFC1123, item.PubDate)
		if err != nil {
			log.Printf("Error parsing publish date for %s: %v\n", item.Title, err)
			publishedAt = time.Now() // Default to now if parsing fails
		}

		// Create post
		postID := uuid.New()
		now := time.Now()

		var description sql.NullString
		if item.Description != "" {
			description = sql.NullString{String: item.Description, Valid: true}
		} else {
			description = sql.NullString{Valid: false}
		}

		err = s.DB.CreatePost(ctx, database.CreatePostParams{
			ID:          postID,
			CreatedAt:   now,
			UpdatedAt:   now,
			Title:       item.Title,
			Url:         item.Link,
			Description: description,
			PublishedAt: sql.NullTime{Time: publishedAt, Valid: true},
			FeedID:      feed.ID,
		})

		if err != nil {
			log.Printf("Error inserting post '%s': %v\n", item.Title, err)
		}
	}
}
