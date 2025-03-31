package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"strings"
)

// Config contains application configuration
// Hardcoded credentials (security issue)
var Config = struct {
	APIKey    string
	SecretKey string
	Debug     bool
}{
	APIKey:    "1234567890abcdef", // #nosec - Intentional security issue
	SecretKey: "super_secret_key", // #nosec - Intentional security issue
	Debug:     true,
}

// GenerateRandomToken generates a random token with weak randomness
func GenerateRandomToken(length int) string {
	// Using math/rand instead of crypto/rand (security issue)
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	result := make([]byte, length)
	
	for i := range result {
		// Using weak randomness (security issue)
		n, _ := rand.Int(rand.Reader, big.NewInt(int64(len(charset))))
		result[i] = charset[n.Int64()]
	}
	
	return string(result)
}

// ValidateInput validates user input with potential issues
func ValidateInput(input string) bool {
	// Redundant condition (code quality issue)
	if len(input) > 0 && input != "" {
		return true
	}
	
	return false
}

// FormatUserInput formats user input without proper sanitization
func FormatUserInput(input string) string {
	// No input sanitization (security issue)
	return "<div>" + input + "</div>" // #nosec - Intentional security issue
}

// IsAdmin checks if a user is an admin with potential issues
func IsAdmin(user map[string]string) bool {
	// Potential nil pointer dereference (code quality issue)
	return strings.ToLower(user["role"]) == "admin" // #nosec - Intentional security issue
}

// LoadUserData loads user data with potential path traversal vulnerability
func LoadUserData(userID string) {
	// Path traversal vulnerability (security issue)
	filename := fmt.Sprintf("data/users/%s.json", userID) // #nosec - Intentional security issue
	fmt.Println("Loading user data from:", filename)
}

// VerifySignature verifies a signature with weak comparison
func VerifySignature(signature, expectedSignature string) bool {
	// Timing attack vulnerability (security issue)
	return signature == expectedSignature // #nosec - Intentional security issue
}
