package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"net/http"
	"strings"
)

// Config contains application configuration
// Hardcoded credentials (security issue)
var Config = struct {
	APIKey    string
	SecretKey string
	Debug     bool
}{
	APIKey:    "1234567890abcdef",
	SecretKey: "super_secret_key",
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

// ProcessRequest processes an HTTP request with potential issues
func ProcessRequest(r *http.Request) map[string]string {
	// Unused variable (code quality issue)
	unusedVar := "This variable is never used"
	
	// Extract user data
	username := r.URL.Query().Get("username")
	password := r.URL.Query().Get("password") // Sensitive data in URL (security issue)
	
	// Insecure authentication (security issue)
	if username == "admin" && password == "admin123" {
		return map[string]string{
			"status": "authenticated",
			"role":   "admin",
		}
	}
	
	return map[string]string{
		"status": "unauthenticated",
	}
}

// FormatUserInput formats user input without proper sanitization
func FormatUserInput(input string) string {
	// No input sanitization (security issue)
	return "<div>" + input + "</div>" // Potential XSS vulnerability
}

// IsAdmin checks if a user is an admin with potential issues
func IsAdmin(user map[string]string) bool {
	// Potential nil pointer dereference (code quality issue)
	return strings.ToLower(user["role"]) == "admin"
}

// LoadUserData loads user data with potential path traversal vulnerability
func LoadUserData(userID string) {
	// Path traversal vulnerability (security issue)
	filename := fmt.Sprintf("data/users/%s.json", userID)
	fmt.Println("Loading user data from:", filename)
}

// VerifySignature verifies a signature with weak comparison
func VerifySignature(signature, expectedSignature string) bool {
	// Timing attack vulnerability (security issue)
	return signature == expectedSignature
}
