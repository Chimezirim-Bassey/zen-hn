# Stage 1: Base build stage
FROM python:3.13.3-slim AS builder

LABEL author="Ichinga Samuel"

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /zen_hn

# Install dependencies first for caching benefit
RUN pip install --upgrade pip
COPY requirements.txt /zen_hn/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13.3-slim

# create directory for the user
ARG USERNAME=super_hacker
ARG GROUPNAME=zen_hackers

RUN groupadd --system $GROUPNAME && useradd --system -g $GROUPNAME $USERNAME


# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /zen_hn

# Copy application code
# change ownership of the files to the non-root user
COPY --chown=$USERNAME:$GROUPNAME . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER $USERNAME

# Expose the application port
EXPOSE 8000

# Make entry file executable
RUN chmod +x  /zen_hn/scripts/entrypoint.prod.sh

# Start the application using Gunicorn
CMD ["/zen_hn/scripts/entrypoint.prod.sh"]
