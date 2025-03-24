FROM jupyter/base-notebook:latest

USER root
WORKDIR /home/jovyan

# Copy the requirements file
COPY requirements.txt /home/jovyan/

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose Jupyter port
EXPOSE 8888

CMD ["start-notebook.sh", "--NotebookApp.token=''"]
