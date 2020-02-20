FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "poli-bias", "/bin/bash", "-c"]

# Expose the correct port
EXPOSE 5000

# The code to run when container is started:
COPY . .
ENTRYPOINT ["conda", "run", "-n", "poli-bias", "python", "app.py"]
