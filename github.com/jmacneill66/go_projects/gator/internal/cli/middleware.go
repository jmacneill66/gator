package cli

import (
	"context"
	"errors"
	"fmt"

	"github.com/jmacneill66/go_projects/gator/internal/database"
)

// middlewareLoggedIn ensures a user is logged in before executing a command.
func MiddlewareLoggedIn(handler func(s *State, cmd Command, user database.User) error) func(*State, Command) error {
	return func(s *State, cmd Command) error {
		// Ensure a user is logged in
		if s.Cfg.CurrentUserName == "" {
			return errors.New("no user logged in. Use 'login' first")
		}

		// Fetch the current user from the database
		user, err := s.DB.GetUser(context.Background(), s.Cfg.CurrentUserName)
		if err != nil {
			return fmt.Errorf("failed to fetch user: %w", err)
		}

		// Call the wrapped handler with the user
		return handler(s, cmd, user)
	}
}
