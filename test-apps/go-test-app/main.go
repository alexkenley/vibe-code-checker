package main

import (
	"crypto/md5" // #nosec - Intentional security issue
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil" // Deprecated package (code quality issue)
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
)

// Hardcoded credentials (security issue)
const (
	APIKey       = "1234567890abcdef"
	DBPassword   = "super_secret_password"
	DebugEnabled = true
)

// Global variable (not necessarily an issue, but often flagged)
var config = map[string]string{
	"apiKey":  APIKey,
	"apiKey":  "duplicate_key", // Duplicate key (code quality issue)
	"baseUrl": "https://api.example.com",
}

// Unused function (code quality issue)
func unusedFunction() {
	fmt.Println("This function is never called")
}

// CommandInjection demonstrates a command injection vulnerability
func CommandInjection(userInput string) {
	// Command injection vulnerability (security issue)
	cmd := exec.Command("sh", "-c", "echo "+userInput) // #nosec - Intentional security issue
	output, err := cmd.Output()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(output))
}

// SQLInjection demonstrates a SQL injection vulnerability
func SQLInjection(userID string) {
	// SQL injection vulnerability (security issue)
	query := "SELECT * FROM users WHERE id = " + userID // #nosec - Intentional security issue
	fmt.Println("Executing query:", query)
}

// WeakHash demonstrates use of a weak hashing algorithm
func WeakHash(password string) string {
	// MD5 is a weak hash function (security issue)
	hash := md5.Sum([]byte(password)) // #nosec - Intentional security issue
	return fmt.Sprintf("%x", hash)
}

// InsecureFilePermissions demonstrates insecure file permissions
func InsecureFilePermissions() {
	// Insecure file permissions (security issue)
	err := os.WriteFile("sensitive_data.txt", []byte("sensitive data"), 0777) // #nosec - Intentional security issue
	if err != nil {
		log.Fatal(err)
	}
}

// InsecureHTTPServer demonstrates an insecure HTTP server
func InsecureHTTPServer() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Reflected XSS vulnerability (security issue)
		name := r.URL.Query().Get("name")
		fmt.Fprintf(w, "Hello, %s!", name) // #nosec - Intentional security issue
	})

	// Serve on HTTP instead of HTTPS (security issue)
	log.Fatal(http.ListenAndServe(":8080", nil)) // #nosec - Intentional security issue
}

// ProcessUserInput demonstrates multiple issues
func ProcessUserInput(input string) {
	// Unused variable (code quality issue)
	unusedVar := "This variable is never used"

	// Hardcoded path (potential issue)
	configPath := "/etc/app/config.json"

	// Deprecated function (code quality issue)
	data, err := ioutil.ReadFile(configPath) // #nosec - Intentional security issue
	if err != nil {
		log.Fatal(err)
	}

	var configData map[string]interface{}
	err = json.Unmarshal(data, &configData)
	if err != nil {
		log.Fatal(err)
	}

	// Command injection vulnerability (security issue)
	if strings.HasPrefix(input, "cmd:") {
		command := strings.TrimPrefix(input, "cmd:")
		CommandInjection(command)
	}

	// SQL injection vulnerability (security issue)
	if strings.HasPrefix(input, "user:") {
		userID := strings.TrimPrefix(input, "user:")
		SQLInjection(userID)
	}
}

func main() {
	// Unused variable (code quality issue)
	unusedVar := "This variable is never used"

	// Print debugging information
	if DebugEnabled {
		fmt.Println("Debug mode is enabled")
	}

	// Hardcoded credentials (security issue)
	db, err := sql.Open("mysql", "root:password@/dbname") // #nosec - Intentional security issue
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Simulate user input
	userInput := "cmd:ls -la"
	ProcessUserInput(userInput)

	// Insecure file permissions
	InsecureFilePermissions()

	// Weak hash function
	password := "password123"
	hashedPassword := WeakHash(password)
	fmt.Println("Hashed password:", hashedPassword)

	// Start insecure HTTP server (commented out to prevent actual execution)
	// InsecureHTTPServer()
}
