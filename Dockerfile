# Use a Python-specific slim image (Debian-based)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to take advantage of Docker caching
COPY requirements.txt .

# Install dependencies
# 'slim' has better support for 'wheels' (pre-compiled libraries)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your files (app.py, pipe.pkl, df.pkl)
COPY . .

# Expose the port Streamlit uses (8501) or Flask (5000)
# Looking at your code, you are using Streamlit!
EXPOSE 8501

# Streamlit needs a specific way to run inside Docker
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]