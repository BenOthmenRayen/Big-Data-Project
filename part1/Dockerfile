FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# Update sources.list to use archived repositories
RUN echo "deb http://archive.debian.org/debian stretch main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security stretch/updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y python3

# Set working directory
WORKDIR /app

# Copy necessary files
COPY mapper.py reducer.py purchases.txt runjob.sh ./

# Make scripts executable
RUN chmod +x mapper.py reducer.py runjob.sh

# Default command to keep the container alive
CMD ["sh", "-c", "./runjob.sh && tail -f /dev/null"]

