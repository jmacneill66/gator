Gator - A CLI RSS Feed Aggregator

Gator is a command-line tool that fetches RSS feeds, stores posts in a PostgreSQL database, and displays them in a structured format. It allows users to follow feeds, browse recent posts, and manage their subscriptions efficiently.
📋 Requirements

    Go 1.18+

    PostgreSQL 13+

    Goose (for database migrations)

🛠 Installation

The recommended way to install Gator is via go install:

go install github.com/jmacneill66/gator@latest

This will install the gator binary in your $GOPATH/bin, making it available system-wide.
⚙️ Database Setup

Before using Gator, you must initialize the database.
1️⃣ Install Goose (if not installed)

Goose is a database migration tool. Install it using:

go install github.com/pressly/goose/v3/cmd/goose@latest

2️⃣ Create the Database

Ensure PostgreSQL is running, then create the gator database:

createdb gator

3️⃣ Run Migrations

Navigate to the gator project directory and run:

goose -dir sql/schema postgres "postgres://username:password@localhost:5432/gator?sslmode=disable" up

Replace username and password with your PostgreSQL credentials.

This command applies database migrations, creating necessary tables.
⚙️ Configuration

Before running the program, set up the config file:

1️⃣ Create the config file:

touch ~/.gatorconfig.json

2️⃣ Edit ~/.gatorconfig.json:

{
  "db_url": "postgres://username:password@localhost:5432/gator",
  "current_user_name": ""
}

Replace username, password, and localhost:5432 with your PostgreSQL details.
🚀 Running the Program
🔹 Production Mode

Once installed with go install, run Gator like this:

gator <command> [args]

Example:

gator register alice
gator login alice

🔹 Development Mode

If you're working on the project locally, use:

go run . <command> [args]

Example:

go run . register alice
go run . login alice

    Important: go run . is for development only. Use gator for production.

🔧 Available Commands
Command Description
register <name> Register a new user
login <name> Log in as a user
reset Reset the database (deletes all users and feeds)
users List all users
feeds Show all available feeds
addfeed <name> <url> Add a new RSS feed
follow <url> Follow an existing feed
following List feeds you're following
unfollow <url> Unfollow a feed
browse [limit] View recent posts (default: 2)
agg <time> Run the scraper in a loop (e.g., agg 30s)
📖 Example Usage
1️⃣ Register and Login

gator register alice
gator login alice

2️⃣ Add and Follow Feeds

gator addfeed "TechCrunch" "<https://techcrunch.com/feed/>"
gator follow "<https://techcrunch.com/feed/>"

3️⃣ Browse Recent Posts

gator browse 5

4️⃣ Start Continuous Aggregation

gator agg 1m

Press Ctrl+C to stop the aggregator.
🛠 Development

If you're modifying queries, regenerate database code using:

sqlc generate

Run tests:

go test ./...

📜 License

MIT License. See LICENSE for details.
📬 Contact

Created by Your Name
📧 Email: <jeffrey.macneill@gmail.com>
