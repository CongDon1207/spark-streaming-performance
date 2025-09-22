# Dockerfile cho Spark với demo files
FROM bitnami/spark:3.5

# Set working directory
WORKDIR /opt/bitnami/spark

# Create app directory and required directories
USER root
RUN mkdir -p /opt/app/demo /opt/app/exercises /tmp/spark-events /root/.ivy2

# Set environment variables
ENV HOME=/root
ENV USER=root

# Copy demo files
COPY ./demo/ /opt/app/demo/
COPY ./exercises/ /opt/app/exercises/

# Copy spark configuration
COPY ./spark/spark-defaults.conf /opt/bitnami/spark/conf/spark-defaults.conf

# Set permissions
RUN chmod +x /opt/app/demo/*.py
RUN chmod +r /opt/app/demo/* /opt/app/exercises/ -R

# Expose ports
EXPOSE 7077 8080 4040 9999