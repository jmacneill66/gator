package cli

import (
	"context"
	"errors"
	"fmt"
	"github.com/jmacneill66/go_projects/gator/internal/database"
	"log"
	"strconv"
	"time"

	"github.com/google/uuid"
)

// HandlerLogin handles the "login" command.
func HandlerLogin(s *State, cmd Command) error {
	if len(cmd.Args) == 0 {
		return errors.New("username is required")
	}

	username := cmd.Args[0]

	// GetUser
	user, err := s.DB.GetUser(context.Background(), username)
	if err != nil {
		fmt.Printf("Error: user '%s' does not exist.\n", username)
		return fmt.Errorf("user '%s' does not exist", username)
	}
	// Correctly use the user variable
	fmt.Printf("User found: ID=%s, Name=%s, CreatedAt=%v\n", user.ID, user.Name, user.CreatedAt)
	// Set user in config
	if err := s.Cfg.SetUser(username); err != nil {
		return fmt.Errorf("failed to update config: %w", err)
	}

	fmt.Printf("Logged in as '%s'.\n", username)
	return nil
}

// HandlerRegister handles the "register" command.
func HandlerRegister(s *State, cmd Command) error {
	if len(cmd.Args) == 0 {
		return errors.New("username is required")
	}

	username := cmd.Args[0]

	// Generate a new UUID
	userID := uuid.New()

	// Get the current timestamp
	now := time.Now()

	// Create the user in the database
	_, err := s.DB.CreateUser(context.Background(), database.CreateUserParams{
		ID:        userID,
		Name:      username,
		CreatedAt: now,
		UpdatedAt: now,
	})

	if err != nil {
		return fmt.Errorf("failed to register user: %w", err)
	}

	// Set the current user in config
	if err := s.Cfg.SetUser(username); err != nil {
		return fmt.Errorf("failed to update config: %w", err)
	}

	// Log user details for debugging
	log.Printf("User registered: ID=%s, Name=%s, CreatedAt=%s", userID, username, now)

	fmt.Printf("User '%s' has been registered.\n", username)
	return nil
}

// HandlerReset deletes all users from the database.
func HandlerReset(s *State, cmd Command) error {
	fmt.Println("⚠️  WARNING: This will delete all users from the database!")

	/* Confirm deletion (optional)
	var confirm string
	fmt.Print("Type 'yes' to proceed: ")
	fmt.Scanln(&confirm)
	if confirm != "yes" {
		fmt.Println("Reset operation canceled.")
		return nil
	}*/

	// Execute the DeleteAllUsers query
	err := s.DB.DeleteAllUsers(context.Background())
	if err != nil {
		fmt.Println("Error: Failed to reset the database.")
		return fmt.Errorf("failed to delete users: %w", err)
	}

	fmt.Println("✅ All users have been deleted.")
	return nil
}

// HandlerUsers fetches and prints all users.
func HandlerUsers(s *State, cmd Command) error {
	// Get all users from the database
	users, err := s.DB.GetUsers(context.Background())
	if err != nil {
		return fmt.Errorf("failed to fetch users: %w", err)
	}

	// Get the current user from config
	currentUser := s.Cfg.CurrentUserName

	// Print users
	for _, user := range users {
		if user.Name == currentUser {
			fmt.Printf("* %s (current)\n", user.Name)
		} else {
			fmt.Printf("* %s\n", user.Name)
		}
	}

	return nil
}

// HandlerAgg fetches and prints an RSS feed.
func HandlerAgg(s *State, cmd Command) error {
	/*feedURL := "https://www.wagslane.dev/index.xml"

	fmt.Println("Fetching RSS feed...")
	feed, err := rss.FetchFeed(context.Background(), feedURL)
	if err != nil {
		return fmt.Errorf("failed to fetch feed: %w", err)
	}
	// Print parsed feed
	fmt.Println("\n=== RSS Feed ===")
	fmt.Printf("Title: %s\n", feed.Channel.Title)
	fmt.Printf("Link: %s\n", feed.Channel.Link)
	fmt.Printf("Description: %s\n", feed.Channel.Description)

	fmt.Println("\n=== Items ===")
	for _, item := range feed.Channel.Item {
		fmt.Printf("- %s\n  %s\n  %s\n  Description: %s\n\n",
			item.Title, item.Link, item.PubDate, item.Description)
	}
	log.Println("RSS feed successfully fetched and parsed.")
	return nil */

	// Ensure interval is provided
	if len(cmd.Args) < 1 {
		return errors.New("usage: agg <time_between_reqs> (e.g., 1s, 1m, 1h)")
	}
	// Parse interval
	timeBetweenRequests, err := time.ParseDuration(cmd.Args[0])
	if err != nil {
		return fmt.Errorf("invalid duration format: %w", err)
	}
	fmt.Printf("⏳ Collecting feeds every %s\n", timeBetweenRequests)
	// Create ticker for periodic execution
	ticker := time.NewTicker(timeBetweenRequests)
	defer ticker.Stop()
	// Run immediately, then on each tick
	for {
		ScrapeFeeds(s)
		<-ticker.C
	}
}

// HandlerFeeds prints all RSS feeds from the database.
func HandlerFeeds(s *State, cmd Command) error {
	// Fetch all feeds with user info
	feeds, err := s.DB.GetFeedsWithUser(context.Background())
	if err != nil {
		return fmt.Errorf("failed to fetch feeds: %w", err)
	}

	// Print feeds
	fmt.Println("\n=== Feeds ===")
	for _, feed := range feeds {
		fmt.Printf("- %s\n  URL: %s\n  Added by: %s\n\n", feed.Name, feed.Url, feed.UserName)
	}

	return nil
}

// HandlerFollow allows a user to follow a feed.
func HandlerFollow(s *State, cmd Command, user database.User) error {
	// Ensure feed URL is provided
	if len(cmd.Args) < 1 {
		return errors.New("usage: follow <feed_url>")
	}
	feedURL := cmd.Args[0]

	// Get the feed by URL
	feed, err := s.DB.GetFeedByUrl(context.Background(), feedURL)
	if err != nil {
		return fmt.Errorf("no feed found with URL: %s", feedURL)
	}
	// Create feed follow record
	followID := uuid.New()
	now := time.Now()

	follow, err := s.DB.CreateFeedFollow(context.Background(), database.CreateFeedFollowParams{
		ID:        followID,
		CreatedAt: now,
		UpdatedAt: now,
		UserID:    user.ID,
		FeedID:    feed.ID,
	})
	if err != nil {
		return fmt.Errorf("failed to follow feed: %w", err)
	}
	// Print follow confirmation
	fmt.Printf("✅ %s is now following '%s'\n", follow.UserName, follow.FeedName)
	return nil
}

// HandlerFollowing prints all feeds a user is following.
func HandlerFollowing(s *State, cmd Command, user database.User) error {
	// Get the feed follows for the user
	follows, err := s.DB.GetFeedFollowsForUser(context.Background(), s.Cfg.CurrentUserName)
	if err != nil {
		return fmt.Errorf("failed to fetch followed feeds: %w", err)
	}
	// Print followed feeds
	fmt.Println("\n=== Following Feeds ===")
	for _, follow := range follows {
		fmt.Printf("- %s\n", follow.FeedName)
	}
	return nil
}

// HandlerAddFeed adds a new RSS feed and follows it.
func HandlerAddFeed(s *State, cmd Command, user database.User) error {
	// Ensure name and URL are provided
	if len(cmd.Args) < 2 {
		return errors.New("usage: addfeed <name> <url>")
	}
	feedName := cmd.Args[0]
	feedURL := cmd.Args[1]

	// Create new feed
	feedID := uuid.New()
	now := time.Now()
	feed, err := s.DB.CreateFeed(context.Background(), database.CreateFeedParams{
		ID:        feedID,
		CreatedAt: now,
		UpdatedAt: now,
		Name:      feedName,
		Url:       feedURL,
		UserID:    user.ID,
	})
	if err != nil {
		return fmt.Errorf("failed to create feed: %w", err)
	}
	// Auto-follow the feed
	followID := uuid.New()
	_, err = s.DB.CreateFeedFollow(context.Background(), database.CreateFeedFollowParams{
		ID:        followID,
		CreatedAt: now,
		UpdatedAt: now,
		UserID:    user.ID,
		FeedID:    feed.ID,
	})
	if err != nil {
		return fmt.Errorf("failed to auto-follow feed: %w", err)
	}
	// Print confirmation
	fmt.Println("✅ Feed added and followed successfully:")
	fmt.Printf("- Name: %s\n", feed.Name)
	fmt.Printf("- URL: %s\n", feed.Url)
	fmt.Printf("- User: %s\n", user.Name)
	return nil
}

// HandlerUnfollow allows a user to unfollow a feed.
func HandlerUnfollow(s *State, cmd Command, user database.User) error {
	// Ensure feed URL is provided
	if len(cmd.Args) < 1 {
		return errors.New("usage: unfollow <feed_url>")
	}
	feedURL := cmd.Args[0]

	// Get the feed by URL
	feed, err := s.DB.GetFeedByUrl(context.Background(), feedURL)
	if err != nil {
		return fmt.Errorf("no feed found with URL: %s", feedURL)
	}

	// Create params for DeleteFeedFollow
	params := database.DeleteFeedFollowParams{
		Name: user.Name,
		Url:  feedURL,
	}

	// Delete feed follow record
	err = s.DB.DeleteFeedFollow(context.Background(), params)
	if err != nil {
		return fmt.Errorf("failed to unfollow feed: %w", err)
	}

	// Print unfollow confirmation
	fmt.Printf("✅ %s has unfollowed '%s'\n", user.Name, feed.Name)
	return nil
}

// HandlerBrowse prints recent posts for a user.
func HandlerBrowse(s *State, cmd Command, user database.User) error {
	// Default limit to 2 if not provided
	limit := 2
	if len(cmd.Args) > 0 {
		parsedLimit, err := strconv.Atoi(cmd.Args[0])
		if err != nil || parsedLimit < 1 {
			return errors.New("invalid limit; must be a positive integer")
		}
		limit = parsedLimit
	}

	// Fetch posts using the struct parameter
	posts, err := s.DB.GetPostsForUser(context.Background(), database.GetPostsForUserParams{
		Name:  user.Name,
		Limit: int32(limit),
	})
	if err != nil {
		return fmt.Errorf("failed to fetch posts: %w", err)
	}

	// Print posts
	fmt.Println("\n📌 Recent Posts:")
	for _, post := range posts {
		fmt.Printf("- %s\n  📅 %s\n  🔗 %s\n\n", post.Title, post.PublishedAt.Time.Format(time.RFC822), post.Url)
	}
	return nil
}
