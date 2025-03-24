package cli

import (
	"gator/internal/config"
	"gator/internal/database"
)

// State struct holds a pointer to the Config.
type State struct {
	Cfg *config.Config
	DB  *database.Queries
}
