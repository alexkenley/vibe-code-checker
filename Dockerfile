FROM ubuntu:22.04

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    gnupg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install ESLint and TypeScript tools globally
RUN npm install -g eslint@8.56.0
RUN npm install -g typescript@latest
RUN npm install -g @typescript-eslint/parser@6.21.0
RUN npm install -g @typescript-eslint/eslint-plugin@6.21.0
RUN npm install -g retire@4.3.2

# Set up Node.js tools
WORKDIR /home/scanner
COPY .eslintrc.js .
COPY eslint.config.js .
ENV PATH="/usr/local/lib/node_modules/.bin:${PATH}"

# Install Go
RUN curl -OL https://golang.org/dl/go1.22.1.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz \
    && rm go1.22.1.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

# Install Ruby
RUN apt-get update && apt-get install -y ruby-full \
    && gem install rubocop brakeman \
    && rm -rf /var/lib/apt/lists/*

# Install Python tools
RUN pip3 install flake8 bandit

# Create a non-root user
RUN useradd -m scanner
RUN chown -R scanner:scanner /home/scanner
RUN mkdir -p /code /reports \
    && chown -R scanner:scanner /code /reports

# Install Go tools and make them available to scanner user
RUN go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest \
    && go install github.com/securego/gosec/v2/cmd/gosec@latest \
    && cp -r /root/go /home/scanner/ \
    && chown -R scanner:scanner /home/scanner/go

# Set environment variables for scanner user
ENV PATH="/home/scanner/go/bin:/usr/local/go/bin:${PATH}"
ENV GOPATH="/home/scanner/go"

# Copy scanner script
COPY scan.py /home/scanner/scan.py
RUN chown scanner:scanner /home/scanner/scan.py

# Set working directory
WORKDIR /home/scanner

# Switch to scanner user
USER scanner

# Define entrypoint
ENTRYPOINT ["python3", "/home/scanner/scan.py"]

# Set default mount points
VOLUME ["/code", "/reports"]
