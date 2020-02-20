# Use miniconda3 image
FROM continuumio/miniconda3

# Set default model argument
ARG model_name=model.tar.gz

# Specify working directory
WORKDIR /app

# Copy over files
COPY . .

# Extract desired model and remove archive
RUN tar -xzf ${model_name} && rm ${model_name}

# Create the environment:
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "poli-bias", "/bin/bash", "-c"]

# Expose the correct port
EXPOSE 5000

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "poli-bias", "python", "-u", "server.py"]
# ENTRYPOINT ["python", "-u", "server.py"]
