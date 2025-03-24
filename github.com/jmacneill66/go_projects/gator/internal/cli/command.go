package cli

import "fmt"

// Command represents a CLI command with a name and arguments.
type Command struct {
	Name string
	Args []string
}

// Commands holds a map of command names to handler functions.
type Commands struct {
	handlers map[string]func(*State, Command) error
}

// Register registers a command with its handler function.
func (c *Commands) Register(name string, f func(*State, Command) error) {
	if c.handlers == nil {
		c.handlers = make(map[string]func(*State, Command) error)
	}
	c.handlers[name] = f
}

// Run executes a command if it exists.
func (c *Commands) Run(s *State, cmd Command) error {
	handler, exists := c.handlers[cmd.Name]
	if !exists {
		return fmt.Errorf("unknown command: %s", cmd.Name)
	}
	return handler(s, cmd)
}
