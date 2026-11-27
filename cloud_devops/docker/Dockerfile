FROM debian:bookworm-slim
#debian because we cant use alpine for vmstats etc.

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        procps \
        util-linux \
        hostname \
        gawk \
    && rm -rf /var/lib/apt/lists/*
    #good practice to clean up apt cache to reduce image size
#This creates app folder and copy over scripts
WORKDIR /app
COPY scripts/host_info.sh scripts/host_usage.sh /app/
RUN chmod +x /app/host_info.sh /app/host_usage.sh

CMD ["/app/host_usage.sh"]