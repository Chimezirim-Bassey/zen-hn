# Stage 1: Base build stage
FROM python:3.13.3-slim AS builder

LABEL author="Ichinga Samuel"

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/zen_hn

# Install dependencies first for caching benefit
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/zen_hn
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13.3-slim

# create directory for the user
ARG USERNAME=super_hacker
ARG GROUPNAME=zen_hackers

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN groupadd --system $GROUPNAME && useradd --system -g $GROUPNAME $USERNAME

# Create application directory

RUN mkdir -p /home/$USERNAME/zen_hn && chown $USERNAME:$GROUPNAME /home/$USERNAME/zen_hn

# Switch to non-root user
USER $USERNAME

# Set the working directory
WORKDIR /home/$USERNAME/zen_hn

# Copy application code
# change ownership of the files to the non-root user
COPY --chown=$USERNAME:$GROUPNAME . .
RUN mkdir -p staticfiles
#COPY . .
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Make entry file executable
RUN chmod u+x  /home/$USERNAME/zen_hn/scripts/entrypoint.sh

# Start the application using Gunicorn
ENTRYPOINT ["/home/super_hacker/zen_hn/scripts/entrypoint.sh"]
