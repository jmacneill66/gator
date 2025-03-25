package main

import (
	//"context"
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/lib/pq" // PostgreSQL driver
	//"github.com/google/uuid"

	"github.com/jmacneill66/go_projects/gator/internal/cli"
	"github.com/jmacneill66/go_projects/gator/internal/config"
	"github.com/jmacneill66/go_projects/gator/internal/database"
)

func main() {
	// Read the config file
	cfg, err := config.Read()
	if err != nil {
		log.Fatalf("Error reading config: %v", err)
	}

	// Ensure DB URL is set
	if cfg.DBUrl == "" {
		log.Fatalf("Error: Database URL is not set in config.")
	}

	// Open database connection
	db, err := sql.Open("postgres", cfg.DBUrl)
	if err != nil {
		log.Fatalf("Error opening database: %v", err)
	}

	// Initialize database queries
	dbQueries := database.New(db)

	// Create a state struct holding the config
	state := &cli.State{
		DB:  dbQueries,
		Cfg: &cfg,
	}

	// Initialize the command registry
	commands := &cli.Commands{}
	commands.Register("login", cli.HandlerLogin)
	commands.Register("register", cli.HandlerRegister)
	commands.Register("reset", cli.HandlerReset)
	commands.Register("users", cli.HandlerUsers)
	commands.Register("agg", cli.HandlerAgg)
	commands.Register("feeds", cli.HandlerFeeds)
	commands.Register("addfeed", cli.MiddlewareLoggedIn(cli.HandlerAddFeed))
	commands.Register("follow", cli.MiddlewareLoggedIn(cli.HandlerFollow))
	commands.Register("following", cli.MiddlewareLoggedIn(cli.HandlerFollowing))
	commands.Register("unfollow", cli.MiddlewareLoggedIn(cli.HandlerUnfollow))
	commands.Register("browse", cli.MiddlewareLoggedIn(cli.HandlerBrowse))
	commands.Register("agg", cli.HandlerAgg)

	// Parse command-line arguments
	if len(os.Args) < 2 {
		fmt.Println("Error: not enough arguments provided.")
		os.Exit(1)
	}

	// Extract command name and arguments
	cmdName := os.Args[1]
	cmdArgs := os.Args[2:]

	// Create the command instance
	cmd := cli.Command{Name: cmdName, Args: cmdArgs}

	// Run the command
	if err := commands.Run(state, cmd); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}
