package cli

import (
	"github.com/jmacneill66/go_projects/gator/internal/config"
	"github.com/jmacneill66/go_projects/gator/internal/database"
)

// State struct holds a pointer to the Config.
type State struct {
	Cfg *config.Config
	DB  *database.Queries
}
