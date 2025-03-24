package config

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

// Config struct represents the JSON config structure.
type Config struct {
	CurrentUserName string `json:"current_user_name"`
	DBUrl           string `json:"db_url"`
}

// File constants
const configFileName = ".gatorconfig.json"

// getConfigFilePath returns the config file path in the HOME directory.
func getConfigFilePath() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("failed to get home directory: %w", err)
	}
	return filepath.Join(homeDir, configFileName), nil
}

// Read reads and returns the configuration.
func Read() (Config, error) {
	filePath, err := getConfigFilePath()
	if err != nil {
		return Config{}, err
	}

	file, err := os.Open(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return Config{}, nil // Return an empty config if the file doesn't exist.
		}
		return Config{}, fmt.Errorf("failed to open config file: %w", err)
	}
	defer file.Close()

	var cfg Config
	if err := json.NewDecoder(file).Decode(&cfg); err != nil {
		return Config{}, fmt.Errorf("failed to decode JSON: %w", err)
	}

	return cfg, nil
}

// write writes the Config struct to the JSON file.
func write(cfg Config) error {
	filePath, err := getConfigFilePath()
	if err != nil {
		return err
	}

	file, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("failed to create config file: %w", err)
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(cfg); err != nil {
		return fmt.Errorf("failed to encode JSON: %w", err)
	}

	return nil
}

// SetUser updates the current_user_name without overwriting db_url.
func (cfg *Config) SetUser(userName string) error {
	cfg.CurrentUserName = userName
	return write(*cfg)
}
